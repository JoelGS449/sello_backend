from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Herramienta, Perfil, Usuario


@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ['nombre']}


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'lista_herramientas']
    filter_horizontal = ['herramientas']

    @admin.display(description='Herramientas')
    def lista_herramientas(self, obj):
        return ', '.join(h.nombre for h in obj.herramientas.all()) or '—'


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'perfil', 'is_active', 'is_staff']
    list_filter = ['perfil', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (('Perfil', {'fields': ['perfil']}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Perfil', {'fields': ['perfil']}),)
