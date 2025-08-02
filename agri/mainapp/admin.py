from django.contrib import admin
from . import models

admin.site.register(models.CropType)
admin.site.register(models.CropImage)
admin.site.register(models.FarmerCrop)
admin.site.register(models.Order)
admin.site.register(models.BuyerProfile)
admin.site.register(models.FarmerProfile)
admin.site.register(models.CropCalendar)
