# Generated by Django 4.1.3 on 2023-05-14 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Catalog", "0006_alter_clinics_clinicaddress_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reviews",
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
                ("email", models.EmailField(max_length=254)),
                ("name", models.CharField(max_length=50)),
                ("text", models.CharField(max_length=100)),
                (
                    "review_clinic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Catalog.clinics",
                    ),
                ),
            ],
        ),
    ]
