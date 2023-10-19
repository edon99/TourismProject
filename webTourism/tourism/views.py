from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.db.models import Avg
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login ,logout
from django.urls import reverse
from tourism.models import User, Location , LocationImage, Verification, Rating
from .forms import UserForm, LocationForm, VerificationForm, UserUpdateForm, LocationRating
from django.contrib import messages
from .serializers import UserSerializer,LocationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET','POST'])
def apiTest(request):
    locations = Location.objects.all()
    locationSerial = LocationSerializer(locations, many=True)
    return Response(locationSerial.data)

def LocationAPI(request):
    api_response = apiTest(request)
    data = api_response.data
    return render(request, 'tourism/api.html',{'locations':data})



def home(request):
    return render (request, 'tourism/home.html')

def signup(request):    
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')
        
    else:       
        form = UserForm() 
        
    return render(request, 'tourism/signup.html',{'form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:  
                return redirect('admin-dash') 
            else:
                return redirect('site-home') 
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'tourism/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def getVerified(request):
    user = request.user
    
    if request.method == 'POST':
        form = VerificationForm(request.POST,request.FILES)  # Pass POST data to the form
        if form.is_valid():
            verification = form.save(commit=False)
            verification.user = request.user  # Assign the user
            verification.save()
            messages.success(request, 'Your verification request is being processed')
            print("supposed to redirect to locations")
            return redirect('locations')
        print("not valid")
    else: 
        form = VerificationForm()

    return render(request, 'tourism/getVerified.html', {'user': user, 'form': form})

def locations(request):
    query = request.GET.get('query')
    locations = Location.objects.all()
    
    if query:
        locations = locations.filter(
            Q(title__icontains=query) | 
            Q(city__icontains=query) | 
            Q(places__icontains=query) 
        )
    cities = Location.objects.values_list('city', flat=True).distinct()
    return render(request, 'tourism/locations.html', {'locations': locations, 'cities': cities})


def newLocation(request):
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES)
        if form.is_valid():
            location = Location(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                summary=form.cleaned_data['summary'],
                guide=request.user,
                places=form.cleaned_data['places'],
                city=form.cleaned_data['city'],
                weather=form.cleaned_data['weather'],
                view=form.cleaned_data['view'],
                family_friendly=form.cleaned_data['family_friendly'],
                latitude=form.cleaned_data['latitude'],  # Get latitude from the form
                longitude=form.cleaned_data['longitude']
            )
            location.save()

            for image in request.FILES.getlist('images'):
                location_image = LocationImage(
                    location=location,
                    image=image
                )
                location_image.save()
            messages.success(request,'Location submitted and is being verified.')
            return redirect('locations')
    else:
        form = LocationForm()

    return render(request, 'tourism/newLocation.html',{'form':form})

def locationDetails(request, pk):
    location = Location.objects.get(id=pk)
    avg_rating = Rating.objects.filter(location=pk).aggregate(avg_rating=Avg('rating'))
    average_rating = avg_rating['avg_rating'] if avg_rating['avg_rating'] is not None else 0
    average_rating = round(average_rating, 1)
    return render(request, 'tourism/locationDetails.html',{'location':location,'average_rating':average_rating})

def locationRating(request, pk):
    location = Location.objects.get(id=pk)
    
    if request.method == 'POST':
        print("it is a post ting ")
        form = LocationRating(request.POST, request.FILES)
        if form.is_valid():
            print("is valid ")
            rating = form.save(commit=False)
            rating.user = request.user
            rating.location = location
            rating.save()
            return redirect('location-details',pk)
    else:
        print("not valid")
        form = LocationRating()

    return render(request, 'tourism/locationRating.html', {'form': form})

def profile(request,pk):
    profile = User.objects.get(id=pk)
    if profile.verified == True:
        verif = Verification.objects.get(user=pk)
    else:
        verif = None
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=profile)  # Pass POST data to the form
        
        if form.is_valid(): 
            profile = form.save()
            messages.success(request, 'User profile updated')
            profile_url = reverse('profile', args=[profile.id])
            return redirect(profile_url)          
    else: 
        form = UserUpdateForm(instance=profile)
    return render(request, 'tourism/profile.html',{'verif':verif,'profile':profile,'form':form})