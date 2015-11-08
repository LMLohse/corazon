from django import forms


class GuestbookForm(forms.Form):
    name = forms.CharField(label='name',
                           max_length=30,
                           widget=forms.TextInput(attrs={'class': 'guestbook_name'}))
    comment = forms.CharField(label='comment',
                              widget=forms.Textarea(attrs={'class': 'guestbook_comment'}),
                              max_length=2000)
    # error_css_class = 'guestbook_error'