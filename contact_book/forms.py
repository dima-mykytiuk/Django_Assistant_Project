from django import forms
from datetime import datetime
from .models import Contact, ContactPhone
from django.core.validators import validate_email, ValidationError
from .tasks import send_add_contact_email, send_add_phone
from django.contrib.auth.models import User


class AddContact(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddContact, self).__init__(*args, **kwargs)
    name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'contact_name_form'}))
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'email_form'}))
    address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'address_form'}))
    phone = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'phone_form'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date_form'}))
    
    def send_email(self, user_email):
        user = User.objects.get(id=self.user)
        send_add_contact_email.delay(user_email, user.username, self.cleaned_data['name'])
    
    def clean(self):

        super(AddContact, self).clean()

        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        address = self.cleaned_data['address']
        phones = [phn.strip() for phn in self.cleaned_data['phone'].split(',')]
        birthday = self.cleaned_data['birthday']
        date_delta = (datetime.now().date() - birthday).days
        all_emails = [cnt.email for cnt in Contact.objects.filter(user_id=self.user)]
        contact_ids = [cnt.id for cnt in Contact.objects.filter(user_id=self.user)]
        all_phones = []
        for contact in contact_ids:
            all_phones.append([cnt.phone for cnt in ContactPhone.objects.filter(contact_id=contact)])
        if len(name) > 40:
            self._errors['name'] = self.error_class(['Name length is maximum 40 characters'])
        if len(email) > 50:
            self._errors['email'] = self.error_class(['Email length is maximum 50 characters'])
        if email in all_emails:
            self._errors['email'] = self.error_class(['Contact with this email is already in the book'])
        if date_delta < 0:
            self._errors['birthday'] = self.error_class(['Invalid birthday'])
        if date_delta > 36525:
            self._errors['birthday'] = self.error_class(['Maximum contact age is 100 years'])
        if len(address) > 50:
            self._errors['address'] = self.error_class(['Address length is maximum 50 characters'])
        try:
            validate_email(email)
        except ValidationError:
            self._errors['email'] = self.error_class(['Invalid email'])
        if len(phones) > 4:
            self._errors['phone'] = self.error_class(['Maximum amount of phones is 4'])
        for this_phone in phones:
            if len(this_phone) != 13:
                self._errors['phone'] = self.error_class(['Phone length is maximum 13 characters'])
            for ls_phone in all_phones:
                for phone in ls_phone:
                    if this_phone in phone:
                        self._errors['phone'] = self.error_class(['Contact with this phone is already in the book'])
                        break
            if not this_phone[1:].isdigit() or not this_phone.startswith('+'):
                self._errors['phone'] = self.error_class(['Phone must start with + and contain only digits'])
            if len(this_phone) < 13:
                self._errors['phone'] = self.error_class(['Phone length must be 13 characters'])
        return self.cleaned_data


class ChangeName(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name',)
        
    def clean(self):
        super(ChangeName, self).clean()
        
        new_name = self.cleaned_data['name']
        
        if len(new_name) > 40:
            self._errors['name'] = self.error_class(['Name length is maximum 40 characters'])
            
        if len(new_name) < 3:
            self._errors['name'] = self.error_class(['Name length is minimum 3 characters'])
        
        return self.cleaned_data


class ChangeBirthday(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ('birthday',)
        
    def clean(self):
        
        super(ChangeBirthday, self).clean()
        
        new_birthday = self.cleaned_data['birthday']
        
        date_delta = (datetime.now().date() - new_birthday).days
        
        if date_delta < 0:
            self._errors['birthday'] = self.error_class(['Invalid birthday, contact from Future?'])
        if date_delta > 36525:
            self._errors['birthday'] = self.error_class(['Maximum contact age is 100 years'])
        
        return self.cleaned_data


class AddPhone(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddPhone, self).__init__(*args, **kwargs)
    phone = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'email_form'}))
    
    @staticmethod
    def send_email(user_email, user, contact_name):
        send_add_phone.delay(user_email, user, contact_name)
    
    def clean(self):
        
        super(AddPhone, self).clean()
        
        phone = self.cleaned_data['phone']
        contact_ids = [cnt.id for cnt in Contact.objects.filter(user_id=self.user)]
        all_phones = []
        for contact in contact_ids:
            all_phones.append([phn.phone for phn in ContactPhone.objects.filter(contact_id=contact)])
        for ls_phone in all_phones:
            for old_phone in ls_phone:
                if phone in old_phone:
                    self._errors['phone'] = self.error_class(['Contact with this phone is already in the book'])
        if len(phone) > 13:
            self._errors['phone'] = self.error_class(['Phone length is maximum 13 characters'])
        if not phone[1:].isdigit() or not phone.startswith('+'):
            self._errors['phone'] = self.error_class(['Phone must start with + and contain only digits'])
        
        return self.cleaned_data


class ChangeEmail(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeEmail, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Contact
        fields = ('email',)
    
    def clean(self):
        
        super(ChangeEmail, self).clean()
        
        email = self.cleaned_data['email']
        all_emails = [cnt.email for cnt in Contact.objects.filter(user_id=self.user)]
        if len(email) > 50:
            self._errors['email'] = self.error_class(['Email length is maximum 25 characters'])
        if email in all_emails:
            self._errors['email'] = self.error_class(['Contact with this email is already in the book'])
        try:
            validate_email(email)
        except ValidationError:
            self._errors['email'] = self.error_class(['Invalid email'])
        
        return self.cleaned_data


class ChangeAddress(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ('address',)
        
    def clean(self):
        super(ChangeAddress, self).clean()
        
        new_address = self.cleaned_data['address']
        
        if len(new_address) > 35:
            self._errors['address'] = self.error_class(['Address length is maximum 50 characters'])
            
        if len(new_address) < 3:
            self._errors['address'] = self.error_class(['Address length is minimum 3 characters'])
        
        return self.cleaned_data
    