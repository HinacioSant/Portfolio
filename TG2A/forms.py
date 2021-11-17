from django import forms
from .models import gallery
from .validators import validate_file_size


# Upload Form:
class ImageForm(forms.ModelForm):
    image = forms.ImageField(validators=[validate_file_size], widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}))

    class Meta:
        model = gallery

        fields = ('title', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),


        }
