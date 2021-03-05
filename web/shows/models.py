from decimal import Decimal
from django.db import models
from localflavor.us.models import PhoneNumberField, USStateField

from sorl.thumbnail import ImageField

from common.utils import get_lat_lng


class Venue(models.Model):
    venue_name = models.CharField(max_length=200, blank=True, null=True)
    venue_image = models.ImageField(upload_to="venues/", blank=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default="U.S.A.")
    phone = PhoneNumberField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    ltlng = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["venue_name"]

    def save(self, *args, **kwargs):
        """ Let's get the latlng before we save"""
        super(Venue, self).save(*args, **kwargs)
        if not self.ltlng:
            address = "%s %s %s %s %s %s" % (
                self.venue_name,
                self.address1,
                self.address2,
                self.city,
                self.state,
                self.zip_code,
            )
            try:
                self.ltlng = get_lat_lng(address)
            except Exception:
                raise Exception
            super(Venue, self).save(*args, **kwargs)

    @property
    def first_show(self):
        shows = self.shows.all().order_by("date")
        return int(shows[0].date.strftime("%s"))

    @property
    def first_show_year(self):
        shows = self.shows.all().order_by("date")
        return shows[0].date.strftime("%Y")

    def __str__(self):
        return self.venue_name


class Tour(models.Model):
    """ A collection of shows, ie, Speed of Sound """

    name = models.CharField(max_length=200, blank=True, null=True)

    @property
    def shows(self):
        return self.show_in_tour.all().order_by("date")

    @property
    def cities(self):
        shows = self.shows
        if shows:
            cities = []
            for show in shows:
                location = show.venue.city + " " + show.venue.state
                if location not in cities:
                    cities.append(location)
            return cities
        else:
            return []

    @property
    def venue_ltlngs(self):
        shows = self.shows
        if shows:
            points = []
            for show in shows:
                if show.venue.ltlng not in points:
                    points.append(show.venue.ltlng)
            return points
        else:
            return []

    @property
    def gross(self):
        return sum([show.gross for show in self.shows if show.gross])

    @property
    def net(self):
        return self.gross - self.all_expenses

    @property
    def date_range(self):
        shows = self.shows
        if shows:
            first_date = min([show.date for show in shows])
            last_date = max([show.date for show in shows])
            return "%s - %s" % (
                first_date.strftime("%m/%d/%y"),
                last_date.strftime("%m/%d/%y"),
            )
        else:
            return None

    @property
    def expenses(self):
        from fidouche.models import TourExpense

        expenses = TourExpense.objects.filter(tour=self)
        if expenses:
            return sum([expense.amount for expense in expenses])
        else:
            return 0

    @property
    def all_expenses(self):
        show_costs = sum([show.get_show_costs() for show in self.shows])
        return show_costs + self.expenses

    @property
    def expense_share(self):
        shows = self.shows
        expenses = self.expenses
        if shows and expenses:
            return Decimal("%.2f" % (expenses / len(shows)))
        else:
            return 0

    def __str__(self):
        return self.name


