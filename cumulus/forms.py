from django import forms
from cumulus.models import Host, Key, Datum

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = [ 'name', 'ip' ]

class KeyForm(forms.ModelForm):
    class Meta:
        model = Key
        fields = [ 'name', 'type', 'description' ]

class DatumForm(forms.ModelForm):
    class Meta:
        model = Datum
        fields = [ 'value', 'key', 'host' ]
