from django.shortcuts import render,redirect
from .models import AgentAccount, Booking, GrantedBookings, House, HousePic, HouseRating, Room, HouseFeature, RoomPic, UserAccount
from .forms import AgentAccountForm, EditHouseForm, EditRoomForm, FeatureForm, HousePicForm, LoginForm, RatingForm, SearchForm, AddHouseForm, AddRoomForm, SignUpForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

def home(request):
    if request.user.is_authenticated:
        acc = UserAccount.objects.get(user=request.user)
        houses_list = House.objects.filter(allowed_sex=acc.sex).order_by('-date_listed')
        houses_list |= House.objects.filter(allowed_sex='b').order_by('-date_listed')
        top_rated = House.objects.all().order_by('-rating')
    else:
        houses_list = House.objects.all().order_by('-date_listed')
        top_rated = House.objects.all().order_by('-rating')
    sponsored = House.objects.filter(sponsored=True)

    paginator1 = Paginator(houses_list,5)
    page1 = request.GET.get('page1')
    houses = paginator1.get_page(page1)

    paginator2 = Paginator(top_rated,5)
    page2 = request.GET.get('page2')
    top_rated = paginator2.get_page(page2)

    paginator3 = Paginator(sponsored,5)
    page3 = request.GET.get('page3')
    sponsored = paginator3.get_page(page3)

    context = {
        'houses' : houses,
        'top_rated' : top_rated,
        'sponsored' : sponsored,
    }
    return render(request,'main/home.html',context)


def house_details(request,id):
    house = House.objects.get(id=id)
    features = HouseFeature.objects.filter(house=house)
    ratings = HouseRating.objects.filter(house=house)
    rooms = Room.objects.filter(house=house)
    form = RatingForm(request.POST or None)
    if request.user.is_authenticated:
        rated = HouseRating.objects.filter(house=house,rater=request.user)
    else:
        rated = ''
    if form.is_valid():
        if request.user.is_authenticated:
            rater = request.user
            if rated:
                return house_details(request,id)
        else:
            return house_details(request,id)
        comment = form.cleaned_data['comment']
        rating = form.cleaned_data['rating']
        rating = int(rating)
        new_rating, created = HouseRating.objects.get_or_create(house=house,rater=rater,rating=rating,comment=comment)
        if created:
            old_rating = house.rating
            num = HouseRating.objects.filter(house=house).count()
            new_rate = (house.rating + rating)/num
            house.rating = new_rate
            house.save()
        form = RatingForm()
        context = {
            'house' : house,
            'rooms' : rooms,
            'features' : features,
            'ratings' : ratings,
            'form' : form,
            'rated' : rated,
        }
        return render(request,'main/house_details.html',context)
    context = {
        'house' : house,
        'rooms' : rooms,
        'features' : features,
        'ratings' : ratings,
        'form' : form,
        'rated' : rated,
    }
    return render(request,'main/house_details.html',context)


def room_details(request,id):
    room = Room.objects.get(id=id)
    house = House.objects.get(id=room.house.id)
    pics = RoomPic.objects.filter(room=room)
    context = {
        'house' : house,
        'room' : room,
        'pics' : pics,
    }
    return render(request,'main/room_details.html',context)

def search(request):
    form = SearchForm(request.POST or None)
    sponsored = House.objects.filter(sponsored=True)
    if form.is_valid():
        query = form.cleaned_data['query']
        if request.user.is_authenticated:
            acc = UserAccount.objects.get(user=request.user)
            houses = House.objects.filter(location__icontains=query) & House.objects.filter(allowed_sex=acc.sex)
            houses |= House.objects.filter(location__icontains=query,allowed_sex='b')
        else:
            houses = House.objects.filter(location__icontains=query)
        sponsored = House.objects.filter(sponsored=True)
        count = len(houses)
        form = SearchForm(request.POST or None)
        context = {
            'form' : form,
            'houses' : houses,
            'sponsored' : sponsored,
            'count' : count
        }
        return render(request,'main/search.html',context)
    context = {
        'form' : form,
        'sponsored' : sponsored,
    }
    return render(request,'main/search.html',context)

