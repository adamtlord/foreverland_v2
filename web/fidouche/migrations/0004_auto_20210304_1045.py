# Generated by Django 3.0 on 2021-03-04 10:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "__first__"),
        ("shows", "__first__"),
        ("fidouche", "0003_auto_20201021_0956"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commissionpayment",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="commission_payment",
                to="fidouche.Agent",
            ),
        ),
        migrations.AlterField(
            model_name="commissionpayment",
            name="show",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="commission_payment",
                to="shows.Show",
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="new_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="expense_category",
                to="fidouche.ExpenseCategory",
                verbose_name="Category",
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="payee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="expense",
                to="fidouche.Payee",
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="show",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="expense",
                to="shows.Show",
            ),
        ),
        migrations.AlterField(
            model_name="expensecategory",
            name="tax_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="expense_category",
                to="fidouche.TaxExpenseCategory",
            ),
        ),
        migrations.AlterField(
            model_name="fiduciarypayment",
            name="show",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="fiduciary_payment",
                to="shows.Show",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="member",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="payment",
                to="members.Member",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="show",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="payment",
                to="shows.Show",
            ),
        ),
        migrations.AlterField(
            model_name="productioncategory",
            name="tax_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="production_category",
                to="fidouche.TaxExpenseCategory",
            ),
        ),
        migrations.AlterField(
            model_name="productionpayment",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="fidouche.ProductionCategory",
            ),
        ),
        migrations.AlterField(
            model_name="productionpayment",
            name="show",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="production_payment",
                to="shows.Show",
            ),
        ),
        migrations.AlterField(
            model_name="subpayment",
            name="show",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subpayment",
                to="shows.Show",
            ),
        ),
        migrations.AlterField(
            model_name="subpayment",
            name="sub",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sub",
                to="members.Sub",
            ),
        ),
        migrations.AlterField(
            model_name="tourexpense",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="fidouche.ExpenseCategory",
            ),
        ),
        migrations.AlterField(
            model_name="tourexpense",
            name="payee",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="fidouche.Payee",
            ),
        ),
        migrations.AlterField(
            model_name="tourexpense",
            name="tour",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="shows.Tour",
            ),
        ),
    ]
