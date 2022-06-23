from django.core.management.base import BaseCommand, CommandError
from contacts_app.models import Milestone, Contact
from contacts_app.config import CONFIG
import datetime
import requests


def should_notify(today, contact):
    if contact.most_recent_event() is None:
        return False
    days_since_event = (today - contact.most_recent_event().date).days
    notify_after = contact.notify_after
    if (
        notify_after > 0
        and days_since_event > 0
        and days_since_event % notify_after == 0
    ):
        return True
    return False


class Command(BaseCommand):
    help = "Checks Milestones and sends notifications"

    def handle(self, *args, **options):
        today = datetime.date.today()
        milestones = Milestone.objects.all()
        milestones_today = [
            x
            for x in milestones
            if (x.date.day == today.day and x.date.month == today.month)
        ]

        contacts = Contact.objects.all()
        contacts_today = [x for x in contacts if should_notify(today, x)]
        print(contacts_today)

        if CONFIG.get("gotify_url") is None:
            self.stdout.write(
                self.style.WARNING(
                    "No gotify_url key found in CONFIG dict in contacts_app.config. No notifications sent."
                )
            )
        else:
            for milestone in milestones_today:
                resp = requests.post(
                    CONFIG["gotify_url"],
                    json={
                        "message": milestone.__str__(),
                        "priority": 2,
                        "title": "Important Date",
                    },
                )

            for contact in contacts_today:
                days_since = (today - contact.most_recent_event().date).days
                message = "It has been {} days since last event with {}.".format(
                    days_since, contact.name
                )
                message += "\nSet to notify every {} days.".format(contact.notify_after)
                resp = requests.post(
                    CONFIG["gotify_url"],
                    json={
                        "message": message,
                        "priority": 2,
                        "title": "Should Contact {}".format(contact.name),
                    },
                )
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully sent notifications for: {}, {}".format(
                        milestones_today, contacts_today
                    )
                )
            )
