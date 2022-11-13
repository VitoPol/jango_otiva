# Generated by Django 4.1.3 on 2022-11-13 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
            options={
                'verbose_name': 'Локация',
                'verbose_name_plural': 'Локации',
            },
        ),
        migrations.AlterModelOptions(
            name='ads',
            options={'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.RemoveField(
            model_name='ads',
            name='author',
        ),
        migrations.AddField(
            model_name='ads',
            name='category_id',
            field=models.ForeignKey(default=999, on_delete=django.db.models.deletion.CASCADE, to='ads.categories'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ads',
            name='image',
            field=models.ImageField(default=999, upload_to='logos/'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=40)),
                ('username', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('role', models.CharField(max_length=40)),
                ('age', models.IntegerField()),
                ('location_id', models.ManyToManyField(to='ads.locations')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.AddField(
            model_name='ads',
            name='author_id',
            field=models.ForeignKey(default=999, on_delete=django.db.models.deletion.CASCADE, to='ads.users'),
            preserve_default=False,
        ),
    ]