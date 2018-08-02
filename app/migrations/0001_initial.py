# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-02 10:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_time', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('Ariana', 'Ariana'), ('Beja', 'Beja'), ('Ben Arous', 'Ben Arous'), ('Bizerte', 'Bizerte'), ('Jendouba', 'Jendouba'), ('Gabes', 'Gabes'), ('Gafsa', 'Gafsa'), ('Kairouan', 'Kairouan'), ('Kasserine', 'Kasserine'), ('Kebili', 'Kebili'), ('Le Kef', 'Le Kef'), ('La Manouba', 'La Manouba'), ('Mahdia', 'Mahdia'), ('Medenine', 'Medenine'), ('Monastir', 'Monastir'), ('Nabeul', 'Nabeul'), ('Sfax', 'Sfax'), ('Sidi Bouzid', 'Sidi Bouzid'), ('Siliana', 'Siliana'), ('Sousse', 'Sousse'), ('Tunis', 'Tunis'), ('Tataouine', 'Tataouine'), ('Tozeur', 'Tozeur'), ('Zaghouan', 'Zaghouan')], max_length=255)),
                ('role', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(choices=[('Ariana', 'Ariana'), ('Beja', 'Beja'), ('Ben Arous', 'Ben Arous'), ('Bizerte', 'Bizerte'), ('Jendouba', 'Jendouba'), ('Gabes', 'Gabes'), ('Gafsa', 'Gafsa'), ('Kairouan', 'Kairouan'), ('Kasserine', 'Kasserine'), ('Kebili', 'Kebili'), ('Le Kef', 'Le Kef'), ('La Manouba', 'La Manouba'), ('Mahdia', 'Mahdia'), ('Medenine', 'Medenine'), ('Monastir', 'Monastir'), ('Nabeul', 'Nabeul'), ('Sfax', 'Sfax'), ('Sidi Bouzid', 'Sidi Bouzid'), ('Siliana', 'Siliana'), ('Sousse', 'Sousse'), ('Tunis', 'Tunis'), ('Tataouine', 'Tataouine'), ('Tozeur', 'Tozeur'), ('Zaghouan', 'Zaghouan')], max_length=255)),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('budget', models.DecimalField(decimal_places=3, max_digits=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile'),
        ),
        migrations.AddField(
            model_name='offer',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='app.Project'),
        ),
    ]