@login_required(login_url='/login/')
def add_house(request):
    form = AddHouseForm(request.POST or None, request.FILES or None)
    agentaccount = AgentAccount.objects.get(user=request.user)
    houses = House.objects.filter(listed_by=agentaccount)
    if form.is_valid():
        sex = form.cleaned_data['allowed_sex']
        location = form.cleaned_data['location']
        house_address = form.cleaned_data['house_address']
        if form.cleaned_data['display_picture'] != None:
            pic = request.FILES['display_picture']
        new_house, created = House.objects.get_or_create(allowed_sex=sex,location=location,house_address=house_address,display_picture=pic,listed_by=agentaccount)
        roomform = AddRoomForm()
        agentaccount = AgentAccount.objects.get(user=request.user)
        houses = House.objects.filter(listed_by=agentaccount)
        context = {
            'house' : new_house,
            'form' : roomform,
            'houses' : houses,
        }
        return render(request,'main/add_rooms.html',context)
    context = {
        'form' : form,
        'houses' : houses
    }
    return render(request,'main/add_house.html',context)

@login_required(login_url='/login/')
def add_rooms(request,id):
    roomform = AddRoomForm(request.POST or None,request.FILES or None)
    house = House.objects.get(id=id)
    agentaccount = AgentAccount.objects.get(user=request.user)
    houses = House.objects.filter(listed_by=agentaccount)
    if roomform.is_valid():
        sex = roomform.cleaned_data['sex']
        if roomform.cleaned_data['display_picture']:
            display_picture = request.FILES['display_picture']
        number_of_beds = roomform.cleaned_data['number_of_beds']
        pricing = roomform.cleaned_data['pricing']
        new_room, created = Room.objects.get_or_create(house=house,sex=sex,display_picture=display_picture,number_of_beds=number_of_beds,pricing=pricing,available_beds=number_of_beds)
        roomform = AddRoomForm()
        url = 'add_rooms/' + str(house.id)
        return redirect(url)
    context = {
        'house' : house,
        'form' : roomform,
        'houses' : houses,
    }
    return render(request,'main/add_rooms.html',context)

@login_required(login_url='/login/')
def my_account(request):
    user = User.objects.get(id=request.user.id)
    user_account = UserAccount.objects.get(user=user)
    try:
        agent_account = AgentAccount.objects.get(user=user)
        houses = House.objects.filter(listed_by=agent_account)
        bookings = len(Booking.objects.filter(agent=agent_account,revoked=False))
    except:
        agent_account = ''
        houses = ''
        bookings = ''
    my_bookings = Booking.objects.filter(booker=user_account)
    context = {
        'user' : user,
        'user_account' : user_account,
        'agent_account' : agent_account,
        'houses' : houses,
        'bookings' : bookings,
        'my_bookings' : my_bookings,
    }
    return render(request,'main/myaccount.html',context)

@login_required(login_url='/login/')
def edit_account(request):
    user = request.user
    user_account = UserAccount.objects.get(user=user)
    agent_account = AgentAccount.objects.get(user=user)
    form = UserForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data['username']:
            user.username = form.cleaned_data['username']
        if form.cleaned_data['first_name']:
            user.first_name = form.cleaned_data['first_name']
        if form.cleaned_data['last_name']:
            user.last_name = form.cleaned_data['last_name']
        if form.cleaned_data['email']:
            user.email = form.cleaned_data['email']
        if form.cleaned_data['agent_name']:
            agent_account.agent_name = form.cleaned_data['agent_name']
        if form.cleaned_data['sex']:
            user_account.sex = form.cleaned_data['sex']
        user.save()
        user_account.save()
        agent_account.save()
        return my_account(request,user.id)
    context = {
        'form' : form,
    }
    return render(request,'main/edit_account.html',context)

@login_required(login_url='/login/')
def delete(request,id):
    house = House.objects.get(id=id)
    acc = AgentAccount.objects.get(user=request.user)
    if house.listed_by == acc:
        house.delete()
    else:
        return home(request)
    return my_account(request,request.user.id)

