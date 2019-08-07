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
  # 自定义的旅行单位日, 一般以到达目的地后的当地时间晚上睡觉为止算第一天, 随后按照当地时间继续一天天推算
  trip_day = models.CharField('旅行自定义天(Trip Day)',max_length=200)
  # 当地的具体时间
  local_date = models.CharField('当地具体日期(Local Day)', max_length=200)
  # creator
  created_by = models.CharField('Creator', max_length = 200)
  # updator
  latest_updator = models.CharField('Latest Updator', max_length = 200)
  # image
  image = models.ImageField(upload_to='mo-images/')
  # previous tag
  previous_tag = models.CharField('previous_tag', max_length = 200)

  class Meta:
    verbose_name = '消费项(XMoneyObject)'
    verbose_name_plural = '消费项(XMoneyObject)'
  def __str__(self): #pragma: no cover
    return self.name

class XTripInfo(models.Model):
  object_id = models.AutoField(primary_key = True)
  current_trip_day = models.CharField('current trip day', max_length = 200)
  current_utc = models.CharField('current_utc', max_length = 200)
  class Meta:
    verbose_name="trip basic info"
    verbose_name_plural = 'trip basic info'
  
  def __str__(self):
    return self.current_trip_day

class XUserExInfo(models.Model):
  username = models.CharField('username',max_length=200)
  headportrait = models.ImageField(upload_to='user-head-portraits/')
  previous_tag = models.CharField('previous_tag', max_length = 200)

  class Meta:
    verbose_name = 'UserExtraInformation'
    verbose_name_plural = 'UserExtraInformation'
  def __str__(self): #pragma: no cover
    return self.username

class XCurrency(models.Model):
  # 自增id
  object_id = models.AutoField(primary_key=True)
  name = models.CharField('currency_name', max_length = 200)

  class Meta:
    verbose_name = 'CurrencyList'
    verbose_name_plural = 'CurrencyList'

  def __str__(self): #pragma: no cover
    return self.name