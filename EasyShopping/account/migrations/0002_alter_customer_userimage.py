# Generated by Django 5.1 on 2024-10-11 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='userImage',
            field=models.ImageField(blank=True, default='customers/userImageDefault.png', null=True, upload_to='customers/'),
        ),
    ]
