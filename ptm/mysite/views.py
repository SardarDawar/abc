from django.shortcuts import render
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .tokens import account_activation_token
from rest_framework import generics

from .forms import *
from .models import *
from .serializers import *


def home(request):
    #if request.user.is_authenticated and  not request.user.is_superuser:
    if request.user.is_authenticated:
        try:
            profile = profileModel.objects.get(user=request.user)
        except:
            profile=None
        if profile.approve == True:
            context = {
                'profile' : profile,
                'section' : 'dashboard'
            }
            if profile.Teacher_or_Parent =='Parent':
                return render(request, 'parent/homeparent.html', context)
            if profile.Teacher_or_Parent =='Teacher':
                return render(request, 'teacher/hometeacher.html', context)
        else:   
            return render(request, 'mysite/Approve.html')
    return render(request, 'mysite/home.html')

def contact(request):
    if request.method!='POST':
        form = contactForm()
    else:
        form = contactForm(request.POST)
        if form.is_valid():
            mail_subject = 'Contact -- By -- ' + form.cleaned_data.get('userName')
            to_email = settings.EMAIL_HOST_USER
            message = form.cleaned_data.get('body')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('home')
    
    context= {'form' : form}
    return render(request, 'mysite/contact.html', context)

def login_user(request):
    if request.method!= 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Usename or password may have been entered incorrectly.')
                return redirect('login')
    
    return render(request, 'mysite/login.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('home')




    
def register_user(request):
    if request.method!='POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email']
            user.save()
            profile = profileModel.objects.create(user = user)
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.Teacher_or_Parent = form_2.cleaned_data['Teacher_or_Parent']
            profile.save()
            current_site = get_current_site(request)
            message = render_to_string('mysite/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'mysite/acc_active_email_confirm.html')
    return render(request, 'mysite/register.html', {'form' : form, 'form_2' : form_2})




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.warning(request, 'User has been activated')
        return redirect('login')
    else:
        messages.warning(request, 'Invalid Activation Link')
        return redirect('register')

# @login_required
# def edit_profile(request):
#     try:
#         profile = profileModel.objects.get(user=request.user)
#     except:
#         profile=None
#     context={
#         'profile' : profile,
#         'section' : "editProfile"
#     }
#     return render(request, 'mysite/editProfile.html', context)


@login_required()
def edit_profile(request):
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
    else:
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated.')
            return redirect('home')
    try:
        profile=profileModel.objects.get(user=request.user)
    except:
        profile=None
    context={
        'profile' : profile,
        'section' : "editProfile",
        'form' : form
    }
    return render(request, 'mysite/editProfile.html',context)


@login_required()
def edit_profile_user(request):
    try:
        profile=profileModel.objects.get(user=request.user)
    except:
        profile=profileModel.objects.create(user=request.user)
    if request.method!='POST':
        if profile:
            form = profileInformForm(instance = profile)
        else:
            form = profileInformForm()
    else:
        if profile:
            form = profileInformForm(request.POST, instance = profile)
        else:
            form = profileInformForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated.')
            return redirect('home')
    try:
        profile=profileModel.objects.get(user=request.user)
    except:
        profile=None
    context={
        'profile' : profile,
        'section' : "editProfile",
        'form' : form
    }
    return render(request, 'mysite/editProfileUser.html',context)


@login_required()
def change_password(request):
    if request.method!='POST':
        form = PasswordChangeForm(user = request.user)
    else:
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been updated.')
            return redirect('home')
    return render(request, 'mysite/change_password.html' , {'form': form, 'section' : "editProfile"})




# PARENTS AND PROGRAM  ...........................
#childs .........................
def childview(request):
    form=childform()
    if request.method == 'POST':
        form = childform(request.POST,request.FILES)
        if form.is_valid:
            new= form.save(commit=False)
            new.parent = request.user
            new.save()
    
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request,'parent/childform.html',context)

def childviewedit(request,id):
    childimage=child.objects.get(id=id)
    form=childform(instance=childimage)
    if request.method == 'POST':
        form = childform(request.POST,request.FILES,instance=childimage)
        if form.is_valid:
            new= form.save(commit=False)
            new.parent = request.user
            new.save()
    
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request,'parent/childformedit.html',context)

def childlist(request,user):
    obj = child.objects.filter(parent=user)
    context = {
        'obj': obj,
    }
    return render(request,'parent/childlist.html',context)

def childlistprofile(request,user):
    obj = child.objects.filter(parent=user)
    context = {
        'obj': obj,
    }
    return render(request,'parent/childlistprofile.html',context)
