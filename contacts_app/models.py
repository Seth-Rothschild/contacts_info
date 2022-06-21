from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def most_recent_event(self):
        return self.event_set.order_by("-date").first()


class Event(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return "{}: {} ({})".format(self.contact.name, str(self.date), self.description)


class Milestone(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=200)
    notify = models.BooleanField(null=True)

    def __str__(self):
        return "{}: {} ({})".format(self.contact.name, str(self.date), self.description)
