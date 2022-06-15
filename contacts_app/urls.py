from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "<int:contact_id>/contact_details/",
        views.contact_details,
        name="contact_details",
    ),
    path("<int:contact_id>/event_log/", views.event_log, name="event_log"),
]
