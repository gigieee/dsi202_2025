# Generated by Django 4.2.21 on 2025-05-13 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("adopt", "0005_generaldonation_slip_image_adoptionrequest"),
    ]

    operations = [
        migrations.RenameField(
            model_name="adoptionrequest",
            old_name="created_at",
            new_name="submitted_at",
        ),
    ]
