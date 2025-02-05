# Generated by Django 5.1.5 on 2025-01-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Image for the main page.', upload_to='main_images')),
                ('text', models.TextField(blank=True, help_text='Optional text associated with the image.', null=True)),
                ('author', models.CharField(blank=True, help_text='Author of the image.', max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the image was created.')),
            ],
            options={
                'verbose_name': 'Main Page Image',
                'verbose_name_plural': 'Main Page Images',
                'ordering': ['pk'],
            },
        ),
    ]
