# Generated by Django 3.2.7 on 2021-09-09 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210909_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.cart'),
        ),
    ]
