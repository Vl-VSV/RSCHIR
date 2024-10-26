# Generated by Django 5.1.2 on 2024-10-20 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('hot', 'Hot'), ('soup', 'Soup'), ('dessert', 'Dessert'), ('salad', 'Salad'), ('drink', 'Drink')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]