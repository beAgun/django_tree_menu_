# Generated by Django 4.2.1 on 2024-04-13 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tree_menu', '0002_alter_menu_options_menu_root'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='root',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tree_menu.menu', verbose_name='Корень/название меню'),
        ),
    ]
