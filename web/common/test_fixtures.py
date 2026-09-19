"""Shared fixtures for queryset performance / behavior tests."""
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from fidouche.models import (
    Expense,
    ExpenseCategory,
    Income,
    Payee,
    Payment,
    ProductionCategory,
    ProductionCompany,
    ProductionPayment,
    Quote,
    SubPayment,
    TaxExpenseCategory,
    TourExpense,
)
from members.models import Member, Sub
from shows.models import Show, Tour, Venue
from songs.models import Setlist, SetlistSong, Song


def create_user(username="tester", password="pass"):
    return User.objects.create_user(username=username, password=password)


def create_venue(name="Test Venue", city="Oakland", state="CA", ltlng="37.8,-122.2"):
    # Always set ltlng so Venue.save does not call Google geocoding.
    return Venue.objects.create(
        venue_name=name, city=city, state=state, ltlng=ltlng
    )


def create_categories():
    tax_cat = TaxExpenseCategory.objects.create(name="Travel")
    tax_prod = TaxExpenseCategory.objects.create(name="Production")
    expense_cat = ExpenseCategory.objects.create(
        category="printing", tax_category=tax_cat
    )
    ads_cat = ExpenseCategory.objects.create(category="ads", tax_category=tax_cat)
    other_cat = ExpenseCategory.objects.create(category="other", tax_category=tax_cat)
    sound_cat = ProductionCategory.objects.create(name="Sound", tax_category=tax_prod)
    iem_cat = ProductionCategory.objects.create(name="IEM", tax_category=tax_prod)
    return {
        "tax_travel": tax_cat,
        "tax_production": tax_prod,
        "printing": expense_cat,
        "ads": ads_cat,
        "other": other_cat,
        "sound": sound_cat,
        "iem": iem_cat,
    }


