from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(label='',
            widget=forms.TextInput(
                attrs={"class":"form-control type_msg", "placeholder":"Type your message..."}
                )
            )