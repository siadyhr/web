# Generated by Django 1.11.12 on 2018-04-12 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wiki', '0002_urlpath_moved_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikiArticleTimeout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeoutMonth', models.PositiveSmallIntegerField(null=True)),
                ('updated', models.DateField(null=True)),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wikiArticleTimeout', to='wiki.Article')),
            ],
        ),
    ]
