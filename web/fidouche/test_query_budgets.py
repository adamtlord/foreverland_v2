from common.test_fixtures import build_performance_fixture, create_user
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse


class QueryCountBaselineTests(TestCase):
    """Tightened query budgets after queryset optimizations."""

    def setUp(self):
        self.fx = build_performance_fixture()
        create_user(is_staff=True)
        self.client = Client()
        self.client.login(username="tester", password="pass")
        self.year = self.fx["year"]

    def _assert_max_queries(self, max_queries, func):
        with CaptureQueriesContext(connection) as ctx:
            func()
        self.assertLessEqual(
            len(ctx),
            max_queries,
            f"Expected <= {max_queries} queries, got {len(ctx)}:\n"
            + "\n".join(q["sql"][:120] for q in ctx.captured_queries[:40]),
        )

    def test_dashboard_query_budget(self):
        # Was ~64 before optimization.
        self._assert_max_queries(
            25, lambda: self.client.get(reverse("financial_dashboard"))
        )

    def test_gigs_by_year_query_budget(self):
        # Was ~82 before optimization.
        self._assert_max_queries(
            25,
            lambda: self.client.get(
                reverse("gigs_by_year", kwargs={"year": self.year})
            ),
        )

    def test_year_over_year_query_budget(self):
        # Was ~85 before optimization.
        self._assert_max_queries(
            25, lambda: self.client.get(reverse("gigs_year_over_year"))
        )

    def test_venue_map_data_query_budget(self):
        # Was ~9 before optimization.
        self._assert_max_queries(
            5, lambda: self.client.get(reverse("venue_map_data"))
        )

    def test_setter_dashboard_query_budget(self):
        # Was ~9 before optimization.
        self._assert_max_queries(
            10, lambda: self.client.get(reverse("setter_dashboard"))
        )

    def test_tax_reports_query_budget(self):
        # Was ~58 before optimization.
        url = (
            reverse("tax_reports")
            + f"?start_date={self.year}-01-01&end_date={self.year}-12-31"
        )
        self._assert_max_queries(30, lambda: self.client.get(url))

    def test_finance_reports_query_budget(self):
        # Was ~30 before optimization.
        url = (
            reverse("finance_reports")
            + f"?start_date={self.year}-01-01&end_date={self.year}-12-31"
        )
        self._assert_max_queries(15, lambda: self.client.get(url))
