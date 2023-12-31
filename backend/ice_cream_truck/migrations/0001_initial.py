# Generated by Django 4.2.6 on 2023-11-01 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flavor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FoodItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ice_cream_truck.fooditem')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ice_cream_truck.truck')),
            ],
        ),
        migrations.CreateModel(
            name='FoodItemFlavor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ice_cream_truck.flavor')),
                ('food_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ice_cream_truck.fooditem')),
            ],
        ),
        migrations.AddField(
            model_name='fooditem',
            name='food_item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ice_cream_truck.fooditemtype'),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='truck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ice_cream_truck.truck'),
        ),
    ]
