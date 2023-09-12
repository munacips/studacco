from django.contrib import admin
from .models import AgentAccount, Booking, House,  HouseFeature, HousePic, HouseRating, Room, RoomPic, UserAccount

admin.site.register([AgentAccount,House,HouseFeature, HousePic,HouseRating,Room, RoomPic,UserAccount,Booking])