#attendence.........................
def attenndenceview(request,id):
    name=child.objects.get(id=id)
    form=attendenceform()
    if request.method == 'POST':
        form = attendenceform(request.POST)
        if form.is_valid:
            new= form.save(commit=False)
            new.parent = request.user
            new.classname=name.classname
            new.name=name
            form.save()
    
            return redirect('home')
    context = {
        'form': form,
        
    }
    return render(request,'parent/attendenceform.html',context)

def attendencelist(request,user):
    obj = child.objects.filter(parent=user)
    contact=profileModel.objects.get(user=user)
    att = attendence.objects.filter(parent=user)
    context = {
        'obj': obj,
        'contact':contact,
     
    }
    return render(request,'parent/attendencelist.html',context)

def picklist(request,user):
    obj = child.objects.filter(parent=user)
    att = attendence.objects.filter(parent=user)
    context = {
      
        'obj':att
    }
    return render(request,'parent/picklist.html',context)

def attendenceformedit(request, id):
    obj = attendence.objects.get(id=id)
    form1 = attendenceform(instance=obj)
    if request.method == 'POST':
        form1 = attendenceform(request.POST, instance=obj)
        if form1.is_valid():
            new= form1.save(commit=False)
            new.parent = request.user

            form1.save()
    
            return redirect('home')
    print(form1)    
    context = {
        'form1': form1,
        'obj': obj,
    }
    return render(request,'parent/attendenceformedit.html',context)


#child stories ......................
def childstorieslistparent(request,user):
    obj = child.objects.filter(parent=user)
    context = {
        'obj': obj,
    }
    return render(request,'parent/childstorieslist.html',context)


def childstoriesviewparent(request,id):
    chi = child.objects.get(id=id)
    obj = child_stories.objects.filter(name=chi)

    print(obj)
    context = {  
        'obj':obj
    }
    return render(request,'parent/childstoriesview.html',context)
# Notifications ..................
from django.db.models import Q
def notifcationlistparent(request):
    cla=child.objects.filter(parent=request.user)
    obj = Notifications.objects.all()
   
    #for i in cla[0]:
    obj = Notifications.objects.filter(Q(classname=cla[0].classname))
    #|
    #Q(classname=cla[1].classname))
    print(obj)
    context = {
        'obj': obj,
     
    }
    return render(request,'parent/notification.html',context)

# leaves...............
def leavesview(request):
    form=leavesform()
    if request.method == 'POST':
        form = leavesform(request.POST,request.FILES)
        if form.is_valid:
            new= form.save(commit=False)
            new.name = request.user
            message =  render_to_string('parent/leave.html', {
                'name': request.user,
                'title':request.POST['title'],
                'subject':request.POST['subject'],
               
            })
            mail_subject = 'Activate your account.'
            to_email = request.POST['recipient_email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            form.save()
    
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request,'parent/leaveform.html',context)

def leaveslist(request,user):
    obj =Leaves.objects.filter(name=user)
    context = {
        'obj': obj,
     
    }
    return render(request,'parent/leaveslist.html',context)





###########################################################################################################
###########################################################################################################
################################# Teachers AND PROGRAM  .#######################################################3

def attendencelistteacher(request):
    cla = Class.objects.get(teacher=request.user)
    obj = attendence.objects.filter(Dropped_or_pickup=True,classname=cla)
    a=[]
    for i in obj:
        contact=profileModel.objects.get(user=i.parent)
        a.append(contact.contactNumber)
    context = {
        'obj': obj,
        'a':a,


     
    }
    return render(request,'teacher/attendence.html',context)

def notificationview(request):
    cla = Class.objects.get(teacher=request.user)
    parent= child.objects.filter(classname=cla)
    emails=[]
    for i in parent:
        user= User.objects.filter(username=i.parent)
        for k in user:
            print(k.email)
            emails.append(k.email)

    form=notificationform()
    if request.method == 'POST':
        form = notificationform(request.POST, request.FILES)
        if form.is_valid:
            new =form.save(commit=False)
            new.classname=cla
    ##############   email   ###############333
          
            message =  render_to_string('teacher/notify.html', {
                'title':request.POST['title'],
                'subject':request.POST['subject'],
               
            })
            mail_subject = 'Activate your account.'
            to_email = emails
            for i in to_email:
                email = EmailMessage(mail_subject, message, to=[i])
                email.send()

    ###########################################
            form.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request,'teacher/notificationform.html',context)


def notifcationlist(request):
    cla=Class.objects.get(teacher=request.user)
    obj = Notifications.objects.filter(classname=cla)
    context = {
        'obj': obj,
     
    }
    return render(request,'teacher/notification1.html',context)

