from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Prefetch
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from tenant_schemas.utils import schema_context

from authentication_app.models import Client, License

admin.site.register(Client)
admin.site.register(License)

import logging
new_schema_name = None

logger = logging.getLogger(__name__)
@receiver(post_save , sender=Client)
def create_auth_groups(sender, instance, created, **kwargs):
    if created:
        global new_schema_name
        new_schema_name = instance.schema_name
        logger.info("Se crea nuevo schema")


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    global new_schema_name
    if sender.name == 'django.contrib.auth' and new_schema_name is not None:
        try:
            with schema_context('public'):
                groups=list(Group.objects.prefetch_related(Prefetch('permissions')).all())

            for group in groups:
                with schema_context(new_schema_name):
                    new_group, created = Group.objects.get_or_create(name=group.name)
                    for permission in group.permissions.all():
                        new_group.permissions.add(permission)
        except Exception as e:
            logger.error("Error al crear grupos en el schema %s: %s", new_schema_name, str(e))
        finally:
            new_schema_name = None


