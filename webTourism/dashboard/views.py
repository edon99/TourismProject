from django.http import JsonResponse
from django.shortcuts import redirect, render
from tourism.models import Verification, User
from django.contrib import messages

# Create your views here.

def adminDash(request):
    return render(request,'dashboard/adminDash.html')

def users(request):
    requests = Verification.objects.all().order_by('-created_at')
    
    return render(request,'dashboard/adminUsers.html',{'requests':requests})

def userDetails(request,pk):
    verif = Verification.objects.get(user=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        verif = Verification.objects.get(user=pk)
        user = User.objects.get(id=pk)
        if action == 'accept':
            verif.state = 'Accepted'
            verif.save()
            user.verified = True
            user.save()
            messages.success(request,'User '+str(user)+' has been accepted' )
            return redirect ('admin-users')
        elif action == 'refuse':
            verif.state = 'Refused'
            verif.save()
            messages.success(request,'User '+str(user)+' has been refused' )
            return redirect ('admin-users')
            
        
    return render(request,'dashboard/userDetails.html',{'verif':verif})


    