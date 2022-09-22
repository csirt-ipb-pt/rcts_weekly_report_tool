# Generated by Django 3.1.2 on 2020-12-08 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=19)),
                ('rede', models.CharField(max_length=40)),
                ('data_1', models.CharField(max_length=26)),
                ('data_2', models.CharField(max_length=26)),
                ('count', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=19)),
                ('rede', models.CharField(max_length=40)),
                ('data_1', models.CharField(max_length=26)),
                ('data_2', models.CharField(max_length=26)),
                ('count', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Vul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=19)),
                ('port', models.CharField(max_length=10000)),
                ('rede', models.CharField(max_length=40)),
                ('data_1', models.CharField(max_length=26)),
                ('data_2', models.CharField(max_length=26)),
                ('count', models.CharField(max_length=10000)),
            ],
        ),
    ]