from django.db import models

# Create your models here.
class XMoneyObj(models.Model):
  # 自增id
  object_id = models.AutoField(primary_key=True)
  # 名称
  name = models.CharField('消费项名称(Name)',max_length=200)
  # 价格数
  price = models.CharField('支出金额数(Price)',max_length=200)
  # 货币单位
  currency_unit = models.CharField('货币单位(Currency Unit)',max_length=200)
  # 消费项描述, 亦或是文章, 骚话
  description = models.TextField('消费项描述(Description)')
  # 消费项性质, 属于澄独立消费还是清独立消费还是公共消费
  category = models.CharField('消费项性质(Category)',max_length=200)
  # 消费项的钱款来源, 来自澄库, 还是来自清库, 还是被拆分双方各有承担
  source = models.CharField('消费项钱款来源(Source)',max_length=200)
  # 消费项来源为两家合资, c和q分别承担多少金额数量
  source_c_price = models.CharField('消费项钱款来源 澄金额数(Source_C_Price)',max_length=200)
  source_q_price = models.CharField('消费项钱款来源 清金额数(Source_Q_Price)',max_length=200)
  # 消费项来源为两家合资, c和q分别的货币单位
  source_c_currency_unit = models.CharField('消费项钱款来源 澄货币单位(Source_C_CU)',max_length=200)
  source_q_currency_unit = models.CharField('消费项钱款来源 清货币单位(Source_Q_CU)',max_length=200)
  # 自定义的旅行单位日, 一般以到达目的地后的当地时间晚上睡觉为止算第一天, 随后按照当地时间继续一天天推算
  trip_day = models.CharField('旅行自定义天(Trip Day)',max_length=200)
  # 当地的具体时间
  local_date = models.CharField('当地具体日期(Local Day)', max_length=200)

  class Meta:
    verbose_name = '消费项(XMoneyObject)'
    verbose_name_plural = '消费项(XMoneyObject)'
  def __str__(self): #pragma: no cover
    return self.name


