# Generated by Django 4.1 on 2022-10-03 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='course',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]