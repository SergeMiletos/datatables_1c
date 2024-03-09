from django.urls import path

from . import views

app_name = "datatables"
urlpatterns = [
    path("", views.get1cdata, name="tables"),
    path("tables/", views.get1cdata, name="tables"),
    ]
