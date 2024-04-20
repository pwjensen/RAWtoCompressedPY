# Generated by Django 5.0.3 on 2024-04-02 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compressor", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="compressedimage",
            name="algorithm",
        ),
        migrations.RemoveField(
            model_name="compressedimage",
            name="size_reduction",
        ),
        migrations.AddField(
            model_name="compressedimage",
            name="binary_image",
            field=models.TextField(default=0),
        ),
        migrations.AddField(
            model_name="compressedimage",
            name="file_size",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="compressedimage",
            name="huffman_guide",
            field=models.TextField(default=0),
        ),
        migrations.AddField(
            model_name="rawimage",
            name="file_size",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
