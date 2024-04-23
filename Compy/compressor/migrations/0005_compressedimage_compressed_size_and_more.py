# Generated by Django 4.1.3 on 2024-04-23 16:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("compressor", "0004_compressedimage_file_loc"),
    ]

    operations = [
        migrations.AddField(
            model_name="compressedimage",
            name="compressed_size",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="compressedimage",
            name="file_loc",
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="compressedimage",
            name="size_reduction",
            field=models.TextField(max_length=200, null=True),
        ),
    ]