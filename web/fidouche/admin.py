from common.admin import MaskedSSNAdmin
from django.contrib import admin
from fidouche.models import (Agent, CommissionPayment, ExpenseCategory,
                             Fiduciary, FiduciaryPayment, Payee, Payment,
                             ProductionCategory, ProductionCompany,
                             ProductionPayment, Quote, SubPayment,
                             TaxExpenseCategory, TourExpense)

admin.site.register(Payment)
admin.site.register(SubPayment)
admin.site.register(Payee, MaskedSSNAdmin)
admin.site.register(TourExpense)
admin.site.register(ExpenseCategory)
admin.site.register(TaxExpenseCategory)
admin.site.register(Quote)
admin.site.register(Agent, MaskedSSNAdmin)
admin.site.register(CommissionPayment)
admin.site.register(ProductionCompany, MaskedSSNAdmin)
admin.site.register(ProductionCategory)
admin.site.register(ProductionPayment)
admin.site.register(Fiduciary, MaskedSSNAdmin)
admin.site.register(FiduciaryPayment)
