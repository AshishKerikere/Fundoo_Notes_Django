# Generated by Django 4.1.7 on 2023-03-20 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NotesApp', '0005_alter_notesmodel_colour'),
    ]

    operations = [
        migrations.AddField(
            model_name='notesmodel',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
