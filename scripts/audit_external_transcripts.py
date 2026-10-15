"""Validate the two retained dataset CSVs without creating additional CSV files.

python scripts/audit_external_transcripts.py --check
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import wave

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'external_validation/Benchmark/karakalpak_hf_dataset'


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.parse_args()
    source = read_csv(DATA / 'benchmark_all_samples.csv')
    editorial = read_csv(DATA / 'benchmark_standardized_samples.csv')
    assert source and len(source) == len(editorial)
    assert len({r['audio_path'] for r in source}) == len(source)
    errors = []
    for a, b in zip(source, editorial):
        assert all(a[k] == b[k] for k in a), 'Source/editorial metadata mismatch'
        assert a['text'].strip() and b['standardized_text'].strip()
        assert b['audio_alignment_verified'] == 'False'
        path = DATA / a['audio_path']
        try:
            assert path.resolve().is_relative_to(DATA.resolve())
            with wave.open(str(path), 'rb') as audio:
                frames, channels, width = audio.getnframes(), audio.getnchannels(), audio.getsampwidth()
                assert frames > 0 and channels > 0 and audio.getframerate() > 0
                assert len(audio.readframes(frames)) == frames * channels * width
                assert abs(frames / audio.getframerate() - float(a['duration'])) <= 0.02
        except Exception as exc:
            errors.append({'audio_path': a['audio_path'], 'error': str(exc)})
    assert not errors, errors[:5]
    print(json.dumps({'records': len(source), 'audio_files_checked': len(source),
                      'audio_read_errors': len(errors), 'audio_files_modified': 0,
                      'editorial_changes': sum(a['text'] != b['standardized_text'] for a, b in zip(source, editorial)),
                      'audio_alignment_verified': False,
                      'csv_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in sorted(DATA.glob('*.csv'))}}, indent=2))


if __name__ == '__main__':
    main()
