from decimal import Decimal

from common.test_fixtures import build_performance_fixture
from django.test import TestCase
from shows.models import Show


class CostHelperTests(TestCase):
    def setUp(self):
        self.fx = build_performance_fixture()
        self.show0 = self.fx["shows"][0]
        self.show1 = self.fx["shows"][1]
        self.tour = self.fx["tour"]

    def test_itemized_production_costs(self):
        costs = self.show0.get_production_costs()
        self.assertEqual(costs["Sound"], Decimal("150.00"))
        self.assertEqual(costs["IEM"], Decimal("80.00"))

    def test_legacy_production_fallback(self):
        costs = self.show1.get_production_costs()
        self.assertEqual(costs["Sound"], Decimal("200.00"))
        self.assertEqual(costs["IEM"], 130)

    def test_itemized_expenses(self):
        costs = self.show0.get_expenses()
        self.assertEqual(costs["printing"], Decimal("30.00"))
        self.assertEqual(costs["ads"], Decimal("40.00"))
        self.assertEqual(costs["other"], 0)

    def test_legacy_expense_fallback(self):
        costs = self.show1.get_expenses()
        self.assertEqual(costs["printing"], Decimal("10.00"))
        self.assertEqual(costs["ads"], Decimal("20.00"))
        self.assertEqual(costs["other"], Decimal("5.00"))

    def test_tour_expense_share(self):
        self.assertEqual(self.tour.expense_share, Decimal("22.50"))

    def test_show_costs_include_commission(self):
        # production 230 + expenses 70 + commission 100 = 400
        self.assertEqual(self.show0.get_show_costs(), Decimal("400.00"))

    def test_total_costs_include_tour_share(self):
        # show costs 400 + tour share 22.50
        self.assertEqual(self.show0.get_total_costs(), Decimal("422.50"))

    def test_tour_costs_dict(self):
        self.assertEqual(
            self.show0.get_tour_costs(), {"Tour Costs": Decimal("22.50")}
        )

    def test_show_without_tour_has_no_tour_share(self):
        prior = self.fx["prior"]
        self.assertEqual(prior.get_tour_costs(), {})
        # legacy production + expenses + commission
        # Sound 0 (null→0) + IEM default 130 + printing/ads/other 0 + commission 50
        total = prior.get_total_costs()
        self.assertEqual(total, prior.get_show_costs())
