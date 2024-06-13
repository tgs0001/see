from django import forms
from django.core import validators
from . import petro

 




class EmployeeRegistration(forms.Form):
    name = forms.CharField(label='Full Name')
    email = forms.CharField()
    enothi_id = forms.CharField(label='Enothi ID')
    empid = forms.CharField(label='Employee ID')
    designation = forms.ChoiceField(choices = petro.designations, label="Designation")
    section = forms.ChoiceField(choices = petro.sections, label="Section")
    department = forms.ChoiceField(choices = petro.departments, label="Department")
    division = forms.ChoiceField(choices = petro.divisions, label="Division")
    directorate = forms.ChoiceField(choices = petro.directorates, label="Directorate")
     


    #def __init__(self,enothi_id):
    #    self.name = forms.CharField(label='Full Name')
    ##    self.email = forms.CharField()
    #    self.enothi_id = forms.CharField(label='Enothi ID',initial = enothi_id, disabled = True)
    #    self.empid = forms.CharField(label='Employee ID')
    ##    self.designation = forms.CharField()
    #    self.section = forms.CharField(label="Section")
    #    self.department = forms.CharField()
    #    self.division = forms.CharField()
    #    self.directorate = forms.CharField()
        

    #def __str__ (self):
        #return 'Employee Name'+self.name + ' --  Enothi ID '+self.enothi_id

    def clean(self):
        cleaned_data = super().clean()
        print("this is clean data")
        print(self.cleaned_data.get("password"))
        #rightpass = self.cleaned_data.get("password")
        #wrongpass = self.cleaned_data['repassword']
        
        #if rightpass != wrongpass:
        #    raise forms.ValidationError('Password does not match')