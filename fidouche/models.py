from django.db import models

from localflavor.us.models import PhoneNumberField, USStateField

from members.models import Member, Sub
from shows.models import Show, Tour


class Payment(models.Model):
    show = models.ForeignKey(Show, related_name="payment", null=True)
    member = models.ForeignKey(Member, related_name="payment", null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        unique_together = (('show', 'member'),)
        ordering = ['show__date']

    def __unicode__(self):
        payee = str(self.member.display_first) if self.member else '',
        show = str(self.show.venue) if self.show.venue else '',
        date = self.show.date.strftime('%m/%d/%y') if self.show else '',
        return '%s for %s on %s' % (payee[0], show[0], date[0])


class SubPayment(models.Model):
    show = models.ForeignKey(Show, related_name="subpayment", blank=True, null=True)
    sub = models.ForeignKey(Sub, related_name="sub", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        unique_together = (('show', 'sub'),)

    def __unicode__(self):
        return '%s for %s on %s' % (self.sub.first_name, self.show.venue, self.show.date.strftime('%m/%d/%y'))


class Payee(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Zip", max_length=20, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    ssn = models.CharField(verbose_name="SSN#", max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name


class TaxExpenseCategory(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tax Expense Categories"


class ExpenseCategory(models.Model):
    category = models.CharField(max_length=100, blank=True, null=True)
    tax_category = models.ForeignKey(TaxExpenseCategory, related_name="expense_category", blank=True, null=True)

    def __unicode__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Expense Categories"


class Expense(models.Model):

    show = models.ForeignKey(Show, related_name="expense", blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    payee = models.ForeignKey(Payee, related_name="expense", blank=True, null=True)
    new_category = models.ForeignKey(ExpenseCategory, related_name="expense_category", blank=True, null=True, verbose_name="Category")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    check_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Check #")
    notes = models.TextField(blank=True, null=True)
    receipt_img = models.FileField(upload_to="receipts/", blank=True, null=True)

    @property
    def filetype(self):
        if self.receipt_img:
            return self.receipt_img.name[-3:]
        else:
            return None

    def __unicode__(self):
        safedate = ''
        if self.date:
            safedate = self.date.strftime('%m/%d/%y') + ', '
        return '%s$%s to %s' % (safedate, self.amount, self.payee)


class TourExpense(models.Model):

    tour = models.ForeignKey(Tour, blank=True, null=True)
    date = models.DateField(blank=True, null=True, verbose_name="Expense Date")
    payee = models.ForeignKey(Payee, blank=True, null=True)
    category = models.ForeignKey(ExpenseCategory, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    check_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Check #")
    notes = models.TextField(blank=True, null=True)
    receipt_img = models.FileField(upload_to="receipts/", blank=True, null=True)

    @property
    def filetype(self):
        if self.receipt_img:
            return self.receipt_img.name[-3:]
        else:
            return None

    @property
    def new_category(self):
        return self.category

    def __unicode__(self):
        safedate = ''
        if self.date:
            safedate = self.date.strftime('%m/%d/%y') + ', '
        return '%s$%s to %s' % (safedate, self.amount, self.payee)


class Income(models.Model):

    date = models.DateField(blank=True, null=True)
    payer = models.CharField(blank=True, null=True, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    check_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Check #")
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        safedate = ''
        if self.date:
            safedate = self.date.strftime('%m/%d/%y') + ', '
        return '%s$%s to %s' % (safedate, self.amount, self.payee)


class Quote(models.Model):

    quote = models.TextField()
    source = models.CharField(max_length=128, blank=True, null=True)
    occasion = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return '%s...' % self.quote[0:64]


class Agent(models.Model):

    name = models.CharField(max_length=128)
    agency = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Zip", max_length=20, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    ssn = models.CharField(verbose_name="SSN/EIN", max_length=16, blank=True, null=True)

    def __unicode__(self):
        agency = ', %s' % self.agency if self.agency else ''
        return '%s%s' % (self.name, agency)


class CommissionPayment(models.Model):
    show = models.ForeignKey(Show, related_name="commission_payment", blank=True, null=True)
    agent = models.ForeignKey(Agent, related_name="commission_payment", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    check_no = models.IntegerField(blank=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        unique_together = (('show', 'agent'),)
        ordering = ['-show__date']

    def __unicode__(self):
        agent = str(self.agent.name) if self.agent else '',
        show = str(self.show.venue) if self.show.venue else '',
        date = self.show.date.strftime('%m/%d/%y') if self.show else '',
        return '%s for %s on %s' % (agent[0], show[0], date[0])


class ProductionCompany(models.Model):

    name = models.CharField(max_length=128)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(verbose_name="Zip", max_length=20, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    ssn = models.CharField(verbose_name="SSN/EIN", max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Production companies'


class ProductionCategory(models.Model):
    name = models.CharField(max_length=128)
    tax_category = models.ForeignKey(TaxExpenseCategory, related_name="production_category", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Production categories'


class ProductionPayment(models.Model):
    show = models.ForeignKey(Show, related_name="production_payment", blank=True, null=True)
    company = models.ForeignKey(ProductionCompany, related_name="production_payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    check_no = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(ProductionCategory, blank=True, null=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['show__date']

    def __unicode__(self):
        company = str(self.company.name) if self.company else ''
        show = self.show
        cat = self.category
        return '%s for %s (%s)' % (company, show, cat)

    @property
    def payee(self):
        return self.company

    @property
    def new_category(self):
        return self.category
