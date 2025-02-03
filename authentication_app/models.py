from django.db import models
from tenant_schemas.models import TenantMixin


class Client(TenantMixin):
    nit = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    auto_created_schema = True

    def __str__(self):
        return f'{self.nit} | {self.name} | {self.created_on}'


class License(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=255, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField()

    def __str__(self):
        return f'License {self.license_key} for {self.client.name}'