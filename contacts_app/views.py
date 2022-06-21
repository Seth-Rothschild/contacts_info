from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Contact, Event, Milestone
from django.template import loader
from django.urls import reverse

import datetime
from django import forms


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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "address", "notes"]


def add_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "formtype": "Add Contact",
            "submit": reverse("add_contact"),
            "back": reverse("index"),
            "form": ContactForm(),
        }
        return render(request, "contacts_app/modify.html", context)


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        form.save()
        return HttpResponseRedirect(reverse("contact_details", args=[contact_id]))
    else:
        context = {
            "formtype": "Edit Contact: {}".format(contact.name),
            "submit": reverse("edit_contact", args=[contact_id]),
            "back": reverse("contact_details", args=[contact_id]),
            "delete": reverse("delete_contact", args=[contact_id]),
            "form": ContactForm(instance=contact),
        }
        return render(request, "contacts_app/modify.html", context)


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    contact.delete()
    return HttpResponseRedirect(reverse("index"))


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["date", "description", "notes"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


def add_event(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = EventForm(request.POST).save(commit=False)
        form.contact = contact
        form.save()
        return HttpResponseRedirect(reverse("contact_details", args=[contact_id]))
    else:
        context = {
            "formtype": "Add Event for {}".format(contact.name),
            "submit": reverse("add_event", args=[contact_id]),
            "back": reverse("contact_details", args=[contact_id]),
            "form": EventForm(),
        }
        return render(request, "contacts_app/modify.html", context)


def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        form.save()
        return HttpResponseRedirect(reverse("contact_details", args=[event.contact.id]))
    else:
        context = {
            "formtype": "Edit Event for {}".format(event.contact.name),
            "submit": reverse("edit_event", args=[event_id]),
            "back": reverse("contact_details", args=[event.contact.id]),
            "delete": reverse("delete_event", args=[event_id]),
            "form": EventForm(instance=event),
        }
        return render(request, "contacts_app/modify.html", context)


def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse("contact_details", args=[event.contact.id]))


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ["date", "description"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


def add_milestone(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == "POST":
        form = MilestoneForm(request.POST).save(commit=False)
        form.contact = contact
        form.save()
        return HttpResponseRedirect(reverse("contact_details", args=[contact_id]))
    else:
        context = {
            "formtype": "Add Important Date for {}".format(contact.name),
            "submit": reverse("add_milestone", args=[contact_id]),
            "back": reverse("contact_details", args=[contact_id]),
            "form": MilestoneForm(),
        }
        return render(request, "contacts_app/modify.html", context)


def edit_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    if request.method == "POST":
        form = MilestoneForm(request.POST, instance=milestone)
        form.save()
        return HttpResponseRedirect(
            reverse("contact_details", args=[milestone.contact.id])
        )
    else:
        context = {
            "formtype": "Edit Important Date for {}".format(milestone.contact.name),
            "submit": reverse("edit_milestone", args=[milestone_id]),
            "back": reverse("contact_details", args=[milestone.contact.id]),
            "delete": reverse("delete_milestone", args=[milestone_id]),
            "form": MilestoneForm(instance=milestone),
        }
        return render(request, "contacts_app/modify.html", context)


def delete_milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    milestone.delete()
    return HttpResponseRedirect(reverse("contact_details", args=[milestone.contact.id]))
