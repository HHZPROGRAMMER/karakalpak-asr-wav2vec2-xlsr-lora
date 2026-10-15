# Karakalpak Speech Recognition — XLS-R 300M + LoRA + CTC

Automatic Speech Recognition (ASR) for the Karakalpak language using Wav2Vec2 XLS-R 300M, LoRA fine-tuning, and Connectionist Temporal Classification (CTC).

## Ishni qayerdan boshlash kerak?

Notebooklarni loyiha ildizidan oching. Raqamlar vazifalar tartibini bildiradi; barchasini ketma-ket Run All qilish talab qilinmaydi.

| Notebook | Vazifasi |
|---|---|
| [02_inspect_encoder_and_lora.ipynb](./02_inspect_encoder_and_lora.ipynb) | Encoder arxitekturasi va LoRA sozlamalarini ko‘rish |
| [03_train_xlsr_lora_ctc.ipynb](./03_train_xlsr_lora_ctc.ipynb) | XLS-R modelini LoRA va CTC bilan o‘qitish |
| [04_compare_checkpoints_and_tune_kenlm.ipynb](./04_compare_checkpoints_and_tune_kenlm.ipynb) | Checkpointlarni solishtirish va KenLM dekoderini sozlash |
| [05_analyze_errors_and_backup_model.ipynb](./05_analyze_errors_and_backup_model.ipynb) | Model xatolarini tahlil qilish va zaxira nusxa yaratish |
| [06_evaluate_mendeley_external_dataset.ipynb](./06_evaluate_mendeley_external_dataset.ipynb) | Oldingi Mendeley datasetida tashqi baholash |
| [07_optimize_validation_wer_cer.ipynb](./07_optimize_validation_wer_cer.ipynb) | Validation orqali WER va CER ko‘rsatkichlarini yaxshilash |
| [08_finetune_and_evaluate_benchmark.ipynb](./08_finetune_and_evaluate_benchmark.ipynb) | Modelni qo‘shimcha o‘qitish, dekoderni tanlash va benchmarkda baholash |

Modelni yaxshilashni davom ettirish uchun asosiy notebook: **08_finetune_and_evaluate_benchmark.ipynb**. `07` alohida validation/dekoder optimizatsiyasi uchun. `03` va `04` oldingi trening va tajriba jarayonlarini saqlaydi. Tarixiy notebooklarda `/home/intern/...` manzillari bor; ularni o‘z serveringizga moslamasdan Run All qilmang.

### Datasetlar va natijalar

- `audio_shards/`: modelni o‘qitish uchun audio shardlar.
- `data/`: train, validation va test metadata indekslari.
- `checkpoints/`: trening qadami bo‘yicha saqlangan holatlar.
- `experiments/`: oldingi trening tajribalari.
- `models/`: eksport qilingan adapterlar va model to‘plamlari.
- `processor/`: tokenizer va audio processor konfiguratsiyasi.
- `kenlm/`: til modeli, korpus va KenLM dasturlari.
- `results/`: mavjud tajriba natijalari; `validation_`, `test_`, `mendeley_` prefikslari baholash manbasini ko‘rsatadi.
- `external_validation/Benchmark/karakalpak_hf_dataset/`: hozirgi tashqi benchmark va uning `audio/` fayllari.

Benchmark uchun to‘liq manifest: `external_validation/Benchmark/karakalpak_hf_dataset/benchmark_all_samples.csv`. Filtrlangan to‘plamga kirish holati `benchmark_standardized_samples.csv`dagi `included_in_filtered` ustunida saqlangan. `08` notebookda benchmarkni bajarishdan oldin `BENCHMARK_CSV`ga kerakli manifestning aniq yo‘lini yozing. Eski va yordamchi CSVlar foydalanuvchi topshirig‘i bilan o‘chirildi; faqat to‘liq tuzatilgan va adabiylashtirilgan dataset CSVlari qoldi.

`06` notebook eski Mendeley datasetini kutadi. Uning CSV/audio manzillari hozirgi Benchmark manifestidan farq qiladi.

### Ishga tushirish holati

Nomlar almashtirilgach notebooklarning Python sintaksisi va yangilangan havolalari tekshirildi; to‘liq trening bajarilmadi. Hozirgi lokal Python muhitida PyTorch va kerakli ASR kutubxonalari yo‘q, NVIDIA drayveri ham ishlamayapti. `08`ni PyTorch, Transformers, PEFT, NumPy, pandas, PyArrow, SoundFile, librosa, pyctcdecode, jiwer va tqdm mavjud CUDA muhitida bajaring. Bazaviy `facebook/wav2vec2-xls-r-300m` ham yuklangan yoki yuklash uchun mavjud bo‘lishi kerak. KenLM binarilari server arxitekturasiga mos bo‘lishi kerak.


## Tashqi dataset matnlari

Qo‘shimcha adabiy variant: `external_validation/Benchmark/karakalpak_hf_dataset/benchmark_standardized_samples.csv` → `standardized_text`. 74 ta matnda 76 ta qo‘shimcha o‘zgarish bor; audio bilan tasdiqlangan transcript emas. Baholash uchun mavjud `text` saqlanadi.

60 ta matndagi 61 ta yozuv/so‘z chegarasi xatosi tuzatildi. Keyingi tozalashda asl nusxalar va yordamchi CSVlar foydalanuvchi topshirig‘i bilan o‘chirildi. Barcha 2613 audio–matnning mazmuniy mosligi hali tasdiqlanmagan.

- [Tuzatish hisoboti](external_validation/transcript_audit/README.md)
- [09_review_external_transcripts.ipynb](09_review_external_transcripts.ipynb): o‘zgargan va shubhali matnlarni ko‘rish, mos audioni tinglash.
- Tekshiruv: `python scripts/audit_external_transcripts.py --check`.

## Project Overview

This project focuses on developing a speech-to-text system for the low-resource Karakalpak language.

The model is based on Wav2Vec2 XLS-R 300M and fine-tuned using Low-Rank Adaptation (LoRA).

## Model Architecture

Audio (16 kHz)
    |
    v
CNN Feature Encoder
    |
    v
Transformer Encoder (XLS-R 300M)
    |
    v
LoRA Adaptation
    |
    v
CTC Classification Head
    |
    v
CTC Decoding
    |
    v
Karakalpak Transcription

LoRA adapters are applied to selected Transformer components during fine-tuning.

## Dataset

The project uses a preprocessed Karakalpak speech corpus.

Preprocessing includes:

- Audio resampling to 16 kHz
- Audio normalization and silence trimming
- Text normalization
- Duplicate removal
- Vocabulary preparation for CTC

## Training

Base architecture: Wav2Vec2 XLS-R 300M

Fine-tuning method: LoRA

Loss function: CTC Loss

Framework: PyTorch and Hugging Face Transformers

## Evaluation

Initial evaluation results:

| Metric | Score |
|--------|-------|
| Word Error Rate (WER) | 21% |
| Character Error Rate (CER) | 7% |

These are approximate results from the initial experiment.

## Language Model

KenLM experiments are included to investigate language-model-assisted CTC decoding.

## Future Improvements

- Hyperparameter optimization
- LoRA configuration tuning
- Data augmentation
- KenLM beam-search optimization
- Full fine-tuning experiments

## Technologies

- Python
- PyTorch
- Hugging Face Transformers
- PEFT / LoRA
- Wav2Vec2 XLS-R
- CTC
- KenLM
- Jupyter Notebook

## Author

Hasan Hafizov

GitHub: https://github.com/HHZPROGRAMMER
