# Generated by Django 4.1.4 on 2023-09-24 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_transaction_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="file",
            field=models.ImageField(
                blank=True, null=True, upload_to="transaction_files/"
            ),
        ),
    ]