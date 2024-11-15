# Generated by Django 5.1.3 on 2024-11-15 00:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('pets', '0002_alter_pet_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='group_pets', to='groups.group'),
        ),
    ]