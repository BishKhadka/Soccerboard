# Generated by Django 4.2.2 on 2023-06-10 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App1", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mymodel",
            name="field1",
        ),
        migrations.RemoveField(
            model_name="mymodel",
            name="field2",
        ),
        migrations.RemoveField(
            model_name="mymodel",
            name="field3",
        ),
        migrations.RemoveField(
            model_name="mymodel",
            name="field4",
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Competition",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Date",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Day",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Fouls",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="GA",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="GF",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Offside",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Opponent",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Possession",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Red",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Result",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Shots",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Shots_Target",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Team",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Time",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Venue",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
        migrations.AddField(
            model_name="mymodel",
            name="Yellow",
            field=models.CharField(default="DEFAULT", max_length=255),
        ),
    ]
