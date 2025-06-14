# Generated by Django 4.2.21 on 2025-05-15 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("adopt", "0009_notification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="generaldonation",
            name="slip_image",
            field=models.ImageField(blank=True, null=True, upload_to="donation_slips/"),
        ),
        migrations.CreateModel(
            name="MedicalDonation",
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
                ("donor_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("slip_image", models.ImageField(upload_to="medical_donation_slips/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "sponsorship",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="donations",
                        to="adopt.medicalsponsorship",
                    ),
                ),
            ],
        ),
    ]
