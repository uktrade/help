from __future__ import unicode_literals

from django.db import migrations


def delete_triage(apps, schema_editor):
    TriageModel = apps.get_model('contact', 'TriageModel')
    TriageModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(delete_triage, migrations.RunPython.noop)
    ]
