# Generated by Django 2.2.5 on 2019-12-03 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20191204_0132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='content',
            old_name='Title',
            new_name='title',
        ),
    ]
