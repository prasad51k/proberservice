# services/app1/tests.py
from django.test import TestCase
from services.prober.models import PersonInfo, StreemDetails, Address, Education, ProberProfileModel
from datetime import date

class ProberProfileTestCase(TestCase):

    def setUp(self):
        # Create a PersonInfo instance
        self.person = PersonInfo.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            dob="1990-01-01"
        )

        # Create other related instances
        self.streem = StreemDetails.objects.create(
            main_probe="Science",
            interested_probe="Physics"
        )

        self.address = Address.objects.create(
            person=self.person,
            country="USA",
            state="California",
            city="San Francisco",
            zip_code="94105"
        )

        self.education = Education.objects.create(
            person=self.person,
            higher_education="Masters",
            pass_out_year="2015",
            university_college="Stanford University"
        )

        # Create ProberProfileModel instance
        self.profile = ProberProfileModel.objects.create(
            person_info=self.person,
            streem_details=self.streem,
            address=self.address,
            education=self.education,
            message="This is an optional message"
        )

    def test_prober_profile_creation(self):
        # Test that the ProberProfileModel instance was created correctly
        self.assertEqual(self.profile.person_info.first_name, "John")
        self.assertEqual(self.profile.streem_details.main_probe, "Science")
        self.assertEqual(self.profile.address.city, "San Francisco")
        self.assertEqual(self.profile.education.university_college, "Stanford University")
        self.assertEqual(self.profile.message, "This is an optional message")

    def test_person_info_str_method(self):
        self.assertEqual(str(self.person), "John Doe")