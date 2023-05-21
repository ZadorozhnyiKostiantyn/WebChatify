from django import forms
from .models import ChatRoom


class CreateNewGroupForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ["name", "photo"]
        widgets = {
            "name": forms.TextInput(attrs={
                'name': "group_name",
                'placeholder': 'Enter group name...',
            }),
            "photo": forms.FileInput(attrs={
                'name': "group_photo",
                'id': "group_photo",
                'accept': "image/*",
            })
        }