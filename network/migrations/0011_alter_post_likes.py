# Generated by Django 4.0.2 on 2022-04-17 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_post_likes_alter_likes_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totol_likes', to='network.likes'),
        ),
    ]