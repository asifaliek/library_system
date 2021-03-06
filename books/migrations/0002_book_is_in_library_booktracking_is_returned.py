# Generated by Django 4.0.4 on 2022-05-11 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_in_library',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='booktracking',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]
