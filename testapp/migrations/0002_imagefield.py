# Generated by Django 2.0.6 on 2019-11-19 12:45

from django.db import migrations
import privates.fields
import privates.storages


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='File',
            name='image',
            field=privates.fields.PrivateMediaImageField(
                storage=privates.storages.PrivateMediaFileSystemStorage(), upload_to=''),
        ),
    ]