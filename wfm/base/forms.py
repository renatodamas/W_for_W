from django import forms

from wfm.base.models import Item


class DoacaoChangeListForm(forms.ModelForm):
    # here we only need to define the field we want to be editable
    item = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False)
