# Generated by Django 5.1.3 on 2024-11-25 05:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("document_extr", "0003_auto_20240307_1932"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentType",
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
                ("name", models.CharField(max_length=255)),
            ],
        ),
    ]
