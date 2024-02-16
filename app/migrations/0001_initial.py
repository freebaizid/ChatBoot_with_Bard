# Generated by Django 5.0.2 on 2024-02-16 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot', models.TextField()),
                ('user', models.TextField()),
                ('session_id', models.CharField(max_length=800)),
            ],
        ),
    ]