def build_performance_fixture():
    """
    Build a multi-show fixture sized so N+1s are obvious and totals are fixed.

    Returns a dict of objects used by tests.
    """
    today = date.today()
    year = today.year
    cats = create_categories()
    venue_a = create_venue("Venue A", ltlng="37.8,-122.2")
    venue_b = create_venue("Venue B", ltlng="37.9,-122.3")
    tour = Tour.objects.create(name="Test Tour")
    payee = Payee.objects.create(name="Print Shop")
    company = ProductionCompany.objects.create(name="Sound Co")

    partner = Member.objects.create(
        first_name="Pat",
        last_name="Partner",
        display_first="Pat",
        display_last="Partner",
        active=True,
        partner=True,
        date_partner_joined=date(year - 2, 1, 1),
        section="v",
    )
    non_partner = Member.objects.create(
        first_name="Ned",
        last_name="Nonpartner",
        display_first="Ned",
        display_last="Nonpartner",
        active=True,
        partner=False,
        section="h",
    )
    sub = Sub.objects.create(first_name="Sam", last_name="Sub")

    # Three past shows this year on the tour (played).
    shows = []
    for i, (venue, day) in enumerate(
        [
            (venue_a, datetime(year, 1, 15, 20, 0)),
            (venue_b, datetime(year, 2, 20, 20, 0)),
            (venue_a, datetime(year, 3, 10, 20, 0)),
        ]
    ):
        show = Show.objects.create(
            venue=venue,
            tour=tour,
            date=day,
            public=True,
            gross=Decimal("1000.00") + i * 100,
            net=Decimal("700.00") + i * 50,
            payout=Decimal("50.00") + i,
            commission=Decimal("100.00"),
            to_account=Decimal("25.00"),
            payer="client",
            sound_cost=Decimal("200.00"),
            in_ears_cost=130,
            print_ship_cost=Decimal("10.00"),
            ads_cost=Decimal("20.00"),
            other_cost=Decimal("5.00"),
        )
        shows.append(show)

    # One future show this year (booked, not played).
    future = Show.objects.create(
        venue=venue_a,
        tour=tour,
        date=datetime(year, 12, 15, 20, 0)
        if today.month < 12
        else datetime(year, today.month, min(today.day + 1, 28), 20, 0),
        public=True,
        gross=Decimal("2000.00"),
        net=Decimal("1500.00"),
        payout=Decimal("80.00"),
        commission=Decimal("200.00"),
        payer="client",
    )
    # Ensure future is always after now
    if future.date <= datetime.now():
        future.date = datetime.now() + timedelta(days=14)
        future.save()

    # Prior-year show for YoY / years_with_gigs
    prior = Show.objects.create(
        venue=venue_b,
        date=datetime(year - 1, 6, 1, 20, 0),
        public=True,
        gross=Decimal("500.00"),
        net=Decimal("300.00"),
        payout=Decimal("40.00"),
        payer="agent",
        commission=Decimal("50.00"),
        commission_withheld=True,
    )

    # Itemized production + expenses on first show (overrides legacy fields).
    ProductionPayment.objects.create(
        show=shows[0],
        company=company,
        category=cats["sound"],
        amount=Decimal("150.00"),
        paid=True,
    )
    ProductionPayment.objects.create(
        show=shows[0],
        company=company,
        category=cats["iem"],
        amount=Decimal("80.00"),
        paid=True,
    )
    Expense.objects.create(
        show=shows[0],
        date=shows[0].date.date(),
        payee=payee,
        new_category=cats["printing"],
        amount=Decimal("30.00"),
    )
    Expense.objects.create(
        show=shows[0],
        date=shows[0].date.date(),
        payee=payee,
        new_category=cats["ads"],
        amount=Decimal("40.00"),
    )

    # Tour expenses: $90 across 4 tour shows → share = 22.50
    TourExpense.objects.create(
        tour=tour,
        date=shows[0].date.date(),
        payee=payee,
        category=cats["other"],
        amount=Decimal("90.00"),
    )

    # Payments
    Payment.objects.create(
        show=shows[0], member=partner, amount=Decimal("55.00"), paid=True
    )
    Payment.objects.create(
        show=shows[0], member=non_partner, amount=Decimal("45.00"), paid=True
    )
    Payment.objects.create(
        show=shows[1], member=partner, amount=Decimal("60.00"), paid=True
    )
    SubPayment.objects.create(
        show=shows[1], sub=sub, amount=Decimal("35.00"), paid=True
    )

    Income.objects.create(
        date=shows[0].date.date(), payer="Merch", amount=Decimal("12.00")
    )
    Quote.objects.create(quote="Keep the beat", source="Test")

    # Setter data
    song_a = Song.objects.create(name="Song A", display=True)
    song_b = Song.objects.create(name="Song B", display=True)
    setlist = Setlist.objects.create(show=shows[0])
    SetlistSong.objects.create(setlist=setlist, song=song_a, order=1)
    SetlistSong.objects.create(setlist=setlist, song=song_b, order=2)

    from marketing.models import Testimonial

    Testimonial.objects.create(quote="Great show", featured=True)

    return {
        "year": year,
        "cats": cats,
        "venue_a": venue_a,
        "venue_b": venue_b,
        "tour": tour,
        "shows": shows,
        "future": future,
        "prior": prior,
        "partner": partner,
        "non_partner": non_partner,
        "sub": sub,
        "payee": payee,
        "company": company,
        "setlist": setlist,
        "song_a": song_a,
        "song_b": song_b,
        # Expected totals derived from the fixture formulas
        "expected": {
            # shows[0] itemized production: Sound 150 + IEM 80
            "show0_production": {"Sound": Decimal("150.00"), "IEM": Decimal("80.00")},
            # shows[0] itemized expenses: printing 30 + ads 40 (+ other category empty → 0)
            "show0_expense_printing": Decimal("30.00"),
            "show0_expense_ads": Decimal("40.00"),
            # shows[1] legacy production fallback
            "show1_production": {"Sound": Decimal("200.00"), "IEM": 130},
            # tour: 90 / 4 shows
            "tour_expense_share": Decimal("22.50"),
            # YTD played: shows 0,1,2 (not future)
            "ytd_gross": Decimal("1000") + Decimal("1100") + Decimal("1200"),
            "ytd_net": Decimal("700") + Decimal("750") + Decimal("800"),
            "ytd_payout": Decimal("50") + Decimal("51") + Decimal("52"),
            "ytd_gigs_played": 3,
            "ytd_gigs_booked": 4,  # 3 past + 1 future
            "partner_payment_total": Decimal("55") + Decimal("60"),
            "finance_member_partner_total": Decimal("55") + Decimal("60"),
            "venue_a_show_count": 3,  # shows[0], shows[2], future — wait future also venue_a
            # venue_a: shows[0], shows[2], future = 3; nets only on played with net
        },
    }
