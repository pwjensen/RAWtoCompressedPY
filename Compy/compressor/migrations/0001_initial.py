# Generated by Django 5.0.3 on 2024-04-02 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RawImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="assets/originals/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CompressedImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("compressed_image", models.ImageField(upload_to="images/compressed/")),
                (
                    "algorithm",
                    models.CharField(
                        choices=[
                            ("RLE", "RLE Encoder"),
                            ("Huffman", "Huffman Encoder"),
                            ("LZ77", "LZ77 Encoder"),
                        ],
                        max_length=50,
                    ),
                ),
                ("size_reduction", models.FloatField()),
                ("compressed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "original",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="compressed_images",
                        to="compressor.rawimage",
                    ),
                ),
            ],
        ),
    ]
