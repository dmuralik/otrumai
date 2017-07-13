from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from game.models import Activist, Activity, ActivityLog
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from game.forms import ActivistForm
from django.contrib.auth.models import User
from django.shortcuts import redirect


@login_required
def home(request):
	#if not request.user.is_authenticated():
		#return render('login')
	activist = Activist.objects.get( user = request.user)
	completionMessage = ""

	if request.method == "POST":
		activityLog = ActivityLog()
		activityLog.player = activist
		activityLog.activity = activist.currentActivity
		frm = ActivistForm(request.POST, instance = activityLog)	
		if frm.is_valid():
			frm.save()
			try:
				activity = Activity.objects.get(phase = activist.currentActivity.phase, step = activist.currentActivity.step + 1)
			except Activity.DoesNotExist:
				activity = None
			
			
			message = ""
			if activity == None:
				completionMessage = "Congratulations on completing Phase " + str(activist.currentActivity.phase)
				try:
					activity = Activity.objects.get(phase = activist.currentActivity.phase + 1, step = 1)
				except Activity.DoesNotExist:
					activity = None
				
			if activity != None:
				activist.currentActivity = activity
				activist.save()
			else:
				completionMessage = "You are awesome! You have successfully completed all tasks. We hope you now feel empowered to speak up about gender issues wherever you encounter them."
			

	phasedesc = ""

	if activist.currentActivity.phase == 1:
		phasedesc = "Phase 1: Learn"
	elif activist.currentActivity.phase == 2:
		phasedesc = "Phase 2: Share"
	elif activist.currentActivity.phase == 3:
		phasedesc = "Phase 3: Act"
	#get current activity for user
	#activist = Activist.objects.get( user = request.user)

	#populate dict for form binding
	frmData = {'player': activist, 'activity': activist.currentActivity}

	frm =  ActivistForm(frmData)
	return render(request, 'game/game.html', {'form' : frm, 'activityDesc' : activist.currentActivity.description, 'phasedesc': phasedesc, 'completionMsg': completionMessage})


def register(request):
	if request.method == 'POST':
		frm = UserCreationForm(request.POST)
		if frm.is_valid():
			usr = frm.save()
			activist = Activist()
			activist.user = usr
			activist.currentActivity = Activity.objects.get(phase = 1, step = 1)
			activist.save()
			return render(request, 'game/useractivated.html')
	else:
		frm = UserCreationForm()

	return render(request, 'game/register.html', {'form' : frm})

def login(request, **kwargs):
	if request.user.is_authenticated():
		return redirect('home')
	else: 
	    return auth_views.login(request, **kwargs)

