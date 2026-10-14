from django.db import migrations

HERRAMIENTAS = [('marca', 'Marca de agua'), ('ocr', 'Texto de documentos')]


def crear(apps, schema_editor):
    Herramienta = apps.get_model('cuentas', 'Herramienta')
    for slug, nombre in HERRAMIENTAS:
        Herramienta.objects.get_or_create(slug=slug, defaults={'nombre': nombre})


class Migration(migrations.Migration):
    dependencies = [('cuentas', '0001_initial')]

    operations = [migrations.RunPython(crear, migrations.RunPython.noop)]
