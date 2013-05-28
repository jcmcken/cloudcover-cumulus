from django import forms

class HostForm(forms.Form):
    ip = forms.IPAddressField()

class KeyForm(forms.Form):
    pass

class DatumForm(forms.Form):
    pass
