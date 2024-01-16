# Generated by Django 5.0.1 on 2024-01-16 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('market', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.IntegerField()),
                ('high', models.IntegerField()),
                ('low', models.IntegerField()),
                ('close', models.IntegerField()),
                ('volume', models.BigIntegerField()),
                ('date', models.DateField()),
                ('is_finalized', models.BooleanField(default=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.ticker')),
            ],
            options={
                'verbose_name_plural': 'Price Data',
            },
        ),
    ]
