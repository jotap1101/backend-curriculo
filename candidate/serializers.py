from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError
from uuid import UUID
from .models import *

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone_number', 'email']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'number', 'complement', 'neighborhood', 'zip_code', 'city']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'name', 'url']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

class CandidateSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    social_media = SocialMediaSerializer(many=True, required=False)

    class Meta:
        model = Candidate
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'cpf', 'rg', 'has_disability', 'disability_description', 'has_drivers_license', 'drivers_license_category', 'is_first_job', 'contacts', 'addresses', 'social_media', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True, 'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate_has_disability(self, value):
        if not value and self.initial_data.get('disability_description') is not None:
            raise DRFValidationError('Disability description is required when candidate has a disability.')
        
        return value
    
    def validate_disability_description(self, value):
        if self.initial_data.get('has_disability') and not value:
            raise DRFValidationError('Disability description is required when candidate has a disability.')
        
        return value
    
    def validate_has_drivers_license(self, value):
        if not value and self.initial_data.get('drivers_license_category') is not None:
            raise DRFValidationError('Drivers license category is required when candidate has a drivers license.')
        
        return value
    
    def validate_drivers_license_category(self, value):
        if self.initial_data.get('has_drivers_license') and not value:
            raise DRFValidationError('Drivers license category is required when candidate has a drivers license.')
        
        return value
    
    def validate_is_first_job(self, value):
        if value and self.initial_data.get('is_currently_employed'):
            raise DRFValidationError('Is currently employed is not allowed when candidate is a first jobber.')
        
        return value

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', None)
        addresses_data = validated_data.pop('addresses', None)
        social_media_data = validated_data.pop('social_media', None)

        with transaction.atomic():
            candidate = Candidate.objects.create(**validated_data)

            for contact_data in contacts_data:
                Contact.objects.create(candidate=candidate, **contact_data)

            for address_data in addresses_data:
                Address.objects.create(candidate=candidate, **address_data)

            for social_media_data in social_media_data:
                SocialMedia.objects.create(candidate=candidate, **social_media_data)

        return candidate
    
    def update(self, instance, validated_data):
        related_fields = ['contacts', 'addresses', 'social_media']

        with transaction.atomic():
            related_data = {field: validated_data.pop(field, None) for field in related_fields}

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if related_data['contacts'] is not None:
                existing_ids = []

                for contact_data in related_data['contacts']:
                    contact_id = contact_data.pop('id', None)

                    if contact_id:
                        contact = Contact.objects.get(id=contact_id, candidate=instance)

                        for field in ['phone_number', 'email']:
                            if field not in contact_data:
                                contact_data[field] = getattr(contact, field)

                        for key, value in contact_data.items():
                            setattr(contact, key, value)

                        contact.save()
                        existing_ids.append(contact_id)
                    else:
                        contact = Contact.objects.create(candidate=instance, **contact_data)

                        existing_ids.append(contact.id)

                instance.contacts.exclude(id__in=existing_ids).delete()

            if related_data['addresses'] is not None:
                existing_ids = []

                for address_data in related_data['addresses']:
                    address_id = address_data.pop('id', None)

                    if address_id:
                        address = Address.objects.get(id=address_id, candidate=instance)

                        for field in ['street', 'number', 'complement', 'neighborhood', 'zip_code', 'city']:
                            if field not in address_data:
                                address_data[field] = getattr(address, field)

                        for key, value in address_data.items():
                            setattr(address, key, value)

                        address.save()
                        existing_ids.append(address_id)
                    else:
                        address = Address.objects.create(candidate=instance, **address_data)

                        existing_ids.append(address.id)

                instance.addresses.exclude(id__in=existing_ids).delete()

            if related_data['social_media'] is not None:
                existing_ids = []

                for social_media_data in related_data['social_media']:
                    social_media_id = social_media_data.pop('id', None)

                    if social_media_id:
                        social_media = SocialMedia.objects.get(id=social_media_id, candidate=instance)

                        for field in ['name', 'url']:
                            if field not in social_media_data:
                                social_media_data[field] = getattr(social_media, field)

                        for key, value in social_media_data.items():
                            setattr(social_media, key, value)

                        social_media.save()
                        existing_ids.append(social_media_id)
                    else:
                        social_media = SocialMedia.objects.create(candidate=instance, **social_media_data)

                        existing_ids.append(social_media.id)

                instance.social_media.exclude(id__in=existing_ids).delete()

        return instance