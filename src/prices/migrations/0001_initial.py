# Generated by Django 3.0.6 on 2020-07-09 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenders', '0001_initial'),
        ('limits', '0001_initial'),
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Сумма')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.Contract')),
                ('limit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='limits.LimitMoney')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StartPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Сумма')),
                ('limit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='limits.LimitMoney')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenders.Tender')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContractPriceChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delta', models.DecimalField(decimal_places=2, max_digits=11)),
                ('change', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.ContractChange')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prices.ContractPrice')),
            ],
        ),
        migrations.AddField(
            model_name='contractprice',
            name='start_price',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prices.StartPrice'),
        ),
    ]
