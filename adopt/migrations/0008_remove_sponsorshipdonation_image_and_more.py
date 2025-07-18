# Generated by Django 4.2.21 on 2025-05-14 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("adopt", "0007_blog_rename_submitted_at_adoptionrequest_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sponsorshipdonation",
            name="image",
        ),
        migrations.RemoveField(
            model_name="sponsorshipdonation",
            name="sponsorship",
        ),
        migrations.AddField(
            model_name="sponsorshipdonation",
            name="payment_slip",
            field=models.ImageField(default=True, upload_to="sponsorship_slips/"),
        ),
        migrations.AddField(
            model_name="sponsorshipdonation",
            name="pet",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="adopt.strayanimal",
            ),
        ),
    ]
