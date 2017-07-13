from django import forms
from django.core.exceptions import ValidationError
from game.models import ActivityLog


class ActivistForm(forms.ModelForm):

	class Meta:
		model = ActivityLog
		fields = ['notes']

	def clean_player(self):
		player = self.cleaned_data['player']
		if not player:
			raise ValidationError("Invalid player")

	def clean_activity(self):
		activity = self.cleaned_data['activity']
		if not activity:
			raise ValidationError("Invalid activity")
	