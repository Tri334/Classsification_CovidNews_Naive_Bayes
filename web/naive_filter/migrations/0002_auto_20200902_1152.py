# Generated by Django 3.1 on 2020-09-02 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naive_filter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termunikvalue',
            name='hoax',
            field=models.CharField(max_length=10000000),
        ),
        migrations.AlterField(
            model_name='termunikvalue',
            name='valid',
            field=models.CharField(max_length=10000000),
        ),
    ]
