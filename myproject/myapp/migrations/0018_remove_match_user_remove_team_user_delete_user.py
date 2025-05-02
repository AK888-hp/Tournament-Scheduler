# Generated migration file
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        # Any previous migrations
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='name',
            new_name='player_name',
        ),
    ]
