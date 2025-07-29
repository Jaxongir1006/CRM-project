from django.contrib.auth.models import BaseUserManager
from phonenumber_field.validators import validate_international_phonenumber

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        if not email:
            raise ValueError('The email must be set')
        if not phone_number:
            raise ValueError('The phone number must be set')
        
        email = self.normalize_email(email)

        if password is None:
            raise ValueError('The password must be set')
        if len(password) < 8:
            raise ValueError('The password must be at least 8 characters long')
        if len(password) > 16:
            raise ValueError('The password must be at most 16 characters long')
        if password.isalpha():
            raise ValueError('The password must contain at least one number')
        if password.isnumeric():
            raise ValueError('The password must contain at least one letter')

        try:
            validate_international_phonenumber(phone_number)
        except:
            raise ValueError('The phone number is not valid')

        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user  
    
    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, phone_number, password, **extra_fields)
    
    def login_user(self, login_input, password, **extra_fields):
        try:
            user = self.get(username=login_input) or \
            self.get(email=login_input) or \
            self.get(phone_number=login_input)
        except:
            return None

        if user.check_password(password):
            return user

        return None