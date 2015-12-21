from django import forms


class GuestbookForm(forms.Form):
    name = forms.CharField(label='name',
                           max_length=30,
                           widget=forms.TextInput(attrs={'class': 'guestbook_name'}))
    comment = forms.CharField(label='comment',
                              widget=forms.Textarea(attrs={'class': 'guestbook_comment'}),
                              max_length=2000)
    # error_css_class = 'guestbook_error'


# EMAIL-VERSION of CONTACT (me-view)
class EmailForm(forms.Form):
    sender_email = forms.EmailField(label='sender',
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'me_sender'}))
    subject = forms.CharField(label="subject_text",
                              required=True,
                              max_length=50,
                              widget=forms.TextInput(attrs={'class': 'me_subject'}))
    content = forms.CharField(label='content_text',
                              required=True,
                              max_length=20000,
                              widget=forms.Textarea(attrs={'class': 'me_content'}))