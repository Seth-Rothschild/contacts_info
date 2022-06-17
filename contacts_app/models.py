from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    birthday = models.DateField(blank=True, null=True)
    notes = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200)
    notes = models.TextField()

    def __str__(self):
        return "{} ({})".format(str(self.date), self.description)
