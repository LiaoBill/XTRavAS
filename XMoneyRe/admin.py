from django.contrib import admin

# Register your models here.
from .models import XMoneyObj, XUserExInfo, XTripInfo, XCurrency

admin.site.register(XMoneyObj)
admin.site.register(XUserExInfo)
admin.site.register(XTripInfo)
admin.site.register(XCurrency)