from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ALGERIA_CITIES = [
    ("Adrar", "Adrar"),
    ("Aflou", "Aflou"),
    ("Aïn Témouchent", "Aïn Témouchent"),
    ("Akbou", "Akbou"),
    ("Alger", "Algiers"),
    ("Annaba", "Annaba"),
    ("Batna", "Batna"),
    ("Béchar", "Béchar"),
    ("Béjaïa", "Béjaïa"),
    ("Béni Abbès", "Béni Abbès"),  
    ("Birkhadem", "Birkhadem"),
    ("Blida", "Blida"),
    ("Bordj Bou Arreridj", "Bordj Bou Arreridj"),
    ("Bou Saâda", "Bou Saâda"),
    ("Bouira", "Bouira"),
    ("Boumerdès", "Boumerdès"),
    ("Chlef", "Chlef"),
    ("Constantine", "Constantine"),
    ("Djelfa", "Djelfa"),
    ("El Eulma", "El Eulma"),
    ("El Harrach", "El Harrach"),
    ("El Khroub", "El Khroub"),
    ("El Oued", "El Oued"),
    ("El Tarf", "El Tarf"),
    ("Guelma", "Guelma"),
    ("Jijel", "Jijel"),
    ("Khenchela", "Khenchela"),
    ("Laghouat", "Laghouat"),
    ("M'sila", "M'sila"),
    ("Médéa", "Médéa"),
    ("Mostaganem", "Mostaganem"),
    ("Oran", "Oran"),
    ("Ouargla", "Ouargla"),
    ("Relizane", "Relizane"),
    ("Sétif", "Sétif"),
    ("Sidi Bel Abbès", "Sidi Bel Abbès"),
    ("Skikda", "Skikda"),
    ("Tamanrasset", "Tamanrasset"),
    ("Tébessa", "Tébessa"),
    ("Tiaret", "Tiaret"),
    ("Timimoun", "Timimoun"),
    ("Tipasa", "Tipasa"),
    ("Tizi Ouzou", "Tizi Ouzou"),
    ("Tlemcen", "Tlemcen"),
]

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN ="ADMIN", 'Admin'
        USER ="USER", 'User'
    base_role = Role.USER
    role = models.CharField(max_length=50, choices=Role.choices, default=base_role)
    verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
            return super().save(*args, **kwargs)
    

class Verification(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     idCard = models.ImageField(upload_to='idCard_pics')
     city = models.CharField(max_length=30, choices=ALGERIA_CITIES,null=True)
     address = models.CharField(max_length=50,null=True)
     phone_number = models.CharField(max_length=15 , null=True)
     created_at = models.DateTimeField(default=timezone.now)
     VERIFICATION_STATE = [
          ('Pending','Pending'),
          ('Accepted','Accepted'),
          ('Refused','Refused')  
     ]
     state = models.CharField(max_length=10,choices=VERIFICATION_STATE,default='Pending')
  

class Location(models.Model):
    approved = models.BooleanField(default=False)
    title = models.CharField(max_length=40)
    summary = models.CharField(max_length=50,default=None)
    description = models.TextField()
    guide = models.ForeignKey(User, on_delete=models.CASCADE)
    PLACE_CHOICES = [
        ('Beach', 'Beach'),
        ('Park', 'Park'),
        ('Forest', 'Forest'),
        ('Lake', 'Lake'),
        ('City', 'City'),
        ('Restaurant', 'Restaurant'),
    ]
    WEATHER_COND = [
         ('Cold','cold'),
         ('Warm', 'warm'),
    ]
    
    city = models.CharField(max_length=30, choices=ALGERIA_CITIES, default=None)
    weather = models.CharField(max_length=20,choices=WEATHER_COND, default=None)
    images = models.ManyToManyField('LocationImage',related_name='locations')
    places = models.CharField(max_length=30,choices=PLACE_CHOICES,default=None)
    location_rating = models.ForeignKey('Rating', on_delete=models.CASCADE,related_name='locations',null=True)
    popular = models.BooleanField(default=False)
    family_friendly = models.BooleanField(default=False)
    view = models.BooleanField(default=False)
    latitude = models.CharField(max_length=50, default=0)
    longitude = models.CharField(max_length=50, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        self.description = self.description.capitalize()
        self.title = self.title.capitalize()
        self.summary = self.summary.capitalize()
        super(Location, self).save(*args, **kwargs)

class Rating(models.Model):
     location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='ratings')
     proof = models.ImageField(upload_to='ratingProof_pics',null=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
     comment = models.TextField()
     date = models.DateTimeField(default=timezone.now)




class LocationImage(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_images', null=True)
    image = models.ImageField(upload_to='location_pics')

    def __str__(self):
        return self.image.url

