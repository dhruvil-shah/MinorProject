# Generated by Django 4.1 on 2022-11-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0005_rename_course_coursestudent_course_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
