# Generated by Django 4.2.4 on 2023-11-23 23:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_info', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscribe_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('inir_rate_type', models.TextField()),
                ('user_id', models.ManyToManyField(related_name='subscribe_product', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(unique=True)),
                ('fin_prdt_cd', models.TextField()),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField(null=True)),
                ('join_member', models.TextField()),
                ('join_way', models.TextField(null=True)),
                ('spcl_cnd', models.TextField()),
                ('join_user', models.ManyToManyField(blank=True, related_name='joined_saving_products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('fin_prdt_cd', models.TextField()),
                ('intr_rate_type_nm', models.TextField(max_length=100)),
                ('intr_rate', models.FloatField(blank=True, default=-1, null=True)),
                ('intr_rate2', models.FloatField(blank=True, default=-1, null=True)),
                ('save_trm', models.FloatField()),
                ('rsrv_type_nm', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option', to='api.savingproduct')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_unit', models.TextField()),
                ('ttb', models.TextField()),
                ('tts', models.TextField()),
                ('deal_bas_r', models.TextField()),
                ('bkpr', models.TextField()),
                ('yy_efee_r', models.TextField()),
                ('ten_dd_efee_r', models.TextField()),
                ('kftc_bkpr', models.TextField()),
                ('kftc_deal_bas_r', models.TextField()),
                ('cur_nm', models.TextField()),
                ('exchangeDate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.exchangedate')),
            ],
        ),
        migrations.CreateModel(
            name='DepositProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(unique=True)),
                ('fin_prdt_cd', models.TextField()),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField(null=True)),
                ('join_member', models.TextField()),
                ('join_way', models.TextField(null=True)),
                ('spcl_cnd', models.TextField()),
                ('join_user', models.ManyToManyField(blank=True, related_name='joined_deposit_products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepositOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('fin_prdt_cd', models.TextField()),
                ('intr_rate_type_nm', models.TextField(max_length=100)),
                ('intr_rate', models.FloatField(blank=True, default=-1, null=True)),
                ('intr_rate2', models.FloatField()),
                ('save_trm', models.FloatField()),
                ('intr_rate_type', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='option', to='api.depositproduct')),
            ],
        ),
    ]
