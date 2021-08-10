from django import forms 
from django.forms import Form
from main.models import Saccos


class DateInput(forms.DateInput):
    input_type = "date"

class AddMembersForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Saccos
    try:
        saccos = Saccos.objects.all()
        saccos_list = []
        for sacco in saccos:
            single_sacco = (sacco.id, sacco.sacco_name)
            saccos_list.append(single_sacco)
    except:
        sacco_list = []

    # saccos_list =(
    #     ('Shamiri','Shamiri')
    #     )
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    sacco_id = forms.ChoiceField(label="Sacco", choices=saccos_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))