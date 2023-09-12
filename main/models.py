from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from math import floor


class UserAccount(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    sex = models.CharField(max_length=1,choices=[('m','Male'),('f','Female')])
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class AgentAccount(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.agent_name


class House(models.Model):
    listed_by = models.ForeignKey(AgentAccount,on_delete=models.CASCADE,null=True)
    allowed_sex = models.CharField(max_length=1,choices=[('m','Male'),('f','Female'),('b','Both')])
    location = models.CharField(max_length=50)
    house_address = models.CharField(max_length=200)
    display_picture = models.ImageField(upload_to='dp/houses')
    rating = models.DecimalField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)],decimal_places=1,max_digits=2)
    lived_in = models.ManyToManyField(UserAccount,related_name="lived_in_house",blank=True)
    sponsored =  models.BooleanField(default=False)
    date_listed = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.location + ' ' + self.house_address

    def get_rating(self):
        return floor(self.rating)

    def rating_iter(self):
        return [None] * floor(self.rating)


class HouseFeature(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE)
    feature = models.CharField(max_length=100)

    def __str__(self):
        return self.feature


class Room(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100,default="No name")
    sex = models.CharField(max_length=1,choices=[('m','Male'),('f','Female')])
    display_picture = models.ImageField(upload_to='dp/rooms/')
    number_of_beds = models.IntegerField(validators=[MinValueValidator(0)])
    available_beds = models.IntegerField(validators=[MinValueValidator(0)])
    available = models.BooleanField(default=True)
    pricing = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.room_name


class HousePic(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pics/houses/')


class RoomPic(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pics/rooms/')


class HouseRating(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE)
    rater = models.ForeignKey(User,on_delete=models.SET('deleted'))
    rating = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    comment = models.TextField(blank=True,null=True)

    
class Booking(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE)
    agent = models.ForeignKey(AgentAccount,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.SET('deleted'))
    booker = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    granted = models.BooleanField(default=False)
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return self.booker.user.username + ', ' + self.house.__str__() + ', ' + str(self.room) + ': ' + str(self.date_booked)

    
class GrantedBookings(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    agent = models.ForeignKey(AgentAccount,on_delete=models.SET('deleted'))
    revoked = models.BooleanField(default=False)
