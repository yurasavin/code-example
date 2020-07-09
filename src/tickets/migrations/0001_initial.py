# Generated by Django 3.0.6 on 2020-07-09 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('limits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('status', models.BooleanField(default=True, max_length=10)),
                ('year', models.ManyToManyField(db_index=True, to='limits.Limit')),
            ],
        ),
    ]
