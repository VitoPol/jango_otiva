# Generated by Django 4.1.3 on 2022-11-13 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_locations_alter_ads_options_alter_categories_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ads',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='ads',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='location_id',
            new_name='location',
        ),
    ]
