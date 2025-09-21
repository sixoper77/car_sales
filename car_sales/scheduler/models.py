from django.db import models

class ExchangeRate(models.Model):
    currency=models.CharField(max_length=10)
    rate=models.DecimalField(max_digits=10,decimal_places=4)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.currency}:{self.rate}"
