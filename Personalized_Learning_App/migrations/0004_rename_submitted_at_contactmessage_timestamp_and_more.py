# Generated by Django 5.1.4 on 2025-04-04 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personalized_Learning_App', '0003_contactmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='submitted_at',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='contactmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
