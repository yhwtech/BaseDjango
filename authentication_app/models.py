from django.db import models
from tenant_schemas.models import TenantMixin
from tenant_schemas.postgresql_backend.base import _check_schema_name
from django.utils.translation import gettext_lazy as _

class Client(TenantMixin):
    domain_url = models.CharField(max_length=128, unique=True,verbose_name=_("Url Dominio"))
    schema_name = models.CharField(max_length=63, unique=True,verbose_name=_("Esquema"),
                                   validators=[_check_schema_name])
    nit = models.CharField(max_length=100, verbose_name=_('nit'))
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    on_trial = models.BooleanField(default=False, verbose_name=_('Versión prueba'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha creación'))
    auto_created_schema = True

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def __str__(self):
        return f'{self.nit} | {self.name} | {self.created_on}'


class License(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    license_key = models.CharField(max_length=255, unique=True,verbose_name=_("Clave"))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("creada en"))
    expires_on = models.DateTimeField(verbose_name=_("Expira en"))

    class Meta:
        verbose_name = _('Licencia')
        verbose_name_plural = _('Licencias')

    def __str__(self):
        return f'License {self.license_key} for {self.client.name}'