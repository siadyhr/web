# Generated by Django 1.11.12 on 2018-04-17 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eval', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wikiarticletimeout',
            name='title',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
