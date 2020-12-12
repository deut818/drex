from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.cache import cache
from django.conf import settings
from django_countries.fields import CountryField

import datetime
class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


class UserManager(BaseUserManager):
    def create_user(self, fname, lname, gender, city, country, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        DefaultProfilePicture = "/images/profile/default.png"
        if not email:
            raise ValueError('Users must have an email address')
        if not fname:
            raise ValueError('Users must have a first name')
        if not lname:
            raise ValueError('Users must have a last name')
        if not gender:
            raise ValueError('Users must have a gender')
        if not city:
            raise ValueError('Users must have a city name')
        if not country:
            raise ValueError('Users must have a country')

        user = self.model(
            fname=fname,
            lname=lname,
            gender=gender,
            city=city,
            country=country,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fname, lname, gender, city, country, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            fname, 
            lname, 
            gender, 
            city, 
            country, 
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.user_admin = '<i class="fas fa-check-circle" style="font-size:15px;color:rgb(46, 218, 12);"></i>'
        user.save(using=self._db)
        return users


class User(AbstractBaseUser):
    DefaultProfilePicture = "images/profile/avatar.png"
    DefaultCoverPhoto = "images/cover/background.jpg"
    GenderType = models.TextChoices("GenderType", "MALE FEMALE OTHER")
    fname = models.CharField(max_length=25, verbose_name="first name")
    lname = models.CharField(max_length=25, verbose_name="last name")
    profile_picture = models.ImageField(upload_to='images/profile',blank=True,default=DefaultProfilePicture)
    gender = models.CharField(choices=GenderType.choices, max_length=10)
    city = models.CharField(max_length=25, verbose_name="city name")
    country = CountryField(blank_label='(select country)')
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    cover_photo = models.ImageField(upload_to='images/cover',blank=True,default=DefaultCoverPhoto)
    date_of_birth = models.DateField()
    following = models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False)
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name="registration date", blank=True)
    username = models.SlugField(unique=True, verbose_name="username")
    user_admin = models.CharField(max_length=255, default='', blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'username', 'gender', 'city', 'country', 'date_of_birth']

    def get_absolute_url(self):
        return reverse('users:user-profile', kwargs={
            'pk':self.pk
        })

    def get_update_absolute_url(self):
        return reverse('users:user_update', kwargs={
            'pk':self.pk
        })
        
    
    def get_fullname(self):
        return "{} {} {}".format(self.fname, self.lname, self.user_admin)
        
    def __str__(self):
        return "{} {}".format(self.fname, self.lname)


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
