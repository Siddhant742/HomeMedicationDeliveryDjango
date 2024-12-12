from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, EmailValidator
from django.utils import timezone

class User(AbstractUser):
   phone_number = models.CharField(max_length=15, blank=True, null=True)
   is_verified = models.BooleanField(default=False)
   verification_status = models.CharField(
       max_length=20, 
       choices=[
           ('not_submitted', 'Not Submitted'),
           ('pending', 'Pending'),
           ('verified', 'Verified'),
           ('rejected', 'Rejected')
       ],
       default='not_submitted'
   )
   front_id_image = models.ImageField(
       upload_to='identity_docs/front/',
       validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
       null=True,
       blank=True
   )
   back_id_image = models.ImageField(
       upload_to='identity_docs/back/',
       validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
       null=True,
       blank=True
   )

   class Meta:
       db_table = 'auth_user'

