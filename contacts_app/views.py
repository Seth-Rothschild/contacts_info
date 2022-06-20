from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Contact, Event, Milestone
from django.template import loader
from django.urls import reverse

import datetime


def index(request):
    def sort_function(c):
        if c.most_recent_event() is None:
            return datetime.date.min
        else:
            return c.most_recent_event().date

    def get_recent_milestones():
        today = datetime.date.today()
        today_numeric = 100 * today.month + today.day
        unsorted_milestones = Milestone.objects.order_by(
            "date__month", "date__day"
        ).all()
        numerics = [x.date.month * 100 + x.date.day for x in unsorted_milestones]
        upcoming = []
        previous = []
        for milestone, numerics in zip(unsorted_milestones, numerics):
            if numerics >= today_numeric:
                upcoming.append(milestone)
            else:
                previous.append(milestone)
        return upcoming + previous

    contacts_list = Contact.objects.all()
    contacts_list = sorted(contacts_list, key=sort_function)
    milestones = get_recent_milestones()
    context = {
        "contacts_list": contacts_list,
        "upcoming_milestones": milestones[:5],
        "recent_milestones": milestones[-2:][::-1],
    }
    return render(request, "contacts_app/index.html", context)


def contact_details(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    events = contact.event_set.order_by("-date").all()
    milestones = contact.milestone_set.order_by("-date").all()
    context = {"contact": contact, "events": events, "milestones": milestones}
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


def add_milestone(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = request.POST
        if form["date"] == "":
            date = None
        else:
            date = form["date"]
        m = Milestone(
            contact=contact,
            date=date,
            description=form["description"],
            notify=False,
        )
        m.save()
        return HttpResponseRedirect(reverse("contact_details", args=[contact_id]))
    else:
        context = {
            "contact": contact,
            "formtype": "Add",
            "submit": reverse("add_milestone", args=[contact_id]),
        }
        return render(request, "contacts_app/modify_milestone.html", context)


def edit_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    if request.method == "POST":
        form = request.POST
        if form["date"] == "":
            date = None
        else:
            date = form["date"]
        milestone.date = date
        milestone.description = form["description"]
        milestone.save()
        return HttpResponseRedirect(
            reverse("contact_details", args=[milestone.contact.id])
        )
    else:
        context = {
            "milestone": milestone,
            "contact": milestone.contact,
            "formtype": "Edit",
            "submit": reverse("edit_milestone", args=[milestone_id]),
        }
        return render(request, "contacts_app/modify_milestone.html", context)


def delete_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    milestone.delete()
    return HttpResponseRedirect(reverse("contact_details", args=[milestone.contact.id]))
