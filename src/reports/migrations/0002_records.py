# Generated by Django 3.1.2 on 2020-12-19 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=19)),
                ('rede', models.CharField(max_length=40)),
                ('tipo', models.CharField(max_length=13)),
                ('data_1', models.CharField(max_length=26)),
                ('data_2', models.CharField(max_length=26)),
                ('email_sent', models.CharField(max_length=9)),
            ],
        ),
    ]
