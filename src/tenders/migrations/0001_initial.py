# Generated by Django 3.0.6 on 2020-07-09 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ikz', models.CharField(blank=True, max_length=36)),
                ('num', models.CharField(max_length=19, unique=True)),
                ('status', models.CharField(blank=True, choices=[('in_work', 'In work'), ('done', 'Done'), ('zero', 'Zero'), ('cancel', 'Cancelled')], default='in_work', max_length=20)),
                ('smp', models.BooleanField()),
                ('price', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=11)),
                ('economy', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=11)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tickets.Ticket')),
            ],
        ),
    ]
