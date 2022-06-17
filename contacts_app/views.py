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
    form = request.POST
    if request.method == "POST":
        if form["birthday"] == "":
            birthday = None
        else:
            birthday = form["birthday"]
        c = Contact(
            name=form["name"],
            email=form["email"],
            address=form["address"],
            birthday=birthday,
            notes=form["notes"],
        )
        c.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "contacts_app/add_contact.html", {})


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = request.POST
        if form["birthday"] == "":
            birthday = None
        else:
            birthday = form["birthday"]
        contact.name=form["name"]
        contact.email=form["email"]
        contact.address=form["address"]
        contact.birthday=birthday
        contact.notes=form["notes"]
        contact.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "contacts_app/edit_contact.html", {"contact": contact})


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return HttpResponseRedirect(reverse("index"))


def add_event(request):
    return HttpResponse("add event route")


def edit_event(request, event_id):
    return HttpResponse("edit event {} route".format(event_id))


def delete_event(request, event_id):
    return HttpResponse("delete event {} route".format(event_id))
