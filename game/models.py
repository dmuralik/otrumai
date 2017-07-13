from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
	phase = models.IntegerField()
	step = models.IntegerField()
	description = models.TextField(unique = True)


class Activist(models.Model):

    #this model can be extended later for any additional fields like activation key
	user = models.OneToOneField(User)
	currentActivity = models.ForeignKey(Activity)


class ActivityLog(models.Model):
	player = models.ForeignKey(Activist)
	activity = models.ForeignKey(Activity)
	notes = models.TextField(null = True, blank = True)
	createdOn = models.DateTimeField(auto_now_add = True)
	modifiedOn = models.DateTimeField(auto_now = True)



