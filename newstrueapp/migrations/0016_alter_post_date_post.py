# Generated by Django 4.1.5 on 2023-02-19 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newstrueapp', '0015_alter_comment_date_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_post',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 19, 13, 51, 6, 413328, tzinfo=datetime.timezone.utc)),
        ),
    ]