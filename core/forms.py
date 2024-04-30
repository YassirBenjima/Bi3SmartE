from django import forms
from core.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write Your Review', 'class': 'input'}))
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
