# Generated by Django 2.2.3 on 2019-07-31 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XMoneyObj',
            fields=[
                ('object_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='消费项名称(Name)')),
                ('price', models.CharField(max_length=200, verbose_name='支出金额数(Price)')),
                ('currency_unit', models.CharField(max_length=200, verbose_name='货币单位(Currency Unit)')),
                ('description', models.TextField(verbose_name='消费项描述(Description)')),
                ('category', models.CharField(max_length=200, verbose_name='消费项性质(Category)')),
                ('source', models.CharField(max_length=200, verbose_name='消费项钱款来源(Source)')),
                ('source_c_price', models.CharField(max_length=200, verbose_name='消费项钱款来源 澄金额数(Source_C_Price)')),
                ('source_q_price', models.CharField(max_length=200, verbose_name='消费项钱款来源 清金额数(Source_Q_Price)')),
                ('source_c_currency_unit', models.CharField(max_length=200, verbose_name='消费项钱款来源 澄货币单位(Source_C_CU)')),
                ('source_q_currency_unit', models.CharField(max_length=200, verbose_name='消费项钱款来源 清货币单位(Source_Q_CU)')),
                ('trip_day', models.CharField(max_length=200, verbose_name='旅行自定义天(Trip Day)')),
                ('local_date', models.CharField(max_length=200, verbose_name='当地具体日期(Local Day)')),
            ],
            options={
                'verbose_name': '消费项(XMoneyObject)',
                'verbose_name_plural': '消费项(XMoneyObject)',
            },
        ),
        migrations.CreateModel(
            name='XUserExInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, verbose_name='username')),
                ('headportrait', models.ImageField(upload_to='user-head-portraits/')),
            ],
            options={
                'verbose_name': 'UserExtraInformation',
                'verbose_name_plural': 'UserExtraInformation',
            },
        ),
    ]
