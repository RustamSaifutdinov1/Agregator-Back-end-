# Generated by Django 4.1.3 on 2022-12-05 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Catalog", "0005_remove_clinics_cliniccity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clinics",
            name="ClinicAddress",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="clinics",
            name="ClinicWork_time",
            field=models.TextField(blank=True),
        ),
    ]
