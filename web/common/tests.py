import os
from decimal import Decimal

from common.admin import can_view_ssn, mask_ssn
from common.test_fixtures import build_performance_fixture, create_user
from common.uploads import receipt_upload_to, validate_receipt_file
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from fidouche.models import Expense
from foreverland.settings.env import env_bool, require_allowed_hosts, require_secret_key
from members.models import Member


class SettingsFailClosedTests(TestCase):
    def test_env_bool_accepts_true_strings(self):
        with override_settings():
            os.environ["DEBUG"] = "true"
            self.assertTrue(env_bool("DEBUG", "0"))
            os.environ["DEBUG"] = "0"
            self.assertFalse(env_bool("DEBUG", "1"))

    def test_empty_secret_key_refuses_to_boot(self):
        old = os.environ.get("SECRET_KEY")
        os.environ["SECRET_KEY"] = ""
        try:
            with self.assertRaises(ImproperlyConfigured):
                require_secret_key()
        finally:
            if old is None:
                os.environ.pop("SECRET_KEY", None)
            else:
                os.environ["SECRET_KEY"] = old

    def test_missing_allowed_hosts_refuses_to_boot(self):
        old = os.environ.get("DJANGO_ALLOWED_HOSTS")
        os.environ.pop("DJANGO_ALLOWED_HOSTS", None)
        try:
            with self.assertRaises(ImproperlyConfigured):
                require_allowed_hosts()
        finally:
            if old is not None:
                os.environ["DJANGO_ALLOWED_HOSTS"] = old


class SSNEncryptionTests(TestCase):
    def test_ssn_is_ciphertext_in_db(self):
        member = Member.objects.create(
            first_name="Pat", last_name="Partner", ssn="123-45-6789", active=True
        )
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ssn FROM members_member WHERE id = %s", [member.id]
            )
            raw = cursor.fetchone()[0]
        self.assertNotEqual(raw, "123-45-6789")
        self.assertNotIn("123-45-6789", raw)
        self.assertNotIn("###-##-####", raw or "")
        member.refresh_from_db()
        self.assertEqual(member.ssn, "123-45-6789")

    def test_legacy_plaintext_still_reads(self):
        member = Member.objects.create(first_name="Lee", last_name="Legacy", active=True)
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE members_member SET ssn = %s WHERE id = %s",
                ["987-65-4321", member.id],
            )
        member.refresh_from_db()
        self.assertEqual(member.ssn, "987-65-4321")

    def test_mask_and_reveal_rules(self):
        self.assertEqual(mask_ssn("123-45-6789"), "•••-••-6789")
        staff = create_user(username="staffer", is_staff=True)
        self.assertFalse(can_view_ssn(staff))
        superuser = User.objects.create_superuser(
            "boss", "boss@example.com", "pass"
        )
        self.assertTrue(can_view_ssn(superuser))


class ReceiptPrivacyTests(TestCase):
    def setUp(self):
        self.fx = build_performance_fixture()
        self.expense = Expense.objects.create(
            show=self.fx["shows"][0],
            amount=Decimal("10.00"),
        )
        self.expense.receipt_img.save(
            "check.pdf", ContentFile(b"%PDF-1.4 staff-only"), save=True
        )
        self.filename = self.expense.receipt_img.name.split("receipts/", 1)[-1]

    def test_anonymous_receipt_is_denied(self):
        client = Client()
        response = client.get(
            reverse("private_receipt_media", kwargs={"filename": self.filename})
        )
        self.assertIn(response.status_code, (302, 403))
        if response.status_code == 302:
            self.assertTrue(
                "/accounts/login" in response.url or "/admin/login" in response.url
            )

    def test_non_staff_receipt_is_denied(self):
        create_user(username="member", password="pass", is_staff=False)
        client = Client()
        client.login(username="member", password="pass")
        response = client.get(
            reverse("private_receipt_media", kwargs={"filename": self.filename})
        )
        self.assertIn(response.status_code, (302, 403))

    def test_staff_can_download_receipt(self):
        create_user(is_staff=True)
        client = Client()
        client.login(username="tester", password="pass")
        response = client.get(
            reverse("private_receipt", kwargs={"filename": self.filename})
        )
        self.assertEqual(response.status_code, 200)

    def test_path_traversal_is_404(self):
        create_user(is_staff=True)
        client = Client()
        client.login(username="tester", password="pass")
        response = client.get(
            reverse("private_receipt", kwargs={"filename": "../settings.py"})
        )
        self.assertEqual(response.status_code, 404)

    def test_receipt_upload_rejects_executables(self):
        uploaded = SimpleUploadedFile(
            "payload.exe", b"MZ", content_type="application/octet-stream"
        )
        self.assertIsNotNone(validate_receipt_file(uploaded))
        self.assertTrue(receipt_upload_to(None, "scan.pdf").startswith("receipts/"))


class LoginRateLimitTests(TestCase):
    def test_rapid_login_posts_lock_out(self):
        client = Client()
        for _ in range(10):
            client.post(
                "/accounts/login/", {"username": "nope", "password": "wrong"}
            )
        response = client.post(
            "/accounts/login/", {"username": "nope", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 429)

    def test_password_reset_form_renders(self):
        response = Client().get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)


class PastShowsAndXssTests(TestCase):
    def setUp(self):
        self.fx = build_performance_fixture()
        show = self.fx["shows"][0]
        show.notes = '<script>alert("xss")</script>\nsecond line'
        show.save(update_fields=["notes"])

    def test_past_shows_defaults_to_latest_year(self):
        response = Client().get(reverse("past_shows"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_year"], self.fx["year"])
        self.assertEqual(list(response.context["shows_by_year"].keys()), [self.fx["year"]])

    def test_script_in_notes_is_escaped(self):
        response = Client().get(reverse("past_shows"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<script>alert")
        self.assertContains(response, "&lt;script&gt;")
