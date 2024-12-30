from rest_framework import serializers
from .models import PersonInfo, StreemDetails, Address, Education, ProberProfileModel


# Serializer for PersonInfo Model
class PersonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonInfo
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'dob']


# Serializer for StreemDetails Model
class StreemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreemDetails
        fields = ['id', 'main_probe', 'interested_probe']


# Serializer for Address Model
class AddressSerializer(serializers.ModelSerializer):
    person = PersonInfoSerializer(read_only=True)  # Nested serializer for PersonInfo

    class Meta:
        model = Address
        fields = ['id', 'person', 'country', 'state', 'city', 'zip_code']


# Serializer for Education Model
class EducationSerializer(serializers.ModelSerializer):
    person = PersonInfoSerializer(read_only=True)  # Nested serializer for PersonInfo

    class Meta:
        model = Education
        fields = ['id', 'person', 'higher_education', 'pass_out_year', 'university_college']


# Serializer for ProberProfileModel
class ProberProfileModelSerializer(serializers.ModelSerializer):
    person_info = PersonInfoSerializer()  # Nested serializer for PersonInfo
    streem_details = StreemDetailsSerializer()  # Nested serializer for StreemDetails
    address = AddressSerializer(read_only=True)  # Nested serializer for Address
    education = EducationSerializer(read_only=True)  # Nested serializer for Education

    class Meta:
        model = ProberProfileModel
        fields = [
            'id', 'person_info', 'streem_details', 'address', 'education',
            'message', 'enquiry_timestamp', 'email_sent', 'email_sent_at',
            'email_error_message', 'whatsapp_sent', 'whatsapp_sent_at',
            'whatsapp_error_message'
        ]

    def create(self, validated_data):
        # Extract nested data
        person_info_data = validated_data.pop('person_info')
        streem_details_data = validated_data.pop('streem_details')
        address_data = validated_data.pop('address', None)
        education_data = validated_data.pop('education', None)

        # Create related objects first
        person_info = PersonInfo.objects.create(**person_info_data)
        streem_details = StreemDetails.objects.create(**streem_details_data)

        if address_data:
            address = Address.objects.create(person=person_info, **address_data)
        else:
            address = None

        if education_data:
            education = Education.objects.create(person=person_info, **education_data)
        else:
            education = None

        # Now create the ProberProfileModel
        prober_profile = ProberProfileModel.objects.create(
            person_info=person_info,
            streem_details=streem_details,
            address=address,
            education=education,
            **validated_data  # Include other fields like message, email_sent, etc.
        )

        return prober_profile

    def update(self, instance, validated_data):
        # Update person_info
        person_info_data = validated_data.pop('person_info', None)
        if person_info_data:
            for attr, value in person_info_data.items():
                setattr(instance.person_info, attr, value)
            instance.person_info.save()

        # Update streem_details
        streem_details_data = validated_data.pop('streem_details', None)
        if streem_details_data:
            for attr, value in streem_details_data.items():
                setattr(instance.streem_details, attr, value)
            instance.streem_details.save()

        # Update address if present
        address_data = validated_data.pop('address', None)
        if address_data:
            if instance.address:
                for attr, value in address_data.items():
                    setattr(instance.address, attr, value)
                instance.address.save()
            else:
                instance.address = Address.objects.create(person=instance.person_info, **address_data)

        # Update education if present
        education_data = validated_data.pop('education', None)
        if education_data:
            if instance.education:
                for attr, value in education_data.items():
                    setattr(instance.education, attr, value)
                instance.education.save()
            else:
                instance.education = Education.objects.create(person=instance.person_info, **education_data)

        # Update other fields in ProberProfileModel
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the main instance
        instance.save()

        return instance