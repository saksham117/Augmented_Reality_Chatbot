"""
Defining all our forms here
"""
from django import forms



class Question(forms.Form):
    """
        # form for creating class using form api
    """
    question = forms.CharField(max_length=300, required=True, 
                                widget=forms.TextInput(attrs={'placeholder': 'Ask Me Anything',
                                                               'class': 'form-control'}))

