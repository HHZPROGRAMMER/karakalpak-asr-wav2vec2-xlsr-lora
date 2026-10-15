"""Create a Karakalpak editorial text variant without changing benchmark references.

Run from any folder: python scripts/standardize_external_transcripts.py
The new CSV stays beside the source, so its relative audio paths still resolve.
"""
from __future__ import annotations
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'external_validation/Benchmark/karakalpak_hf_dataset'
AUDIT = ROOT / 'external_validation/transcript_audit'
SOURCE = DATA / 'benchmark_all_samples.csv'
OUTPUT = DATA / 'benchmark_standardized_samples.csv'


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def encoded_csv(fields, rows):
    handle = io.StringIO(newline='')
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode('utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compile_rules(config):
    rules = {r['old']: r for r in config['rules']}
    assert len(rules) == len(config['rules'])
    assert all(r['old'] != r['new'] for r in rules.values())
    regex = re.compile(r'(?<!\w)(?:' + '|'.join(
        re.escape(w) for w in sorted(rules, key=len, reverse=True)) + r')(?!\w)')
    return rules, regex


def main():
    config_path = AUDIT / 'standardization_rules.json'
    config = json.loads(config_path.read_text())
    rules, regex = compile_rules(config)
    source_fields, rows = read_csv(SOURCE)
    assert {'audio_path', 'text', 'duration', 'split'} <= set(source_fields)
    assert len({r['audio_path'] for r in rows}) == len(rows)
    protected = sorted(DATA.glob('*.csv')) + sorted((AUDIT / 'originals').glob('*.csv'))
    protected = [p for p in protected if p != OUTPUT]
    hashes_before = {str(p.relative_to(ROOT)): digest(p) for p in protected}
    _, existing_output = read_csv(OUTPUT)
    filtered_paths = {r['audio_path'] for r in existing_output if r['included_in_filtered'] == 'True'}
    review_rows = []
    output, changes, replacements = [], [], []
    adapted_by_path = {}
    unresolved = []
    alphabet = set('abcdefghijklmnopqrstuvwxyzáǵńóúı ')
    for row in rows:
        hits = list(regex.finditer(row['text']))
        standardized = regex.sub(lambda m: rules[m.group()]['new'], row['text'])
        assert not (set(standardized) - alphabet), 'Unexpected alphabet'
        assert regex.sub(lambda m: rules[m.group()]['new'], standardized) == standardized, 'Non-idempotent rules'
        assert (DATA / row['audio_path']).is_file(), row['audio_path']
        adapted = standardized != row['text']
        output.append({**row, 'standardized_text': standardized,
                       'standardization_changed': adapted,
                       'audio_alignment_verified': False,
                       'included_in_filtered': row['audio_path'] in filtered_paths})
        adapted_by_path[row['audio_path']] = standardized
        if adapted:
            changes.append({'audio_path': row['audio_path'], 'text': row['text'],
                            'standardized_text': standardized,
                            'rules': ' | '.join(dict.fromkeys(m.group() for m in hits)),
                            'audio_alignment_verified': False})
        for m in hits:
            rule = rules[m.group()]
            replacements.append({'audio_path': row['audio_path'], 'old': rule['old'],
                                 'new': rule['new'], 'kind': rule['kind'], 'reason': rule['reason']})
    for review in review_rows:
        term = review['term']
        if term in config['protected_terms']:
            protected_term = config['protected_terms'][term]
            status = 'protected_valid_or_contextual_form'
            reason = protected_term['reason']
        elif term in rules or term in {'húwlegep', 'bolınıwına'}:
            status = 'editorial_variant_provided_audio_unverified'
            reason = 'Adabiy variant tayyor; bu audio bilan tasdiqlangan tuzatish emas.'
        else:
            status = 'unresolved_preserved'
            reason = 'Aniq adabiy almashtirish yetarlicha asoslanmadi; taxmin qilinmadi.'
        unresolved.append({**review, 'standardized_text': adapted_by_path[review['audio_path']],
                           'editorial_status': status, 'editorial_reason': reason})
    output_fields = source_fields + ['standardized_text', 'standardization_changed',
                                    'audio_alignment_verified', 'included_in_filtered']
    output_bytes = encoded_csv(output_fields, output)
    if OUTPUT.exists():
        # Refuse silent replacement if the user has edited the variant since generation.
        previous_summary = AUDIT / 'standardization_summary.json'
        if previous_summary.exists():
            expected_hash = json.loads(previous_summary.read_text())['output_sha256']
            if digest(OUTPUT) != expected_hash:
                raise RuntimeError('The standardized CSV has user edits; merge them before regenerating.')
    OUTPUT.write_bytes(output_bytes)
    assert all({k: r[k] for k in source_fields} == source for r, source in zip(output, rows))
    assert hashes_before == {str(p.relative_to(ROOT)): digest(p) for p in protected}, 'Source files changed'
    summary = {
        'source': str(SOURCE.relative_to(ROOT)), 'output': str(OUTPUT.relative_to(ROOT)),
        'source_text_column': 'text', 'editorial_text_column': 'standardized_text',
        'records': len(rows), 'adapted_rows': len(changes),
        'word_or_boundary_replacements': len(replacements),
        'rules_with_matches': len({r['old'] for r in replacements}),
        'replacement_kinds': dict(collections.Counter(r['kind'] for r in replacements)),
        'review_status_flags': dict(collections.Counter(r['editorial_status'] for r in unresolved)),
        'unresolved_review_rows': None,  # Detailed review CSVs were removed at user request.
        'original_reference_files_modified': 0, 'audio_files_modified': 0,
        'audio_alignment_verified': False, 'use_standardized_text_for_asr_scoring': False,
        'source_sha256': digest(SOURCE), 'output_sha256': digest(OUTPUT),
        'rules_sha256': digest(config_path), 'protected_source_hashes': hashes_before,
        'sources': config['sources'],
    }
    (AUDIT / 'standardization_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in {'protected_source_hashes','sources'}},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
