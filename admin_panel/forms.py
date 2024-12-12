from django import forms
from account.models import User
from transaction.models import Prescription, Order
from .models import About, SliderImage, TeamMember, FullWidthImage, MediaItem

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'

class SliderImageForm(forms.ModelForm):
    class Meta:
        model = SliderImage
        fields = '__all__'

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'

class FullWidthImageForm(forms.ModelForm):
    class Meta:
        model = FullWidthImage
        fields = '__all__'

class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = '__all__'