from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url ='/login/')
def receipes(request):
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get('image')
        name = data.get('name')
        description = data.get('description')
        
        Receipe.objects.create(
            image=image,
            name=name,
            description=description
        )
        return redirect('/')
    
    queryset = Receipe.objects.all()


    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains = request.GET.get('search'))


    context = {'receipes': queryset}
    return render(request, 'receipes.html',context)

def update_receipe(request,id):
    queryset = Receipe.objects.get(id=id)
    if request.method =="POST":
        data = request.POST
        image = request.FILES.get('image')
        name = data.get('name')
        description = data.get('description')
        
        
        queryset.name = name 
        queryset.description = description
        
        if image:
            queryset.image = image

        queryset.save()    
        return redirect('/')

    context = {'receipes': queryset}
    return render(request, 'update_receipes.html',context)



def delete_receipe(request,id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        if not User.objects.filter(username = username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login/')

        user = authenticate(username = username,password = password)
        
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')


    return render(request , 'login.html')






def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = User.objects.filter(username = username)
        if user.exists():
            messages.warning(request, "Username already Exists!!")
            return redirect('/register/')


        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username  
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created Successfuly!!")
        return redirect('/register/')

    return render(request,'register.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')
