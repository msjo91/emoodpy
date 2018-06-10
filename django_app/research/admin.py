from django.contrib import admin

from .models import Institution, Project, ProjGroup

admin.site.register(Institution)
admin.site.register(Project)
admin.site.register(ProjGroup)
