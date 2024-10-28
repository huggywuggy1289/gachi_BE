# Generated by Django 5.1.2 on 2024-10-27 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=100)),
                ('price', models.IntegerField()),
                ('item_image', models.ImageField(upload_to='items/')),
                ('item_type', models.CharField(choices=[('sticker', '스티커'), ('theme', '테마')], max_length=10)),
            ],
        ),
    ]
