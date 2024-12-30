from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
from rest_framework import generics
from .models import ProberProfileModel
from .serializers import ProberProfileModelSerializer


# List view to get all ProberProfiles
class ProberProfileListView(generics.ListCreateAPIView):
    """
        Once user submits a form it will call this view and execute the method perform_create()
    """
    queryset = ProberProfileModel.objects.all()
    serializer_class = ProberProfileModelSerializer

    def perform_create(self, serializer):
        # Save the ProberProfileModel instance to the database
        prober_profile = serializer.save()

        # After saving the profile, send acknowledgment email
        self.send_acknowledgment_email(prober_profile)

    def send_acknowledgment_email(self, prober_profile):
        # Send acknowledgment email to the user (enrolled person)
        subject = 'Thank you for your Enrollment!'
        message = f"""
        Dear {prober_profile.person_info.first_name} {prober_profile.person_info.last_name},

        Thank you for enrolling with us! We have received your details and will get in touch with you shortly.

        Your Enrollment Details:
        Name: {prober_profile.person_info.first_name} {prober_profile.person_info.last_name}
        Email: {prober_profile.person_info.email}
        Phone: {prober_profile.person_info.phone}

        We look forward to helping you with your journey!

        Best Regards,
        Your Company Name
        """

        recipient_list = [prober_profile.person_info.email]  # Send to the user's email address
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    def create(self, request, *args, **kwargs):
        # Customize the response if needed, after creating the object
        response = super().create(request, *args, **kwargs)
        return response


# Detail view to get a specific ProberProfile by ID
class ProberProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProberProfileModel.objects.all()
    serializer_class = ProberProfileModelSerializer
