from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView

from .models import Contact, ContactPhone
from .forms import AddContact, ChangeName, ChangeBirthday, AddPhone, ChangeEmail, ChangeAddress
from django.views import View

from .tasks import send_delete_contact, send_delete_phone, send_change_name, send_change_email, send_change_address, \
    send_change_birthday


# Create your views here.


class IndexView(View):
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'title': 'Web assistant'})


class AddContactView(LoginRequiredMixin, View):
    form_class = AddContact
    template_name = 'pages/add_contact.html'

    def get(self, request, *args, **kwargs):
        form = AddContact()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            birthday = form.cleaned_data['birthday']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            phones = form.cleaned_data['phone']
            contact = Contact(user_id=logged_user_id, name=name, birthday=birthday, email=email, address=address)
            contact.save()
            list_of_phones = phones.split(',')
            form.send_email(request.user.email)
            for phone in list_of_phones:
                added_phone = ContactPhone(contact_id=contact.id, phone=phone.strip())
                added_phone.save()
            return redirect('contact_book')

        return render(request, self.template_name, {'form': form})


class ContactsView(LoginRequiredMixin, View):
    template_name = 'pages/contact_book.html'
    phones = ContactPhone.objects.all()
    context = {'phones': phones}
    
    def get(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        phones = ContactPhone.objects.all()
        contact = Contact.objects.filter(user_id=logged_user_id)
        self.context.update({'contact': contact})
        self.context.update({'phones': phones})
        return render(request, self.template_name, context=self.context)
    
    def post(self, request, *args, **kwargs):
        logged_user_id = request.user.id
        valid_contacts = []
        if 'find_contact' in request.POST:
            name = request.POST['find_contact']
            valid_contacts = Contact.objects.filter(user_id=logged_user_id, name__icontains=name)
        elif 'find_birthday' in request.POST:
            date_interval = request.POST['find_birthday']
            try:
                date_interval = int(date_interval)
            except ValueError:
                self.context.update({'contact': valid_contacts})
                return render(request, template_name='pages/contact_book.html', context=self.context)
            for this_cnt in Contact.objects.filter(user_id=logged_user_id):
                current_date = datetime.now().date()
                this_year_birthday = datetime(
                    year=current_date.year,
                    month=this_cnt.birthday.month,
                    day=this_cnt.birthday.day,
                ).date()
                if current_date > this_year_birthday:
                    this_year_birthday = datetime(
                        year=current_date.year + 1,
                        month=this_cnt.birthday.month,
                        day=this_cnt.birthday.day,
                    ).date()
                if (this_year_birthday - current_date).days <= date_interval:
                    valid_contacts.append(this_cnt)
        self.context.update({'contact': valid_contacts})
        return render(request, template_name='pages/contact_book.html', context=self.context)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'pages/delete_contact.html'
    success_url = reverse_lazy('contact_book')

    def delete(self, request, *args, **kwargs):
        contact_name = Contact.objects.get(pk=self.kwargs['pk']).name
        response = super(ContactDeleteView, self).delete(request, *args, **kwargs)
        send_delete_contact.delay(request.user.username, request.user.email, contact_name)
        return response


class DetailContactView(LoginRequiredMixin, View):
    phones_model = ContactPhone
    contact_model = Contact
    
    def get(self, request, *args, **kwargs):
        phones = self.phones_model.objects.filter(contact_id=self.kwargs['contact_id'])
        contact = self.contact_model.objects.get(pk=self.kwargs['contact_id'])
        context = {
            'id_contact': self.kwargs['contact_id'],
            'phones': phones,
            'contact': contact,
        }
        return render(request, 'pages/detail_contact.html', context)


class AddPhoneView(LoginRequiredMixin, View):
    form_class = AddPhone
    template_name = 'pages/add_phone.html'
    
    def get(self, request, *args, **kwargs):
        context = {
            'form': AddPhone(),
            'id_contact': self.kwargs['contact_id']
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = request.POST['phone']
            phone_to_add = ContactPhone(contact_id=self.kwargs['contact_id'], phone=phone.strip())
            contact = Contact.objects.get(pk=self.kwargs['contact_id'])
            phone_to_add.save()
            form.send_email(request.user.username, request.user.email, contact.name)
            return redirect('detail_contact', contact_id=self.kwargs['contact_id'])
        
        return render(request, self.template_name, {'form': form})
    

class ChangeNameView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'pages/change_contact_name.html'
    form_class = ChangeName
    
    def get_success_url(self):
        contact_id = self.kwargs['pk']
        send_change_name.delay(self.request.user.username, self.request.user.email)
        return reverse_lazy('detail_contact', kwargs={'contact_id': contact_id})


class ChangeEmailView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'pages/change_email.html'
    form_class = ChangeEmail

    def get_success_url(self):
        contact_id = self.kwargs['pk']
        contact = Contact.objects.get(pk=contact_id)
        send_change_email.delay(self.request.user.username, self.request.user.email, contact.name)
        return reverse_lazy('detail_contact', kwargs={'contact_id': contact_id})


class ChangeBirthdayView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'pages/change_birthday.html'
    form_class = ChangeBirthday

    def get_success_url(self):
        contact_id = self.kwargs['pk']
        contact = Contact.objects.get(pk=contact_id)
        send_change_birthday.delay(self.request.user.username, self.request.user.email, contact.name)
        return reverse_lazy('detail_contact', kwargs={'contact_id': contact_id})


class ChangeAddressView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'pages/change_address.html'
    form_class = ChangeAddress

    def get_success_url(self):
        contact_id = self.kwargs['pk']
        contact = Contact.objects.get(pk=contact_id)
        send_change_address.delay(self.request.user.username, self.request.user.email, contact.name)
        return reverse_lazy('detail_contact', kwargs={'contact_id': contact_id})


class PhoneDeleteView(LoginRequiredMixin, DeleteView):
    model = ContactPhone
    template_name = 'pages/delete_form.html'
    
    def delete(self, request, *args, **kwargs):
        response = super(PhoneDeleteView, self).delete(request, *args, **kwargs)
        contact = Contact.objects.get(pk=self.kwargs['contact_id'])
        send_delete_phone.delay(request.user.username, request.user.email, contact.name)
        return response
    
    def get_success_url(self):
        contact_id = self.kwargs['contact_id']
        return reverse_lazy('detail_contact', kwargs={'contact_id': contact_id})
    