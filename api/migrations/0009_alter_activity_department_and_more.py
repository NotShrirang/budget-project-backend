# Generated by Django 4.1.4 on 2023-10-02 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_department_isactive_transaction_isactive"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="activities",
                to="api.department",
            ),
        ),
        migrations.AlterField(
            model_name="collegeuser",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="users",
                to="api.department",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="activity",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="transactions",
                to="api.activity",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="transactions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
