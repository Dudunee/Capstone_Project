from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """
    def create_user(self, email, password):
        """
        Creates and returns a user with an email and password.
        """
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password):
        """
        Creates and returns a superuser.
        """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractUser):
    """
    Custom User model where the email is used as the unique identifier instead of a username.
    """
    email = models.EmailField(unique=True, max_length= 255)
    username =  models.CharField(unique=True, max_length= 15)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= [] # Username is not required for creating a user