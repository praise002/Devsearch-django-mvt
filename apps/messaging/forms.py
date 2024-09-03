from django import forms
from . import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
        self.fields['name'].widget.attrs.update({'placeholder': 'Leave blank if logged in'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Leave blank if logged in'})