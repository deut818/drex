from django import forms
from .models import User
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

#make slug field unique

class RegistrationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('OTHER', 'OTHER')
    )
    fname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control input-field'}))
    lname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control input-field'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control input-field'}))
    city = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'City Name', 'class':'form-control input-field'}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'placeholder':'Email address', 'class':'form-control input-field'}))
    date_of_birth = forms.DateField(label='', widget=forms.DateInput(attrs={'placeholder':'YYYY-MM-DD', 'class':'form-control input-field', 'type':'date'}))
    gender = forms.CharField(widget=forms.Select(choices=GENDER, attrs={'placeholder':'Email address', 'class':'form-control input-field'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control input-field',"id":"psw","pattern":"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}","title":"Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Password confirmation', 'class':'form-control input-field'}))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(
           attrs={"class": "form-control input-field"}
        )
    )

    class Meta:
        model = User
        fields = ('fname', 'lname', 'username', 'gender', 'city', 'country', 'email', 'date_of_birth')
        widgets = {'country': CountrySelectWidget(attrs={'label': ''})}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


