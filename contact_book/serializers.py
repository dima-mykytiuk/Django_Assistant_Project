from rest_framework import serializers

from .models import Contact, ContactPhone
from datetime import datetime


class ContactPhoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    def validate(self, data):
        if not data['phone'][1:].isdigit() or not data['phone'].startswith('+'):
            raise serializers.ValidationError("Phone must start with + and contain only digits")
        if len(data['phone']) < 13:
            raise serializers.ValidationError("Phone length must be 13 characters")
        return data
    
    class Meta:
        model = ContactPhone
        fields = ('id', 'phone')


class ContactSerializer(serializers.ModelSerializer):
    phones = ContactPhoneSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        phone = validated_data.pop('phones')
        if ContactPhone.objects.filter(phone=phone[0]['phone']).exists():
            raise serializers.ValidationError('Contact with this phone is already in the book')
        else:
            contact = Contact.objects.create(**validated_data)
            ContactPhone.objects.create(contact=contact, **phone[0])
        return contact

    def update(self, instance, validated_data):
        phones = validated_data.pop('phones')
        instance.name = validated_data.get('name', instance.name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        email = validated_data.pop('email')
        contact_object = Contact.objects.get(email=email)
        for phone in phones:
            if "id" in phone.keys():
                if ContactPhone.objects.filter(id=phone["id"]).exists():
                    contact_phone = ContactPhone.objects.get(id=phone["id"])
                    if contact_phone.phone != phone.get('phone', contact_phone.phone):
                        contact_phone.phone = phone.get('phone', contact_phone.phone)
                        contact_phone.save()
                    else:
                        continue
                else:
                    continue
            else:
                ContactPhone.objects.create(contact=contact_object, phone=phone.get('phone'))
        return instance
    
    class Meta:
        model = Contact
        fields = ('id', 'name', 'birthday', 'email', 'address', 'phones', 'user')

    def validate(self, data):
        date_delta = (datetime.now().date() - data['birthday']).days
        if len(data['name']) < 3:
            raise serializers.ValidationError("Name must be more than 3 characters")
        if date_delta < 0:
            raise serializers.ValidationError("Invalid birthday, you from future?")
        if date_delta > 36525:
            raise serializers.ValidationError("Invalid birthday, maximum contact age is 100 years")
        if len(data['address']) < 4:
            raise serializers.ValidationError("Address must be more than 4 characters")
        return data
        