def notificationedit(request, id):
    obj = Notifications.objects.get(id=id)
    cla = Class.objects.get(teacher=request.user)
    parent= child.objects.filter(classname=cla)
    emails=[]
    for i in parent:
        user= User.objects.filter(username=i.parent)
        for k in user:
            emails.append(k.email)

    form1 =notificationform(instance=obj)
    if request.method == 'POST':
        form1 = notificationform(request.POST,request.FILES, instance=obj)
        if form1.is_valid():
        ##############   email   ###############333
          
            message =  render_to_string('teacher/notify.html', {
                'title':request.POST['title'],
                'subject':request.POST['subject'],
               
            })
            mail_subject = 'Activate your account.'
            to_email = emails
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

    ###########################################
            form1.save()
    
            return redirect('home')
    print(form1)    
    context = {
        'form1': form1,
        'obj': obj,
    }
    return render(request,'teacher/notificationedit.html',context)




def childstorylist(request):
    cla = Class.objects.get(teacher=request.user)
    obj = child.objects.filter(classname=cla)
    context = {
        'obj': obj,
    }
    return render(request,'teacher/childstories.html',context)


def child_storiesview(request, id):
    obj = child.objects.get(id=id)
    form =child_storiesform()
    if request.method == 'POST':
        form = child_storiesform(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.name=obj
            new.classname=obj.classname
            form.save()
            return render(request,'teacher/success.html')
     
    context = {
        'form': form,
        'obj': obj,
    }
    return render(request,'teacher/childstoriesadd.html',context)



def childlistprofileteacher(request):
    cla = Class.objects.get(teacher=request.user)
    obj = child.objects.filter(classname=cla)
    context = {
        'obj': obj,
    }
    return render(request,'teacher/childlistprofile.html',context)


def leaveslistteacher(request):
    obj =Leaves.objects.all()
    context = {
        'obj': obj,
     
    }
    return render(request,'teacher/leaveslistteacher.html',context)

def leavesviewedit(request,id):
    obj= Leaves.objects.get(id=id)
    obj1=User.objects.get(username=obj.name)
    
    form=leavesform1(instance=obj)
    if request.method == 'POST':
        form = leavesform1(request.POST,request.FILES,instance=obj)
        if form.is_valid:
            new= form.save(commit=False)
            new.name = obj.name
            new.recipient_email=obj.recipient_email
            new.title = obj.title
            new.subject = obj.subject
            new.files = obj.files

            message =  render_to_string('teacher/leaveteacher.html', {
                'name': new.name,
                'title':new.title,
                'subject':new.subject,
                'approved':request.POST['approved'],
               
            })
            mail_subject = 'Activate your account.'
            to_email = obj1.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            form.save()
    
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request,'parent/leaveform.html',context)


def games(request):
    return render(request,'parent/game.html',{})
def game1(request):
    return render(request,'parent/game1.html',{})
def game2(request):
    return render(request,'parent/game2.html',{}) 


#REST...........................................................................................


class ListprofileView(generics.ListAPIView):
    queryset = profileModel.objects.all()
    serializer_class = profileSerializer

class attendenceView(generics.ListAPIView):
    queryset = attendence.objects.all()
    serializer_class = attendenceSerializer

class NotificationView(generics.ListAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

class child_storiesView(generics.ListAPIView):
    queryset = child_stories.objects.all()
    serializer_class = child_storiesSerializer

class LeavesView(generics.ListAPIView):
    queryset = Leaves.objects.all()
    serializer_class = LeavesSerializer
#################################################### Detail ##########################
class profileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = profileModel.objects.all()
    serializer_class = profileSerializer

class attendenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = attendence.objects.all()
    serializer_class = attendenceSerializer

class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

class child_storiesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = child_stories.objects.all()
    serializer_class = child_storiesSerializer

class LeavesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leaves.objects.all()
    serializer_class = LeavesSerializer
#####################################################Viewsets ##########################
from rest_framework import viewsets
class childViewset(viewsets.ModelViewSet):
    queryset = child.objects.all()
    serializer_class = childSerializer

class profileViewset(viewsets.ModelViewSet):
    queryset = profileModel.objects.all()
    serializer_class = profileSerializer

class attendenceViewset(viewsets.ModelViewSet):
    queryset = attendence.objects.all()
    serializer_class = attendenceSerializer

class NotificationViewset(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

class child_storiesViewset(viewsets.ModelViewSet):
    queryset = child_stories.objects.all()
    serializer_class = child_storiesSerializer

class LeavesViewset(viewsets.ModelViewSet):
    queryset = Leaves.objects.all()
    serializer_class = LeavesSerializer

