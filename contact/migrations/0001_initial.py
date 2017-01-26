# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-25 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contact_name', models.CharField(max_length=255, verbose_name='Name')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('originating_page', models.CharField(blank=True, max_length=255)),
                ('service', models.CharField(max_length=63)),
                ('content', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TriageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('contact_name', models.CharField(max_length=255, verbose_name='Name')),
                ('contact_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('originating_page', models.CharField(blank=True, max_length=255)),
                ('service', models.CharField(max_length=63)),
                ('company_name', models.CharField(max_length=255)),
                ('soletrader', models.BooleanField(default=False)),
                ('company_number', models.CharField(max_length=32)),
                ('company_postcode', models.CharField(max_length=32)),
                ('website_address', models.URLField()),
                ('turnover', models.CharField(default='', max_length=10, choices=[
                    ('Under 100k', 'Under £100,000'),
                    ('100k-500k', '£100,000 to £500,000'),
                    ('500k-2m', '£500,001 and £2million'),
                    ('2m+', 'More than £2million')])),
                ('sku_count', models.IntegerField()),
                ('trademarked', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=10)),
                ('experience', models.CharField(default='', max_length=16, choices=[
                    ('Not yet', 'Not yet'),
                    ('Yes, sometimes', 'Yes, sometimes'),
                    ('Yes, regularly', 'Yes, regularly')])),
                ('description', models.TextField()),
                ('contact_phone', models.CharField(blank=True, max_length=16)),
                ('email_pref', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]