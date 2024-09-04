# Generated by Django 5.0.6 on 2024-08-30 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water_management', '0003_alter_watermeterreading_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionAdvice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='advice_images/')),
                ('min_value', models.FloatField()),
                ('max_value', models.FloatField()),
            ],
        ),
    ]
