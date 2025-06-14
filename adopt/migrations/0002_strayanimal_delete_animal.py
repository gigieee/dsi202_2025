# Generated by Django 4.2.21 on 2025-05-12 13:41

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("adopt", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StrayAnimal",
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
                ("pet_id", models.CharField(max_length=30, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("breed", models.CharField(max_length=100)),
                (
                    "species",
                    models.CharField(
                        choices=[("dog", "Dog"), ("cat", "Cat")], max_length=10
                    ),
                ),
                ("age_value", models.PositiveIntegerField()),
                (
                    "age_unit",
                    models.CharField(
                        choices=[
                            ("day", "Day(s)"),
                            ("week", "Week(s)"),
                            ("month", "Month(s)"),
                            ("year", "Year(s)"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")], max_length=10
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("small", "Small"),
                            ("medium", "Medium"),
                            ("large", "Large"),
                            ("extra large", "Extra Large"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "coat_length",
                    models.CharField(
                        choices=[
                            ("hairless", "Hairless"),
                            ("short", "Short"),
                            ("medium", "Medium"),
                            ("long", "Long"),
                            ("wire", "Wire"),
                            ("curly", "Curly"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "good_with",
                    multiselectfield.db.fields.MultiSelectField(
                        blank=True,
                        choices=[
                            ("kids", "Kids"),
                            ("other dogs", "Other Dogs"),
                            ("cats", "Cats"),
                        ],
                        max_length=50,
                        verbose_name="Good with",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("Apricot / Beige", "Apricot / Beige"),
                            ("Bicolor", "Bicolor"),
                            ("Black", "Black"),
                            ("Brindle", "Brindle"),
                            ("Brown/Chocolate", "Brown/Chocolate"),
                            ("Golden", "Golden"),
                            ("Gray/Blue/Silver", "Gray/Blue/Silver"),
                            ("Harlequin", "Harlequin"),
                            ("Merle (Blue)", "Merle (Blue)"),
                            ("Merle (Red)", "Merle (Red)"),
                            ("Red / Chestnut / Orange", "Red / Chestnut / Orange"),
                            ("Sable", "Sable"),
                            (
                                "Tricolor (Brown,Black, & White)",
                                "Tricolor (Brown,Black, & White)",
                            ),
                            ("White / Cream", "White / Cream"),
                            (
                                "Yellow / Tan / Blond / Fawn",
                                "Yellow / Tan / Blond / Fawn",
                            ),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "care_and_behavior",
                    models.CharField(
                        choices=[
                            ("House-trained", "House-trained"),
                            ("Special Needs", "Special Needs"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "days_on_pawpal",
                    models.CharField(
                        choices=[
                            ("Any", "Any"),
                            ("1", "1"),
                            ("7", "7"),
                            ("14", "14"),
                            ("30+", "30+"),
                        ],
                        max_length=10,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=100)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="animal_images/"
                    ),
                ),
                ("story_describe", models.TextField(blank=True)),
                (
                    "behavior",
                    models.CharField(
                        choices=[
                            ("Anxiety", "Anxiety"),
                            ("Barking and Howling", "Barking and Howling"),
                            ("Biting", "Biting"),
                            ("Chewing", "Chewing"),
                            ("Others", "Others"),
                        ],
                        max_length=50,
                    ),
                ),
                ("health_status", models.TextField(blank=True)),
                ("is_adopted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name="Animal",
        ),
    ]
