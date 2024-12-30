from django.db import models


class PersonInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)  # Optional field

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StreemDetails(models.Model):
    main_probe = models.CharField(max_length=255)
    interested_probe = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.main_probe} - {self.interested_probe}"


class Address(models.Model):
    person = models.OneToOneField(PersonInfo, related_name='address', on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"


class Education(models.Model):
    person = models.OneToOneField(PersonInfo, related_name='education', on_delete=models.CASCADE, null=True, blank=True)
    higher_education = models.CharField(max_length=255, null=True, blank=True)
    pass_out_year = models.CharField(max_length=4, null=True, blank=True)
    university_college = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.higher_education} - {self.university_college}"


class ProberProfileModel(models.Model):
    person_info = models.OneToOneField(PersonInfo, on_delete=models.CASCADE)
    streem_details = models.OneToOneField(StreemDetails, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    education = models.OneToOneField(Education, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    # Enquiry submission timestamp
    enquiry_timestamp = models.DateTimeField(auto_now_add=True)

    # Fields for email and WhatsApp notification status
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    email_error_message = models.TextField(null=True, blank=True)

    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True)
    whatsapp_error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.person_info.first_name} {self.person_info.last_name}"

