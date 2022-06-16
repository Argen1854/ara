from django.db import models

class PromoCode(models.Model):
    promo_code = models.CharField(max_length=10)

    discount = models.IntegerField()