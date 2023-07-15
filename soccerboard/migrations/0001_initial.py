from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TableModel",
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
                ("Date", models.DateField(null=True)),
                ("Competition", models.CharField(default="DEFAULT", max_length=255)),
                ("Day", models.CharField(default="DEFAULT", max_length=255)),
                ("Venue", models.CharField(default="DEFAULT", max_length=255)),
                ("Result", models.CharField(default="DEFAULT", max_length=255)),
                ("GF", models.IntegerField(default=-1)),
                ("GA", models.IntegerField(default=-1)),
                ("Opponent", models.CharField(default="DEFAULT", max_length=255)),
                ("Possession", models.IntegerField(default=-1)),
                ("Shots", models.IntegerField(default=-1)),
                ("Shots_Target", models.IntegerField(default=-1)),
                ("Yellow", models.IntegerField(default=-1)),
                ("Red", models.IntegerField(default=-1)),
                ("Fouls", models.IntegerField(default=-1)),
                ("Offside", models.IntegerField(default=-1)),
                ("Team", models.CharField(default="DEFAULT", max_length=255)),
            ],
        ),
    ]
