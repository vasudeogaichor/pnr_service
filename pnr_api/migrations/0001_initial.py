# Generated by Django 4.1.5 on 2023-01-29 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnr_number', models.TextField(max_length=10)),
                ('pnr_status', models.TextField()),
            ],
        ),
    ]
