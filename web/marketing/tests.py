from django.test import Client, TestCase
from django.urls import reverse
from marketing.models import Testimonial


class AboutPageTests(TestCase):
    def test_about_renders_testimonials(self):
        Testimonial.objects.create(quote="Foreverland BLEW ME AWAY!", featured=True)
        response = Client().get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Foreverland BLEW ME AWAY!")
        self.assertEqual(len(response.context["quotes"]), 1)
