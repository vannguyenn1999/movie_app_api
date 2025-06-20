# Generated by Django 5.2 on 2025-05-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_alter_movie_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['-created_at', '-updated_at']},
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='movies/thumbs/', verbose_name='Movie_Image'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='language',
            field=models.CharField(default='English', max_length=10),
        ),
    ]
