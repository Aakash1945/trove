from email.message import EmailMessage
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from gfg import settings
from django.core.mail import send_mail
from gfg import settings

def home(request):
    return render(request,"work/index.html")

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['pass1']

        user =authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,'work/index.html',{'fname': fname})

        else:
            messages.error(request,"Wrong Credentials!")
            return redirect('home')
        
    return render(request,"work/signin.html")

def signup(request):
    if request.method =="POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,'User name already exists! Please try some other user name')
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,'Email already exists')
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,'Username must be under 10 characters')
        
        if pass1 != pass2:
            messages.error(request,"password didn't match") 

        if not username.isalnum():
            messages.error(request,'Username must be Alpha-Numeric!')
            return redirect('home')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()

        messages.success(request,"Your account has been successfully created.")

        #WELCOME EMAIL
        subject="Welcome to TROVE-LOGIN!!"
        message="Hello"+myuser.first_name+"!!\n""Welcome to TROVE!!\nThankyou for visiting our website \nYour account has been successfully created LOGIN and enjoy our service.\n\nThanking you\nAakash"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)


        return redirect('signin')
    


    return render(request,"work/signup.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully!")
    return redirect('home')
     






