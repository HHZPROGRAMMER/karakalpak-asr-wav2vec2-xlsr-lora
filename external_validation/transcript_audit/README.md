# Tashqi datasetning saqlangan fayllari

Foydalanuvchi topshirig‘i bilan eski va yordamchi CSVlar, shu jumladan asl zaxira nusxalar o‘chirildi. Faqat quyidagi ikki CSV qoldi:

- `external_validation/Benchmark/karakalpak_hf_dataset/benchmark_all_samples.csv`: barcha 2613 namunaning imlosi tuzatilgan transcripti (`text`). Avval 60 ta matnda 61 ta tuzatish bajarilgan.
- `external_validation/Benchmark/karakalpak_hf_dataset/benchmark_standardized_samples.csv`: barcha 2613 namuna, saqlangan `text` va alohida `standardized_text`. Adabiy variantda qo‘shimcha 74 ta matnda 76 ta o‘zgarish bor. `included_in_filtered` oldingi filtrlangan 2548 namuna va chiqarilgan 65 namunani ajratadi.

Audio fayllar va ikkala CSVning tarkibi tozalash paytida o‘zgarmadi.

`python scripts/audit_external_transcripts.py --check` ikki CSV va audio fayllarni tekshiradi; yordamchi CSV yaratmaydi. `09_review_external_transcripts.ipynb` matnlarni ko‘rish va audioni tinglash uchun moslandi.

`python scripts/standardize_external_transcripts.py` mavjud transcriptdan adabiy variantni qayta yaratadi; yordamchi CSV yaratmaydi. Qoidalar JSON fayllarda saqlandi. Oldingi `summary.json` tarixiy audit hisoboti; undagi ayrim CSV xeshlariga tegishli fayllar foydalanuvchi topshirig‘i bilan o‘chirilgan.

Hech bir audio tinglab tasdiqlanmagan. `standardized_text` adabiy/muharrirlik varianti bo‘lib, audiodagi so‘zlardan farq qilishi mumkin; u avtomatik WER/CER reference emas.

Imlo manbasi: [Qaraqalpaq tiliniń orfografiyalıq sózligi, 2020](https://elibrary.karsu.uz/wp-content/uploads/2023/06/M.Dawletov-Qaraqalpaq-tilinin-orfografiyaliq-sozligi.2020-1.pdf).
