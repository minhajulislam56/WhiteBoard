# Generated by Django 2.2.5 on 2019-10-09 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20191010_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=1),
        ),
        migrations.DeleteModel(
            name='Course',
        ),
    ]
