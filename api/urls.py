from django.urls import path
from .views import *

urlpatterns = [
    path("check", check, name="check"),
    path("scrape", scrape, name="scrape"),
    path("tenders", get_tenders, name="tenders")
]