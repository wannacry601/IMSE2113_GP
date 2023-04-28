from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models
from GroupProject import settings

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'add-user'
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name=forms.CharField(max_length=150)
    email=forms.EmailField(max_length=150)
    is_superuser=forms.ChoiceField(widget=forms.RadioSelect(),choices=(('Yes','Yes'),('No', 'No')))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

class ChangePassword(forms.Form):
    username = forms.CharField(max_length=150)
    old_Password = forms.CharField(widget=forms.PasswordInput())
    new_Password = forms.CharField(widget=forms.PasswordInput())

class Cargo(forms.Form):

    is_in_warehouse = forms.BooleanField()
    on_pellet = forms.ModelChoiceField(queryset=models.Pellet.objects.all())
    destination = forms.CharField(max_length = 50)
    arrival_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    origin = forms.CharField(max_length = 50)
    due_outbound_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    name = forms.CharField(max_length = 32)
    desc = forms.CharField(max_length = 200)
    weight = forms.DecimalField(max_digits=4, decimal_places=2)
    category = forms.ModelChoiceField(queryset=models.Products.objects.all())
    # class Meta:
    #     model = models.Cargo
    #     fields = ('is_in_warehouse', 
    #               'on_pellet', 
    #               'destination', 
    #               'arrival_date', 
    #               'origin', 
    #               'due_outbound_date', 'name', 
    #               'desc',
    #               'weight',
    #               'category',)