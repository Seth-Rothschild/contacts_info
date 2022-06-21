from django.core.management.base import BaseCommand, CommandError
from contacts_app.models import Milestone
from contacts_app.config import CONFIG
import datetime
import requests


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
        if len(milestones_today) == 0:
            self.stdout.write(self.style.SUCCESS("Success! No important events today"))
        else:
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
                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully sent notifications for: {}".format(
                            milestones_today
                        )
                    )
                )
