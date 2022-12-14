# Generated by Django 4.1.3 on 2022-11-26 10:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("Catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryClinics",
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
                ("name", models.CharField(db_index=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name="Services",
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
                ("name", models.CharField(blank=True, max_length=50)),
                ("content", models.TextField(blank=True)),
                ("photo", models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/")),
            ],
        ),
        migrations.RemoveField(
            model_name="clinics",
            name="title",
        ),
        migrations.AddField(
            model_name="clinics",
            name="address",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="clinics",
            name="city",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="clinics",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="clinics",
            name="name",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="clinics",
            name="photo",
            field=models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/"),
        ),
        migrations.AddField(
            model_name="clinics",
            name="telephone",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="clinics",
            name="time_create",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="clinics",
            name="time_update",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="clinics",
            name="work_time",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name="Doctor",
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
                ("name", models.CharField(blank=True, max_length=50)),
                ("price", models.CharField(blank=True, max_length=50)),
                ("work_time", models.CharField(blank=True, max_length=20)),
                ("experience", models.CharField(blank=True, max_length=20)),
                ("photo", models.ImageField(blank=True, upload_to="photos/%Y/%m/%d/")),
                ("is_published", models.BooleanField(default=True)),
                (
                    "clinic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Catalog.clinics",
                    ),
                ),
                (
                    "service",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Catalog.services",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="clinics",
            name="cat",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="Catalog.categoryclinics",
            ),
        ),
    ]
