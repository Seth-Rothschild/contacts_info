from django.shortcuts import render,get_object_or_404
from django.http import Http404

# Create your views here.
from django.http import HttpResponse
from .models import Contact, Event
from django.template import loader

def index(request):
    contacts_list = Contact.objects.all()
    context = {
        'contacts_list': contacts_list
    }
    template = loader.get_template('contacts_app/index.html')
    return render(request, 'contacts_app/index.html', context)


def contact_details(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'contacts_app/contact_details.html', {'contact': contact})


def event_log(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    events = contact.event_set.all()
    context = {"contact": contact, "events": events}
    return render(request, 'contacts_app/event_log.html', context)
