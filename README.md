# Karakalpak Speech Recognition — XLS-R 300M + LoRA + CTC

Automatic Speech Recognition (ASR) for the Karakalpak language using Wav2Vec2 XLS-R 300M, LoRA fine-tuning, and Connectionist Temporal Classification (CTC).

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
