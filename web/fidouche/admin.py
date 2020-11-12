from django.contrib import admin
from fidouche.models import (
    Payment,
    SubPayment,
    Payee,
    TourExpense,
    ExpenseCategory,
    TaxExpenseCategory,
    Quote,
    Agent,
    CommissionPayment,
    ProductionCompany,
    ProductionCategory,
    ProductionPayment,
    Fiduciary,
    FiduciaryPayment,
)


admin.site.register(Payment)
admin.site.register(SubPayment)
admin.site.register(Payee)
admin.site.register(TourExpense)
admin.site.register(ExpenseCategory)
admin.site.register(TaxExpenseCategory)
admin.site.register(Quote)
admin.site.register(Agent)
admin.site.register(CommissionPayment)
admin.site.register(ProductionCompany)
admin.site.register(ProductionCategory)
admin.site.register(ProductionPayment)
admin.site.register(Fiduciary)
admin.site.register(FiduciaryPayment)
