from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.


#rooms = [
#    {'id':1, 'name':'Lets learn Python'},
#    {'id':2, 'name':'Design with me'},
#    {'id':3, 'name':'Frontend developer'},
#]

def loginPage(request):

    #making sure the page is login 
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # check the user exist 
        try:

            user = User.objects.get(username=username)
        except:

            messages.error(request, 'User does not exist')

        # check credential

        user = authenticate(request, username=username, password=password)


        if user is not None:
            #login creates a session in the database and the browser 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User OR password does not exist')
        
    context = {'page': page}
    
    return render(request, 'base/login_register.html', context)

#logout delete the session in the browser 

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

    #UserCreationForm django built 
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #to be able to clean this date in case user write lowercase
            #or other mistakes i want to capture those mistakes before
            # saving the data 
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:

            messages.error(request, 'An error occurred during registration ')
    return render(request, 'base/login_register.html', {'form':form})

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # topic__name__ that's the way you add others variable
    #rooms = Room.objects.filter(topic__name__icontains=q)

#Q with Q can write 'and' or 'or' & |

    rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
    )

    # get all the topics 
    topics = Topic.objects.all()
    room_count = rooms.count()

    # this is for getting just the messages filter by the browse topics 
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))


    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count,
               'room_messages':room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):

    room = Room.objects.get(id=pk)

    # for i in rooms:

        # if i['id'] == int(pk):
        #     room = i 
    # .message_set.all() we can queary child objects the child is class Message room
    # all we need to do is take the name of the child (class) and write in lowercase
    #room_messages = room.message_set.all().order_by('-created')
    room_messages = room.message_set.all()
    #since this is a many to many relationship I don't need the _set 
    participants = room.participants.all()
    if request.method == 'POST':

        message = Message.objects.create(

            user = request.user,
            room = room,
            #this body is the name of the input we have in room.html 
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages':room_messages, 
               'participants':participants}

    return render(request, 'base/room.html', context)



#------------CRUD

#----Create

def userProfile(request, pk):
    #getting user pk
    user = User.objects.get(id=pk)

    # we can get children of the specific obj by doing the moddel name and 
    # _set
    rooms = user.room_set.all()
    room_messages = user.message_set.all()

    topics = Topic.objects.all()

    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 
               'topics':topics}

    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    #we have the form check forms.py 
    form = RoomForm()
    #send the POST data
    if request.method == 'POST':
        #add the data to the form
        form = RoomForm(request.POST)
        #check is valid
        if form.is_valid():
            #save the data
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

#----Update

@login_required(login_url='login')
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)
    #instance is for load the info it was there 
    form = RoomForm(instance=room)

    #this prevents a user that knows the url for one room can update things
    #without owner(s) permition

    if request.user != room.host:

        return HttpResponse("You don't have credentials")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

#---- Delete 

@login_required(login_url='login')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:

        return HttpResponse("You don't have credentials")

    if request.method == 'POST':

        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):

    message = Message.objects.get(id=pk)

    if request.user != message.user:

        return HttpResponse("You don't have credentials")

    if request.method == 'POST':

        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})
