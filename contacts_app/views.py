from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Contact, Event
from django.template import loader
from django.urls import reverse


def index(request):
    contacts_list = Contact.objects.all()
    context = {"contacts_list": contacts_list}
    template = loader.get_template("contacts_app/index.html")
    return render(request, "contacts_app/index.html", context)


def contact_details(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    events = contact.event_set.all()
    context = {"contact": contact, "events": events}
    return render(request, "contacts_app/contact_details.html", context)


def add_contact(request):
    if request.method == "POST":
        form = request.POST
        c = Contact(
            name=form["name"],
            email=form["email"],
            address=form["address"],
            notes=form["notes"],
        )
        c.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "formtype": "Add",
            "submit": reverse("add_contact"),
            "back": reverse("index"),
        }
        return render(request, "contacts_app/modify_contact.html", context)


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = request.POST
        contact.name = form["name"]
        contact.email = form["email"]
        contact.address = form["address"]
        contact.notes = form["notes"]
        contact.save()
        return HttpResponseRedirect(reverse("contact_details", args=[contact_id]))
    else:
        context = {
            "contact": contact,
            "formtype": "Edit",
            "submit": reverse("edit_contact", args=[contact_id]),
            "back": reverse("contact_details", args=[contact_id]),
        }
        return render(request, "contacts_app/modify_contact.html", context)


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return HttpResponseRedirect(reverse("index"))


def add_event(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = request.POST
        if form["date"] == "":
            date = None
        else:
            date = form["date"]
        e = Event(
            contact=contact,
            date=date,
            description=form["description"],
            notes=form["notes"],
        )
        e.save()
        return HttpResponseRedirect(reverse("contact_details", args=[contact_id]))
    else:
        context = {
            "contact": contact,
            "formtype": "Add",
            "submit": reverse("add_event", args=[contact_id]),
        }
        return render(request, "contacts_app/modify_event.html", context)


def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = request.POST
        if form["date"] == "":
            date = None
        else:
            date = form["date"]
        event.date = date
        event.description = form["description"]
        event.notes = form["notes"]
        event.save()
        return HttpResponseRedirect(reverse("contact_details", args=[event.contact.id]))
    else:
        context = {
            "event": event,
            "contact": event.contact,
            "formtype": "Edit",
            "submit": reverse("edit_event", args=[event_id]),
        }
        return render(request, "contacts_app/modify_event.html", context)


def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse("contact_details", args=[event.contact.id]))