class Show(models.Model):
    # Open to the public/Display on public calendar?
    public = models.BooleanField(default=True)
    # Public Information
    venue = models.ForeignKey(Venue, related_name="shows", on_delete=models.CASCADE)
    date = models.DateTimeField()
    tour = models.ForeignKey(
        Tour,
        related_name="show_in_tour",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    doors_time = models.TimeField(blank=True, null=True)
    ticket_price = models.CharField(max_length=100, blank=True, null=True)
    ticket_url = models.URLField(max_length=200, blank=True, null=True)
    ages = models.CharField(max_length=100, blank=True, null=True)
    opener = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    poster = models.FileField(upload_to="posters/", blank=True, null=True)
    fb_event = models.CharField(max_length=200, blank=True, null=True)
    # Financial Information
    AGENT = "agent"
    CLIENT = "client"
    CASH = "cash"
    CHECK = "check"
    PAYER_CHOICES = (
        (CLIENT, "Client"),
        (AGENT, "Agent"),
    )
    METHOD_CHOICES = (
        (CASH, "Cash"),
        (CHECK, "Check"),
    )
    IEM_CHOICES = (
        (80, "$80"),
        (130, "$130"),
    )
    attendance = models.IntegerField(blank=True, null=True)
    gross = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gross_itemized = models.BooleanField(default=False)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    food_buyout = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    travel_buyout = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    lodging_buyout = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    other_buyout = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    gross_method = models.CharField(
        max_length=100, blank=True, null=True, choices=METHOD_CHOICES
    )
    payer = models.CharField(
        max_length=100, blank=True, null=True, choices=PAYER_CHOICES
    )
    payee_check_no = models.IntegerField(blank=True, null=True)
    commission = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    agent = models.ForeignKey(
        "fidouche.Agent",
        related_name="gig_agent",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    commission_withheld = models.BooleanField(default=False)
    commission_percentage = models.IntegerField(default=10, blank=True, null=True)
    commission_check_no = models.IntegerField(blank=True, null=True)
    commission_paid = models.BooleanField(default=False)
    sound_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    sound_check_no = models.IntegerField(blank=True, null=True)
    in_ears_cost = models.IntegerField(
        blank=True, null=True, choices=IEM_CHOICES, default=130
    )
    in_ears_check_no = models.IntegerField(blank=True, null=True)
    costs_itemized = models.BooleanField(default=False)
    print_ship_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    ads_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    other_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    net = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    to_account = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    subs = models.BooleanField(default=False)
    settlement_sheet = ImageField(upload_to="receipts/", blank=True, null=True)
    payout_notes = models.TextField(null=True, blank=True)

    def get_production_costs(self):
        d = {}
        from fidouche.models import ProductionPayment, ProductionCategory

        production_expenses = list(
            ProductionPayment.objects.filter(show=self).select_related("category")
        )
        production_categories = ProductionCategory.objects.all()
        if production_expenses:
            for category in production_categories:
                d[category.name] = []
            for expense in production_expenses:
                try:
                    d[expense.category.name].append(expense.amount)
                except Exception:
                    pass
            for k in d:
                d[k] = sum(d[k])
        else:
            sound = self.sound_cost or 0
            iem = self.in_ears_cost or 0
            d["Sound"] = sound
            d["IEM"] = iem
        return d

    def get_expenses(self):
        d = {}
        from fidouche.models import Expense, ExpenseCategory

        expenses = list(
            Expense.objects.filter(show=self).select_related("new_category")
        )
        expense_categories = ExpenseCategory.objects.all()
        for category in expense_categories:
            d[category.category] = []
        if expenses:
            for expense in expenses:
                d[expense.new_category.category].append(expense.amount)
        else:
            d["printing"] = self.print_ship_cost or 0
            d["ads"] = self.ads_cost or 0
            d["other"] = self.other_cost or 0
        for k in d:
            if type(d[k]) is list:
                d[k] = sum(d[k])
        return d

    def get_show_costs(self):
        production_costs = self.get_production_costs()
        production = []
        for k in production_costs:
            production.append(production_costs[k])
        production = sum(production)
        expense_costs = self.get_expenses()
        expenses = []
        for k in expense_costs:
            if type(expense_costs[k]) is list:
                expenses.append(sum(expense_costs[k]))
            else:
                expenses.append(expense_costs[k])
        expenses = sum(expenses)
        commission = self.commission if self.commission else 0
        return production + expenses + commission

    def get_total_costs(self):
        tour_costs = self.tour.expense_share if self.tour else 0

        return self.get_show_costs() + tour_costs

    def get_tour_costs(self):
        d = {}
        if self.tour:
            d["Tour Costs"] = self.tour.expense_share
        return d

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return "%s %s" % (self.date.strftime("%m/%d/%y"), self.venue)