@login_required(login_url='/login/')
def edit_house(request,id):
    house = House.objects.get(id=id)
    rooms = Room.objects.filter(house=house)
    acc = AgentAccount.objects.get(user=request.user)
    if house.listed_by == acc:
        form = EditHouseForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['location']:
                house.location = form.cleaned_data['location']
            if form.cleaned_data['house_address']:
                house.house_address = form.cleaned_data['house_address']
            if form.cleaned_data['display_picture']:
                house.display_picture = request.FILES['display_picture']
            if form.cleaned_data['allowed_sex']:
                house.allowed_sex = form.cleaned_data['allowed_sex']
            house.save()
            form = EditHouseForm()
            return my_account(request,request.user.id)
    else:
        return home(request)
    context = {
        'form' : form,
        'house' : house,
        'rooms' : rooms,
    }
    return render(request,'main/edit_house.html',context)

@login_required(login_url='/login/')
def add_features(request,id):
    house = House.objects.get(id=id)
    acc = AgentAccount.objects.get(user=request.user)
    if house.listed_by == acc:
        form = FeatureForm(request.POST or None)
        featues = HouseFeature.objects.filter(house=house)
        if form.is_valid():
            feature = form.cleaned_data['feature']
            new_feature, created = HouseFeature.objects.get_or_create(house=house,feature=feature)
            new_feature.save()
            form = FeatureForm()
            context = {
                'house' : house,
                'form' : form,
                'features' : featues
            }
            return render(request,'main/add_features.html',context)
    context = {
        'house' : house,
        'form' : form,
        'features' : featues
    }
    return render(request,'main/add_features.html',context)

@login_required(login_url='/login/')
def add_pics(request,id):
    house = House.objects.get(id=id)
    acc = AgentAccount.objects.get(user=request.user)
    if house.listed_by == acc:
        form = HousePicForm(request.POST or None, request.FILES or None)
        pics = HousePic.objects.filter(house=house)
        if form.is_valid():
            if form.cleaned_data['image']:
                pic = request.FILES['image']
            house_pic, created = HousePic.objects.get_or_create(house=house,image=pic)
            house_pic.save()
            form = HousePicForm()
            context = {
                'house' : house,
                'form' : form,
                'pics' : pics,
            }
            return render(request,'main/add_pics.html',context)
    context = {
        'house' : house,
        'form' : form,
        'pics' : pics,
    }
    return render(request,'main/add_pics.html',context)

@login_required(login_url='/login/')
def delete_feature(request,id):
    f = HouseFeature.objects.get(id=id)
    house_id = f.house.id
    house = f.house
    acc = AgentAccount.objects.get(user=request.user)
    if house.listed_by == acc:
        f.delete()
        return add_features(request,house_id)
    else:
        return home(request)

@login_required(login_url='/login/')
def delete_pic(request,id):
    f = HousePic.objects.get(id=id)
    house_id = f.house.id
    house = f.house
    acc = AgentAccount.objects.get(user=request.user)
    if house.listed_by == acc:
        f.delete()
        return add_pics(request,house_id)
    else:
        return home(request)

def log_in(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET.get('next'))
    context = {
        'form' : form
    }
    return render(request,'main/login.html',context)

