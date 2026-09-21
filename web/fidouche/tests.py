import json
from decimal import Decimal

from common.context_processors import list_years_with_gigs, random_quote
from common.test_fixtures import build_performance_fixture, create_user
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse


class FidoucheViewBehaviorTests(TestCase):
    def setUp(self):
        self.fx = build_performance_fixture()
        self.user = create_user(is_staff=True)
        self.client = Client()
        self.client.login(username="tester", password="pass")
        self.year = self.fx["year"]

    def test_financial_dashboard_ytd(self):
        response = self.client.get(reverse("financial_dashboard"))
        self.assertEqual(response.status_code, 200)
        ytd = response.context["ytd"]
        self.assertEqual(ytd["gigs_played"], self.fx["expected"]["ytd_gigs_played"])
        self.assertEqual(ytd["gigs_booked"], self.fx["expected"]["ytd_gigs_booked"])
        self.assertEqual(ytd["gross"], self.fx["expected"]["ytd_gross"])
        self.assertEqual(ytd["net"], self.fx["expected"]["ytd_net"])
        self.assertEqual(ytd["payout"], self.fx["expected"]["ytd_payout"])

    def test_gigs_by_year_totals(self):
        response = self.client.get(
            reverse("gigs_by_year", kwargs={"year": self.year})
        )
        self.assertEqual(response.status_code, 200)
        # Current year filters to past shows only → 3 played
        self.assertEqual(response.context["gigs_played"], 3)
        self.assertEqual(response.context["gross"], self.fx["expected"]["ytd_gross"])
        self.assertEqual(response.context["net"], self.fx["expected"]["ytd_net"])
        # payments on show0 (55+45) + show1 (60) + show2 fallback payout*14
        expected_players = (
            Decimal("55")
            + Decimal("45")
            + Decimal("60")
            + (Decimal("52") * 14)
        )
        self.assertEqual(response.context["players"], expected_players)
        self.assertEqual(response.context["by_month"][1]["count"], 1)
        self.assertEqual(response.context["by_month"][2]["count"], 1)
        self.assertEqual(response.context["by_month"][3]["count"], 1)

    def test_gigs_year_over_year(self):
        response = self.client.get(reverse("gigs_year_over_year"))
        self.assertEqual(response.status_code, 200)
        years = response.context["years"]
        self.assertIn(self.year, years)
        self.assertIn(self.year - 1, years)
        self.assertEqual(years[self.year]["gigs_played"], 4)  # all shows this year
        self.assertEqual(
            years[self.year - 1]["gross"], Decimal("500.00")
        )

    def test_finance_reports(self):
        start = f"{self.year}-01-01"
        end = f"{self.year}-12-31"
        response = self.client.get(
            reverse("finance_reports"), {"start_date": start, "end_date": end}
        )
        self.assertEqual(response.status_code, 200)
        member_payments = response.context["member_payments"]
        partner = self.fx["partner"]
        self.assertEqual(
            member_payments[partner]["total"],
            self.fx["expected"]["finance_member_partner_total"],
        )

    def test_tax_reports_partner_total(self):
        start = f"{self.year}-01-01"
        end = f"{self.year}-12-31"
        response = self.client.get(
            reverse("tax_reports"), {"start_date": start, "end_date": end}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["partner_total"],
            self.fx["expected"]["partner_payment_total"],
        )
        self.assertEqual(
            response.context["total_other_income"], Decimal("12.00")
        )

    def test_venue_map_data(self):
        response = self.client.get(reverse("venue_map_data"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        by_name = {v["name"]: v for v in data}
        self.assertIn("Venue A", by_name)
        venue_a = by_name["Venue A"]
        # shows[0], shows[2], future
        self.assertEqual(venue_a["num_shows"], 3)
        self.assertEqual(venue_a["first_show_year"], str(self.year))
        # net from shows with net: 700 + 800 (+ future 1500)
        self.assertEqual(venue_a["net"], 700 + 800 + 1500)


class ContextProcessorTests(TestCase):
    def setUp(self):
        self.fx = build_performance_fixture()
        self.factory = RequestFactory()

    def test_active_years_is_eager_list(self):
        request = self.factory.get("/")
        ctx = list_years_with_gigs(request)
        years = ctx["active_years"]
        self.assertIsInstance(years, list)
        self.assertFalse(callable(years))
        self.assertIn(self.fx["year"], years)
        self.assertIn(self.fx["year"] - 1, years)

    def test_random_quote_returns_featured(self):
        request = self.factory.get("/")
        ctx = random_quote(request)
        self.assertIsNotNone(ctx["random_quote"])
        self.assertEqual(ctx["random_quote"].quote, "Great show")


class FidoucheStaffGateTests(TestCase):
    def setUp(self):
        self.fx = build_performance_fixture()
        create_user(username="member", password="pass", is_staff=False)
        self.client = Client()
        self.client.login(username="member", password="pass")

    def test_non_staff_cannot_read_dashboard(self):
        response = self.client.get(reverse("financial_dashboard"))
        self.assertIn(response.status_code, (302, 403))
        if response.status_code == 302:
            self.assertTrue(
                "/accounts/login" in response.url or "/admin/login" in response.url
            )

    def test_non_staff_cannot_read_tax_reports(self):
        response = self.client.get(reverse("tax_reports"))
        self.assertIn(response.status_code, (302, 403))
        if response.status_code == 302:
            self.assertTrue(
                "/accounts/login" in response.url or "/admin/login" in response.url
            )

    def test_anonymous_cannot_read_dashboard(self):
        anon = Client()
        response = anon.get(reverse("financial_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            "/accounts/login" in response.url or "/admin/login" in response.url
        )


class SetterViewTests(TestCase):
    def setUp(self):
        self.fx = build_performance_fixture()
        self.user = create_user()
        self.client = Client()
        self.client.login(username="tester", password="pass")

    def test_setter_dashboard(self):
        response = self.client.get(reverse("setter_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Song A")
        self.assertContains(response, "2 songs")

    def test_view_setlist(self):
        response = self.client.get(
            reverse("view_setlist", kwargs={"gig_id": self.fx["shows"][0].id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Song A")
        self.assertContains(response, "Song B")
