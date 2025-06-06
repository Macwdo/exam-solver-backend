# Generated by Django 5.2.1 on 2025-05-23 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('answer', models.JSONField(blank=True, null=True)),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='not_started', max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