def signup(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        sex = form.cleaned_data['sex']
        password = make_password(form.cleaned_data['password'])
        new_user, created = User.objects.get_or_create(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
        new_acc, created = UserAccount.objects.get_or_create(user=new_user,sex=sex)
        return log_in(request)
    context ={
        'form' : form
    }
    return render(request,'main/signup.html',context)

@login_required(login_url='/login/')
def log_out(request):
    logout(request)
    return log_in(request)

@login_required(login_url='/login/')
def bookings(request):
    user = request.user
    acc = AgentAccount.objects.get(user=user)
    bookings = Booking.objects.filter(agent=acc,granted=False,revoked=False)
    context = {
        'bookings' : bookings,
    }
    return render(request,'main/bookings.html',context)

@login_required(login_url='/login/')
def get_room(request,id):
    room = Room.objects.get(id=id)
    house = House.objects.get(id=room.house.id)
    pics = RoomPic.objects.filter(room=room)
    user = request.user
    acc = UserAccount.objects.get(user=user)
    if room.available_beds > 0:
        new_bookings, created = Booking.objects.get_or_create(house=room.house,agent=room.house.listed_by,room=room,booker=acc)
    else:
        context = {
            'error_message' : 'No more available beds',
            'room' : room,
            'house' : house,
            'pics' : pics,
        }
        return render(request,'main/room_details.html',context)
    if created:
        context = {
            'created' : created,
            'room' : room,
            'house' : house,
            'pics' : pics,
        }
        return render(request,'main/room_details.html',context)
    else:
        context = {
            'error_message' : "Error occured: You may have booked the room alredy.",
            'room' : room,
            'house' : house,
            'pics' : pics,
        }
        return render(request,'main/room_details.html',context)

@login_required(login_url='/login/')
def check_bookings(request):
    user = request.user
    acc = UserAccount.objects.get(user=user)
    bookings = Booking.objects.filter(booker=acc)
    context = {
        'bookings' : bookings,
    }
    return render(request,'main/checkbookings.html',context)

@login_required(login_url='/login/')
def grant(request,id):
    booking = Booking.objects.get(id=id)
    acc = AgentAccount.objects.get(user=request.user)
    room = booking.room
    room.available_beds = room.available_beds - 1
    room.save()
    if booking.agent == acc:
        booking.granted = True
        new_granted, created = GrantedBookings.objects.get_or_create(booking=booking,user=booking.booker,agent=acc)
        new_granted.save()
        booking.save()
        return bookings(request)
    else:
        return home(request)

@login_required(login_url='/login/')
def create_agent(request):
    user = request.user
    form = AgentAccountForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['agent_name']
        number = form.cleaned_data['phone_number']
        new_agent, created = AgentAccount.objects.get_or_create(user=user,phone_number=number,agent_name=name)
        return my_account(request)
    context = {
        'form' : form,
    }
    return render(request,'main/create_agent.html',context)

@login_required(login_url='/login/')
def clear(request,id):
    user = request.user
    acc = AgentAccount.objects.get(user=user)
    house = House.objects.get(id=id)
    if house.listed_by != acc:
        return home(request)
    rooms = Room.objects.filter(house=house)
    for room in rooms:
        room.available_beds = room.number_of_beds
        room.save()
    return my_account(request)

@login_required(login_url='/login/')
def edit_room(request,id):
    form = EditRoomForm(request.POST or None,request.FILES or None)
    user = request.user
    room = Room.objects.get(id=id)
    house = room.house
    rooms = Room.objects.filter(house=house)
    acc = AgentAccount.objects.get(user=user)
    if room.house.listed_by != acc:
        return home(request)
    if form.is_valid():
        if form.cleaned_data['room_name']:
            room.room_name = form.cleaned_data['room_name']
        if form.cleaned_data['sex']:
            room.sex = form.cleaned_data['sex']
        if form.cleaned_data['number_of_beds']:
            room.number_of_beds = form.cleaned_data['number_of_beds']
        if form.cleaned_data['display_picture']:
            room.display_picture = request.FILES['display_picture']
        if form.cleaned_data['available']:
            room.available = form.cleaned_data['available']
        if form.cleaned_data['pricing']:
            room.pricing = form.cleaned_data['pricing']
        room.save()
        form = EditRoomForm()
        context = {
            'form' : form,
            'room' : room,
            'rooms' : rooms
        }
        return render(request,'main/edit_room.html',context)
    context = {
        'form' : form,
        'room' : room,
        'rooms' : rooms
    }
    return render(request,'main/edit_room.html',context)

@login_required(login_url='/login/')
def g_bookings(request):
    user = request.user
    acc = AgentAccount.objects.get(user=user)
    bookings = Booking.objects.filter(agent=acc,granted=True,revoked=False)
    context = {
        'bookings' : bookings,
    }
    return render(request,'main/g_bookings.html',context)

@login_required(login_url='/login/')
def revoke(request,id):
    booking = Booking.objects.get(id=id)
    user = request.user
    acc = AgentAccount.objects.get(user=user)
    if booking.agent != acc:
        return home(request)
    room = booking.room
    room.available_beds += 1
    room.save()
    booking.granted = False
    booking.revoked = True
    booking.save()
    return bookings(request)

@login_required(login_url='/login/')
def delete_booking(request,id):
    booking = Booking.objects.get(id=id)
    user = request.user
    acc = UserAccount.objects.get(user=user)
    if booking.booker != acc:
        return home(request)
    booking.delete()
    return check_bookings(request)