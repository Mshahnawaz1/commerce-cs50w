from django import forms
from .models import Listing,Comment

class Listing_form(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'description', 'category', 'image_url', 'starting_bid']

# class Comment_form(forms.ModelForm):
#     class Meta:
#         model= Comment
#         fields = ['comment']
   