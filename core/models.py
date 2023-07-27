from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    def default_birthday():
        return timezone.datetime(1970, 1, 1).date()
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    birthday = models.DateField(default=default_birthday)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    premium = models.BooleanField(default=False)
    location = models.CharField(max_length=100, default='London')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def age(self):
        today = timezone.now().date()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age

    def clean(self):
        super().clean()
        if self.age() < 18:
            raise ValidationError("Users below 18 years are not allowed.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    # Add related names to fix the conflicts with 
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )



#### To go dynamic , uncomment the code below and comment out the one above, This will calculate the birthday as per current date and the birth day entered before saving the user 


# class User(AbstractBaseUser, PermissionsMixin):
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     )
#     def default_birthday():
#         return timezone.datetime(1970, 1, 1).date()
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     birthday = models.DateField()
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
#     premium = models.BooleanField(default=False)
#     location = models.CharField(max_length=100, default='London')
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def age(self):
#         today = timezone.now().date()
#         age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
#         return age

#     def clean(self):
#         super().clean()
#         if self.age() < 18:
#             raise ValidationError("Users below 18 years are not allowed.")

#     def save(self, *args, **kwargs):
#         # Calculate default birthday based on the current year and the user's age
#         default_birthday = timezone.now().date().replace(year=timezone.now().date().year - self.age())
#         if not self.birthday:
#             self.birthday = default_birthday
#         super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = 'user'
#         verbose_name_plural = 'users'

#     # Add related names to fix the conflicts with 
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_set',
#         blank=True,
#     )
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_set',
#         blank=True,
#     )
