# Generated by Django 5.1.3 on 2024-11-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetwist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
