# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("gallery", "0010_set_visibility")]

    operations = [migrations.RemoveField(model_name="basemedia", name="notPublic")]
