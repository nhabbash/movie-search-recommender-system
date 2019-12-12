# Generated by Django 3.0 on 2019-12-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('original_lan', models.TextField(blank=True, null=True)),
                ('spoken_lan', models.TextField(blank=True, null=True)),
                ('genres', models.TextField(blank=True, null=True)),
                ('data', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
    ]
