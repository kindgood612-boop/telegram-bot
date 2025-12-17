# handlers/__init__.py

from handlers.admin.roles import register as admin_roles
from handlers.admin.moderation import register as admin_moderation
from handlers.admin.locks import register as admin_locks

from handlers.developer.dev_roles import register as dev_roles

def register_handlers(dp):
    admin_roles(dp)
    admin_moderation(dp)
    admin_locks(dp)
    dev_roles(dp)
