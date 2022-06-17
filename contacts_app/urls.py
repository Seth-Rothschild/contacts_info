from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "<int:contact_id>/contact_details/",
        views.contact_details,
        name="contact_details",
    ),
    path(
        "contact/add/",
        views.add_contact,
        name="add_contact",
    ),
    path(
        "contact/delete/<int:contact_id>",
        views.delete_contact,
        name="delete_contact",
    ),
    path(
        "contact/edit/<int:contact_id>",
        views.edit_contact,
        name="edit_contact",
    ),
    path(
        "event/add/",
        views.add_event,
        name="add_event",
    ),
    path(
        "event/delete/<int:event_id>",
        views.delete_event,
        name="delete_event",
    ),
    path(
        "event/edit/<int:event_id>",
        views.edit_event,
        name="edit_event",
    ),
]
