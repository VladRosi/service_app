# Generated by Django 3.2.16 on 2023-12-10 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20231210_1716'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['field_a', 'field_b'], name='services_su_field_a_155836_idx'),
        ),
    ]
