from django.db import models
from django.contrib.auth.models import User


class Vendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class CreditReport(models.Model):
    lc_number = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    beneficiary_name = models.CharField(max_length=255)
    beneficiary_address = models.TextField()
    beneficiary_country = models.CharField(max_length=255)
    expiry_date = models.DateField()
    credit_risk = models.CharField(max_length=100)
    related_party = models.CharField(max_length=100)
    line_of_business = models.CharField(max_length=100)
    #vendor_name = models.CharField(max_length=255)
    vendor_name = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)  # current date/time
    entry_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    document = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"{self.lc_number} - {self.client_name}"

class RequestedReport(models.Model):
    lc_number = models.CharField(max_length=100)
    client_name = models.CharField(max_length=255)
    beneficiary_name = models.CharField(max_length=255)
    beneficiary_address = models.TextField()
    beneficiary_country = models.CharField(max_length=255)
    related_party = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=255)
    request_date = models.DateTimeField(auto_now_add=True)  # current date/time
    request_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.beneficiary_name} - {self.beneficiary_country}"
