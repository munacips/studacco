from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name="home"),
    path('house_details/<int:id>',views.house_details,name="house_details"),
    path('room_details/<int:id>',views.room_details,name="room_details"),
    path('search/',views.search,name="search"),
    path('add_house/',views.add_house,name="add_house"),
    path('add_rooms/<int:id>',views.add_rooms,name="add_rooms"),
    path('my_account/',views.my_account,name="my_account"),
    path('edit_account/',views.edit_account,name="edit_account"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('edit_house/<int:id>',views.edit_house,name="edit_house"),
    path('add_features/<int:id>',views.add_features,name="add_features"),
    path('add_pics/<int:id>',views.add_pics,name="add_pics"),
    path('delete_feature/<int:id>',views.delete_feature,name="delete_feature"),
    path('delete_pic/<int:id>',views.delete_pic,name="delete_pic"),
    path('bookings/',views.bookings,name="bookings"),
    path('book_room/<int:id>',views.get_room,name="get_room"),
    path('check_bookings/',views.check_bookings,name="check_bookings"),
    path('grant/<int:id>',views.grant,name="grant"),
    path('createagent/',views.create_agent,name="grant"),
    path('clear/<int:id>',views.clear,name="clear"),
    path('edit_room/<int:id>',views.edit_room,name="edit_room"),
    path('gbookings/',views.g_bookings,name="g_bookings"),
    path('revoke/<int:id>',views.revoke,name="revoke"),
    path('delete_booking/<int:id>',views.delete_booking,name="delete_bookin"),
    path('login/',views.log_in,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.log_out,name="logout")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)