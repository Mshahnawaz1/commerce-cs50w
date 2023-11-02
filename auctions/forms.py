from django import forms
from .models import Listing,Comment

class Listing_form(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'description', 'category', 'image_url', 'starting_bid']

        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control mb-3'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }   