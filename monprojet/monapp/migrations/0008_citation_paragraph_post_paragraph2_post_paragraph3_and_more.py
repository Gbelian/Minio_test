# Generated by Django 5.0.6 on 2024-05-28 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monapp', '0007_comment_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auteur', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='citation_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph2',
            field=models.TextField(default='Default description text'),
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph3',
            field=models.TextField(default='Default description text'),
        ),
        migrations.AddField(
            model_name='post',
            name='paragraph4',
            field=models.TextField(default='Default description text'),
        ),
    ]
