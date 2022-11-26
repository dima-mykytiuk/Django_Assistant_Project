from rest_framework import serializers

from .models import Contact, ContactPhone
from datetime import datetime


class ContactPhoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    def validate(self, data):
        if not data['phone'][1:].isdigit() or not data['phone'].startswith('+'):
            raise serializers.ValidationError("Phone must start with + and contain only digits")
        if len(data['phone']) != 13:
            raise serializers.ValidationError("Phone length must be 13 characters")
        return data
    
    class Meta:
        model = ContactPhone
        fields = ('id', 'phone')


class ContactSerializer(serializers.ModelSerializer):
    phones = ContactPhoneSerializer(many=True)
    
    def create(self, validated_data):
        phones = validated_data.pop('phones')
        all_phones = []
        contact_ids = [cnt.id for cnt in Contact.objects.filter(user_id=validated_data['user'].id)]
        cnt_emails = [cnt.email for cnt in Contact.objects.filter(user_id=validated_data.get('user').id)]
        for contact in contact_ids:
            all_phones.append([phn.phone for phn in ContactPhone.objects.filter(contact_id=contact)])
        for ls_phone in all_phones:
            if phones[0]['phone'] in ls_phone:
                raise serializers.ValidationError('Contact with this phone is already in the book')
        name = validated_data.get('name')
        birthday = validated_data.get('birthday')
        email = validated_data.get('email')
        address = validated_data.get('address')
        user = validated_data.get('user')
        if email in cnt_emails:
            raise serializers.ValidationError('Contact with this email is already in the book')
        contact = Contact.objects.create(name=name, birthday=birthday, email=email, address=address, user=user)
        for phone in phones:
            ContactPhone.objects.create(contact=contact, phone=phone.get('phone'))
        return contact
    
    def update(self, instance, validated_data):
        phones = validated_data.pop('phones')
        all_phones = []
        contact_ids = [cnt.id for cnt in Contact.objects.filter(user_id=validated_data['user'].id)]
        cnt_phones = [phn.phone for phn in ContactPhone.objects.filter(contact_id=instance.id)]
        for contact in contact_ids:
            all_phones.append([phn.phone for phn in ContactPhone.objects.filter(contact_id=contact)])
        instance.name = validated_data.get('name', instance.name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        if instance.email == validated_data.get('email'):
            pass
        else:
            cnt_emails = [cnt.email for cnt in Contact.objects.filter(user_id=validated_data.get('user').id)]
            if validated_data.get('email') in cnt_emails:
                raise serializers.ValidationError('Contact with this email is already in the book')
            else:
                instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        list_of_phones = [phn['phone'] for phn in phones]
        for phone in phones:
            if phone['phone'] in cnt_phones:
                continue
            elif "id" in phone.keys():
                for ls_phone in all_phones:
                    if phone['phone'] in ls_phone:
                        raise serializers.ValidationError('Contact with this phone is already in the book')
                    else:
                        contact_phone = ContactPhone.objects.get(id=phone["id"])
                        contact_phone.phone = phone.get('phone', contact_phone.phone)
                        contact_phone.save()
            else:
                cnt_phones.append(phone.get('phone'))
                ContactPhone.objects.create(contact=instance, phone=phone.get('phone'))
        if len(cnt_phones) > len(phones):
            for phone in cnt_phones:
                if phone not in list_of_phones:
                    ContactPhone.objects.get(phone=phone).delete()
        return instance
    
    class Meta:
        model = Contact
        fields = ('id', 'name', 'birthday', 'email', 'address', 'phones', 'user')
    
    def validate(self, data):
        date_delta = (datetime.now().date() - data['birthday']).days
        if len(data['phones']) > 4:
            raise serializers.ValidationError("Maximum amount of phones is 4")
        if len(data['name']) < 3:
            raise serializers.ValidationError("Name must be more than 3 characters")
        if date_delta < 0:
            raise serializers.ValidationError("Invalid birthday, you from future?")
        if date_delta > 36525:
            raise serializers.ValidationError("Invalid birthday, maximum contact age is 100 years")
        if len(data['address']) < 4:
            raise serializers.ValidationError("Address must be more than 4 characters")
        return data
