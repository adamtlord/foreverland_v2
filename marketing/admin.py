from django.contrib import admin
from marketing.models import Testimonial


class TestimonialAdmin(admin.ModelAdmin):
    search_fields = ["quote, show, featured"]
    list_display = ["quote", "source", "show", "featured"]


admin.site.register(Testimonial, TestimonialAdmin)
