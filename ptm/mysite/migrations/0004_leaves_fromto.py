# Generated by Django 2.2.6 on 2019-11-13 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_leaves_type_of_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaves',
            name='fromto',
            field=models.DateField(default='2019-02-02'),
            preserve_default=False,
        ),
    ]
