from abc import abstractproperty
from random import Random, paretovariate
from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from passlib.hash import pbkdf2_sha256
from django.conf import settings
import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import date,datetime,timedelta
import datetime
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .services import *
from .auth_guard import auth_admin, auth_driver, auth_member, auth_user
from .models import *
from .forms import *
# Create your views here.


def ProjectHome(request):
    return render(request,'pswms/Common/ProjectHome.html')

def ProjectAbout(request):
    return render(request,'pswms/Common/About.html')

def AdminData(request):
    passwd=pbkdf2_sha256.hash("admin",rounds=1000,salt_size=32)
    qry=AdminDetails(login_id="Admin",login_passwd=passwd)
    qry.save()
    return redirect("pswms:common_login")

def CommonLogin(request):   
    form=LoginForm()
    
    if request.method=='POST':
        form=LoginForm(request.POST)
       
        if 'forgotpassword' in request.POST:
            login_id=request.POST['user_name']
            if login_id=="":
                msg="enter username"
                return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
            return redirect("pswms:forgot_password",login_id)
        
        if form.is_valid():
            login_id=form.cleaned_data['user_name']
            login_passwd=form.cleaned_data['passwd']
            
            if login_id.isdigit():
                data_exist=DriverDetails.objects.filter(driver_id=login_id).exists()
                if data_exist:
                    driver_data=DriverDetails.objects.get(driver_id=login_id)
                    check_passwd=driver_data.verifyPasswd(login_passwd)
                    if check_passwd:
                        request.session['driver_id']=driver_data.driver_id
                        
                        return redirect("pswms:driver_home")
                    else:
                        msg="Incorrect Password"
                        return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
                else:
                    msg="UserName or Password Incorrect"
                    return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})

            if '@' in login_id:
                email_exist=UserDetails.objects.filter(user_email=login_id).exists()
                if email_exist:
                    user_data=UserDetails.objects.get(user_email=login_id)
                    check_passwd=user_data.verifyPasswd(login_passwd)
                    if check_passwd:
                
                        if user_data.user_status=="approved":
                            
                            request.session['user_id']=user_data.user_id
                            request.session['pan_id']=user_data.user_pan.pan_id
                            request.session['user_name']=user_data.user_name
                            request.session['ward_id']=user_data.user_ward.ward_id
                            return redirect("pswms:user_home")
                        elif user_data.user_status=='blocked':
                            msg="Your Account has been Blocked by Admin"
                            return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
                        else:
                            msg="Your Account has not been approved by Admin"
                            return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
                    else:
                        msg="Password Incorrect"
                        return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
                else:
                    msg="Incorrect user name or password"
                    return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
            elif login_id=="Admin":
                do_exist=AdminDetails.objects.filter(login_id=login_id).exists()
                if do_exist:
                    admin_data=AdminDetails.objects.get(login_id=login_id)
                    check_passwd=admin_data.verifyPasswd(login_passwd)
                    if check_passwd:
                        request.session['admin_id']=admin_data.login_id
                        return redirect("pswms:super_home")
                    else:
                        msg="Password Incorrect"
                        return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
                else:
                    msg="Incorrect User Name or Pssword"
                    return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
            elif re.match(r'[a-z A-Z]',login_id):
                do_exist=PanchayathMemberDetails.objects.filter(p_user_name=login_id).exists()
                if do_exist:
                    member_data=PanchayathMemberDetails.objects.get(p_user_name=login_id)
                    if member_data.p_status=="Tenure Completed":
                        msg="Your Account Has Expired"
                        return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
                    else:

                        check_passwd=member_data.verifyPasswd(login_passwd)
                        if check_passwd:
                            request.session['id']=member_data.pid
                            ward_data=WardDetails.objects.get(ward_member=request.session['id'])
                            
                            request.session['ward_id']=ward_data.ward_id
                        
                            request.session['user_type']="member" 
                            return redirect("pswms:member_home")
                        else:
                            msg="Password Incorrect"
                            return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
                else:
                    msg="Incorrect User Name or Pssword"
                    return render(request,'pswms/Common/CommonLogin.html',{'msg':msg,'form':form})
            else:
                print(form.errors)
        
    return render(request,'pswms/Common/CommonLogin.html',{'form':form})






@auth_admin
def AddPanchayath(request):
  
    form=PanchayathForm()
    panchayath_list=PanchayathDetails.objects.all()
    current_page=request.GET.get('page')
    panchayath_list=get_pagination(3,current_page,panchayath_list)
   
    
    if request.method=='POST':
        
        form=PanchayathForm(request.POST)
        if form.is_valid():
            panchayath_name=form.cleaned_data['pan_name']
            do_exist=PanchayathDetails.objects.filter(pan_name=panchayath_name.lower()).exists()
            if do_exist:
                error_msg="Panchayath Already Added"
                return render(request,'pswms/SuperAdmin/AddPanchayath.html',{'form':form,'error_msg':error_msg,'panchayath_list':panchayath_list})
                
            else:
                qry=PanchayathDetails(pan_name=panchayath_name.lower())
                qry.save()
                success_msg="Panchayath Added Succesfully"
                error_msg=""    
                updated_list=PanchayathDetails.objects.all()
                current_page=request.GET.get('page')
                updated_list=get_pagination(3,current_page,updated_list)
                for i in updated_list:
                    print(i.pan_name)
                return render(request,'pswms/SuperAdmin/AddPanchayath.html',{'form':form,'success_msg':success_msg,'panchayath_list':updated_list})
        else:
            print(form.errors)
    return render(request,'pswms/SuperAdmin/AddPanchayath.html',{'form':form,'panchayath_list':panchayath_list})

def DeletePanchayath(request,p_id):
    ward=PanchayathDetails.objects.get(pan_id=p_id)
    ward.delete()
    return redirect("pswms:add_panchayath")


@auth_user
def UserHome(request):
    user_data=UserDetails.objects.get(user_id=request.session['user_id'])
   
   
    return render(request,'pswms/Users/UserHome.html',{'data':user_data})    

@auth_admin
def SuperHome(request):
    user_data=AdminDetails.objects.get(login_id=request.session['admin_id'])
    return render(request,'pswms/SuperAdmin/Chart.html',{'data':user_data})
    


@auth_member
def MemberHome(request):
    panchayath=WardDetails.objects.get(ward_id=request.session['ward_id'])
    member_panchayath=panchayath.pan_id.pan_name
    users_count=UserDetails.objects.filter(user_ward=request.session['ward_id'],user_status='approved').count()
    member_name=PanchayathMemberDetails.objects.get(pid=request.session['id'])
    name=member_name.p_name
    request.session['m_name']=name
    request.session['usr_count']=users_count
    request.session['p_nme']=member_panchayath
    # member_data=PanchayathMemberDetails.objects.get(pid=request.session['id'])
    return render(request,'pswms/Member/chart.html',{'p':member_panchayath,'c':users_count,'m':name})


@auth_driver
def DriverHome(request):
    driver_data=DriverDetails.objects.get(driver_id=request.session['driver_id'])
    return render(request,'pswms/Driver/DriverHome.html',{'data':driver_data})
   


def AddBin(request):
    form=BinForm()
    panchayath_list=PanchayathDetails.objects.all()
    
    primary_data=PanchayathDetails.objects.filter()[:1].get()
    pan_name=primary_data.pan_name
    bin_list=BinDetails.objects.select_related('pan_id').filter(pan_id=primary_data.pan_id)    
    current_page=request.GET.get('page')
    bin_list=get_pagination(4,current_page,bin_list)
    if request.method=='GET' and 'panid' in request.session:
        bin_list=BinDetails.objects.select_related('pan_id').filter(pan_id=request.session['panid'])    
        current_page=request.GET.get('page')
        bin_list=get_pagination(4,current_page,bin_list)
        pan_name=request.session['pan_name']
    if request.method=='POST':
        form=BinForm(request.POST)
        if form.is_valid():
            try:
                
                bin_name=form.cleaned_data['bin_name'].lower()
                pan_id=PanchayathDetails.objects.get(pan_id=request.POST['panchayath'])
                # current_page=request.GET.get('page')
                # bin_details=BinDetails.objects.filter(pan_id=pan_id)
                # bin_details=get_pagination(4,current_page,bin_details)
            
                do_exist=BinDetails.objects.filter(pan_id=pan_id,bin_name=bin_name).exists()
                
                if do_exist:
                    current_page=request.GET.get('page')
                    bin_details=BinDetails.objects.filter(pan_id=pan_id)
                    bin_details=get_pagination(4,current_page,bin_details)
                    error_msg="Bin Already Added For The Panchayath"
                    form=BinForm()
                    return render(request,'pswms/SuperAdmin/AddBin.html',{'form':form,'panchayath_list':panchayath_list,'error_msg':error_msg,'bin_list':bin_list,'pan_name':request.session['pan_name']})
                else:
                    qry=BinDetails(pan_id=pan_id,bin_name=bin_name)
                    
                    qry.save()
                    
                    current_page=request.GET.get('page')
                    
                    updated_list=BinDetails.objects.filter(pan_id=pan_id)
                    
                    request.session['panid']=updated_list[0].pan_id.pan_id
                    request.session['pan_name']=updated_list[0].pan_id.pan_name
                    
                    updated_list=get_pagination(4,current_page,updated_list)
                    
                    form=BinForm()
                    
                    success_msg="Bin Added Succesfully"
                    
                    return render(request,'pswms/SuperAdmin/AddBin.html',{'form':form,'panchayath_list':panchayath_list,'success_msg':success_msg,'bin_list':updated_list,'pan_name':request.session['pan_name']})
            except Exception as e:
                pass
        
    
    return render(request,'pswms/SuperAdmin/AddBin.html',{'form':form,'panchayath_list':panchayath_list,'bin_list':bin_list,'pan_name':pan_name})




@auth_admin
def AddWard(request):
    form=WardForm()
    updated_pan=""
    ward_list=WardDetails.objects.all()
    primary_data=PanchayathDetails.objects.filter()[:1].get()
    ward_display=WardDetails.objects.select_related('pan_id').filter(pan_id=primary_data.pan_id).order_by('ward_no')
    pan_name=primary_data.pan_name
    current_page=request.GET.get('page')
    panchayath=PanchayathDetails.objects.all()
    ward_display=get_pagination(4,current_page,ward_display)
    if request.method=='GET' and 'sel_pan' in request.session:

     
        current_page=request.GET.get('page')
        ward_display=WardDetails.objects.select_related('pan_id').filter(pan_id=request.session['sel_pan']).order_by('ward_no')
        ward_display=get_pagination(4,current_page,ward_display)
        pan_name=request.session['updated_pan']
    
    if request.method=='POST':
        form=WardForm(request.POST)
        if form.is_valid():
            current_page=request.GET.get('page')
            pan_id=request.POST['panchayath']
            
            ward_no=form.cleaned_data['ward_no']
            updated_display=WardDetails.objects.select_related('pan_id').filter(pan_id=pan_id).order_by('ward_no')
            updated_display=get_pagination(4,current_page,updated_display)
            if updated_display:
                request.session['updated_pan']=updated_display[0].pan_id.pan_name           
            do_exist=WardDetails.objects.filter(pan_id=pan_id,ward_no=ward_no).exists()
            
            
            if do_exist:
                error_msg="Data Already Added"
                current_page=request.GET.get('page')
                updated_display=WardDetails.objects.select_related('pan_id').filter(pan_id=pan_id).order_by('ward_no')
                request.session['sel_pan']=updated_display[0].pan_id.pan_id
                updated_display=get_pagination(4,current_page,updated_display)
                
                return render(request,'pswms/SuperAdmin/AddWard.html',{'panchayath':panchayath,'error_msg':error_msg,'form':form,'ward_display':updated_display,'pan_name':request.session['updated_pan'],}) 
            else:
                
                pan_data=PanchayathDetails.objects.get(pan_id=pan_id)
                request.session['updated_pan']=pan_data.pan_name
                qry=WardDetails(pan_id=pan_data,ward_no=ward_no)
                qry.save()
                request.session['sel_pan']=pan_data.pan_id
                current_page=request.GET.get('page')
                updated_display=WardDetails.objects.select_related('pan_id').filter(pan_id=request.session['sel_pan']).order_by('ward_no')
                updated_display=get_pagination(4,current_page,updated_display)
                success_msg="Data Saved Succesfully"
                return render(request,'pswms/SuperAdmin/AddWard.html',{'panchayath':panchayath,'success_msg':success_msg,'form':form,'ward_display':updated_display,'pan_name':request.session['updated_pan'],})
        else:
            print(form.errors)
   
    return render(request,'pswms/SuperAdmin/AddWard.html',{'panchayath':panchayath,'form':form,'ward_list':ward_list,'ward_display':ward_display,'pan_name':pan_name})












@auth_admin
def AddNotification(request):
    form=NotificationForm()
    
    notification_list=NotificationDetails.objects.all()
    current_page=request.GET.get('page')
    notification_list=get_pagination(5,current_page,notification_list)




    if request.method=='POST':




        form=NotificationForm(request.POST)
        if form.is_valid():
             notification_title=form.cleaned_data['notification_title']
             notification=form.cleaned_data['notification']
             notification_date=date.today()
             print(notification_date)
             do_exist=NotificationDetails.objects.filter(notification=notification,date=notification_date).exists()

             if do_exist:
                form=NotificationForm()
                error_msg="Notification Already Added"
                return render(request,'pswms/SuperAdmin/AddNotification.html',{'form':form,'error_msg':error_msg,'notification_list':notification_list})


             else:
                qry=NotificationDetails(notification_title=notification_title, notification=notification.lower(),date=notification_date)
                qry.save()
                success_msg="Notification Added Succesfully"
                error_msg="" 
                updated_list=NotificationDetails.objects.all()
                current_page=request.GET.get('page')
                updated_list=get_pagination(5,current_page,updated_list)
                for i in updated_list:
                    print(i.notification)   
                form=NotificationForm()
                return render(request,'pswms/SuperAdmin/AddNotification.html',{'form':form,'success_msg':success_msg,'notification_list':updated_list})
       
    return render(request,'pswms/SuperAdmin/AddNotification.html',{'form':form,'notification_list':notification_list})

def DeleteBin(request,bin_id):
    bin_data=BinDetails.objects.get(bin_id=bin_id)
    bin_data.delete()
    return redirect("pswms:add_bin")

@auth_admin
def DeleteWard(request,ward_id):
    wrd_data=WardDetails.objects.get(ward_id=ward_id)
    wrd_data.delete()
    return redirect("pswms:add_ward")

def DeleteNotification(request,n_id):
    notfn_data=NotificationDetails.objects.get(n_id=n_id)
    notfn_data.delete()
    return redirect("pswms:add_notification")

@auth_member
def ViewNotifications(request):
    
    notification_list=NotificationDetails.objects.filter().order_by('n_id')[:5]
    current_page=request.GET.get('page')
    notification_list=get_pagination(1,current_page,notification_list)
    context={
        'notification_list':notification_list,
        'm':request.session['m_name'],
        'p':request.session['p_nme'],
        'c':request.session['usr_count']
        }

    return render(request,'pswms/Member/ViewNotifications.html',context)
    
@auth_admin
def AddPanchayathMember(request):
    form=PanchayathMemberForm()
  
    
    panchayath_list=PanchayathDetails.objects.all()
    ward_list=WardDetails.objects.all().order_by('ward_no')
    if request.method=='POST':
        form=PanchayathMemberForm(request.POST,request.FILES)
        if form.is_valid():
            p_name=form.cleaned_data['p_name']
            p_address=form.cleaned_data['p_address']
            p_dob=form.cleaned_data['p_dob']
            p_gender=form.cleaned_data['p_gender']
            p_email=form.cleaned_data['p_email']
            p_phno=form.cleaned_data['p_phno']
            p_img=form.cleaned_data['p_img']
            passwd=get_random_string(length=8)
            p_year=request.POST['yr_frm']+" To " +request.POST['yr_to']
            
            user_name=p_name.lower()
            p_passwd=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
            do_exist=PanchayathMemberDetails.objects.filter(p_email=p_email).exists()
            
            if do_exist:
                error_msg="Panchyath Member Already Added"
                form=PanchayathMemberForm()
                return render(request,'pswms/SuperAdmin/AddPanchayathMember.html',{'form':form,'error_msg':error_msg,'yr_frm':range(2000,2031),'yr_to':range(2000,2031)})
            else:
                pid=request.POST['panchayath']
                ward=request.POST['ward']
                qry=PanchayathMemberDetails(p_name=p_name,p_gender=p_gender,p_dob=p_dob,p_address=p_address,p_email=p_email,p_phno=p_phno,p_img=p_img,p_user_name=user_name, p_passwd=p_passwd,p_status="Active",p_year=p_year,ward_id=ward)
                
                try:
                    ward_data=WardDetails.objects.get(pan_id=pid,ward_id=ward)
                    if ward_data.ward_member==None:

                        qry.save()
                        latest_entry=PanchayathMemberDetails.objects.latest('pid')
                        ward_data.ward_member=latest_entry
                        email_admin(ward_data.ward_member.p_email,user_name,passwd)
                        latest_entry.ward_id=ward
                        latest_entry.save()
                        ward_data.save()
                        form=PanchayathMemberForm()
                        
                        success_msg="Member Added Succesfully"
                        return render(request,'pswms/SuperAdmin/AddPanchayathMember.html',{'form':form,'success_msg':success_msg,'panchayath_list':panchayath_list,'yr_frm':range(2000,2031),'yr_to':range(2000,2031)})
                    else:
                       
                        try:
                            ex_member=WardDetails.objects.select_related('ward_member').get(ward_id=ward)
                            
                            ex_member.ward_member.p_status="Tenure Completed"
                            ex_member.ward_member.save()
                            
                            qry.save()
                            current_member_id=PanchayathMemberDetails.objects.latest('pid')
                            ward_data.ward_member=current_member_id
                            current_member_id.ward_id=ward
                            current_member_id.save()
                            ward_data.save()
                            email_admin(ward_data.ward_member.p_email,user_name,passwd)
                            success_msg="Member Changed Succesfully"
                            form=PanchayathMemberForm()
                        except Exception as e:
                            pass
                        return render(request,'pswms/SuperAdmin/AddPanchayathMember.html',{'form':form,'success_msg':success_msg,'panchayath_list':panchayath_list,'yr_frm':range(2000,2031),'yr_to':range(2000,2031)})
                except Exception as e:
                    pass
        
    
    return render(request,'pswms/SuperAdmin/AddPanchayathMember.html',{'form':form,'panchayath_list':panchayath_list,'ward_list':ward_list,'yr_frm':range(2000,2031),'yr_to':range(2000,2031)})\

@auth_member
def MemberUpdateProfile(request):
    member_data=PanchayathMemberDetails.objects.get(pid=request.session['id'])
    form=MemberUpdateForm(instance=member_data)
    if request.method=='POST':
        form=MemberUpdateForm(request.POST)
        
        
        if form.is_valid():
            address=form.cleaned_data['p_address']
            phno=form.cleaned_data['p_phno']
            email=form.cleaned_data['p_email']
            member_data.p_address=address
            member_data.p_email=email
            member_data.p_phno=phno
            member_data.save()
            context={
                'form':form,
                'm':request.session['m_name'],
                'p':request.session['p_nme'],
                'c':request.session['usr_count']
            }
            return render(request,'pswms/Member/UpdateProfile.html',context)
        else:
            print(form.errors)
       
    return render(request,'pswms/Member/UpdateProfile.html',{'form':form,'m':request.session['m_name'],'p':request.session['p_nme'],'c':request.session['usr_count']})



def UserRegistration(request):
    form=UserRegForm()
    panchayath_list=PanchayathDetails.objects.all()
    if request.method=='POST':
        form=UserRegForm(request.POST,request.FILES)
        if form.is_valid():
           if form.is_valid():    
            first_name=form.cleaned_data['first_name'].title()
            last_name=form.cleaned_data['last_name'].title()
            user_name=first_name+ " "+last_name
            user_dob=form.cleaned_data['user_dob']
            user_address=form.cleaned_data['user_address']
            user_gender=form.cleaned_data['user_gender']
            user_email=form.cleaned_data['user_email'] 
            user_phno=form.cleaned_data['user_phno']
            user_house_no=form.cleaned_data['user_house_no']
            user_passwd=form.cleaned_data['user_passwd']
            passwd_again=form.cleaned_data['confirm_passwd']
            user_img=form.cleaned_data['user_img']
            pan_id=PanchayathDetails.objects.get(pan_id= request.POST['pan'])
            ward_id=WardDetails.objects.get(ward_id=request.POST['ward'])
            status="not approved"
            enc_passwd=pbkdf2_sha256.hash(user_passwd,rounds=1000,salt_size=32)
            do_exist=UserDetails.objects.filter(user_email=user_email).exists()
            if user_passwd!=passwd_again:
                password_error="Password Mismatch"
                return render(request,'pswms/Common/UserRegistration.html',{'panchayath_list':panchayath_list,'password_error':password_error,'form':form})
            elif len(user_passwd)<8:
                password_error="Password should be atleat 8 characters"
                return render(request,'pswms/Common/UserRegistration.html',{'panchayath_list':panchayath_list,'password_error':password_error,'form':form})
            if do_exist:
                msg="User Already Added"
                return render(request,'pswms/Common/UserRegistration.html',{'panchayath_list':panchayath_list,'error_msg':msg,'form':form})
            
            
            else:
                qry=UserDetails(user_name=user_name,user_pan=pan_id, user_ward=ward_id, user_gender=user_gender,user_dob=user_dob,user_house_no=user_house_no, user_address=user_address,user_email=user_email,user_phno=user_phno,user_img=user_img,user_passwd=enc_passwd,user_status=status)
                qry.save()
                msg="Registration Succesful"
                return render(request,'pswms/Common/UserRegistration.html',{'panchayath_list':panchayath_list,'success_msg':msg,'form':form})
            
    
    return render(request,'pswms/Common/UserRegistration.html',{'panchayath_list':panchayath_list,'form':form})

@auth_member
def PendingUsers(request):
    users_list=UserDetails.objects.select_related('user_pan').select_related('user_ward').filter(user_status="not approved",user_ward=request.session['ward_id'])    
    print(users_list)
    context={
                'users':users_list,
                'm':request.session['m_name'],
                'p':request.session['p_nme'],
                'c':request.session['usr_count']
            }
    return render(request,'pswms/Member/ApproveUsers.html',context)

@auth_driver
def PendingWorks(request):
    pending_request=TempryRequest.objects.filter( (Q(status='driver_assigned')|Q(status='delayed')),driver_id=request.session['driver_id'],) .order_by('date')
    
    return render(request,'pswms/Driver/PendingRequest.html',{'pending_request':pending_request})

@auth_member
def ApproveUser(request,user_id):
    user_data=UserDetails.objects.get(user_id=user_id)
    user_data.user_status="approved"
    user_data.save()
    email_user(user_data.user_email,'Approved')
    return redirect("pswms:pending_users")

@auth_member
def RejectUser(request,user_id):
    user_data=UserDetails.objects.get(user_id=user_id)
    user_data.user_status="rejected"
    email_user(user_data.user_email,'Rejected')
    user_data.save()
    return redirect("pswms:pending_users")

@auth_member
def DeleteUsers(request,user_id):
    user_data=UserDetails.objects.get(user_id=user_id)
    user_data.user_status="deleted"
    email_user(user_data.user_email,'deleted')
    user_data.save()
    return redirect("pswms:pending_users")

def Logout(request):
    if 'admin_id' in request.session:
        del request.session['admin_id']
    if 'id' in request.session:
        del request.session['id']
    if 'ward_id' in request.session:
        del request.session['ward_id']
    request.session.flush()
    return redirect("pswms:common_login")

def getWard(request):#AJAX call 
    pan_id=request.GET.get('pan_id')
    ward_list=WardDetails.objects.filter(pan_id=pan_id)
    return render(request, 'pswms/Common/ward_dropdown_list_options.html', {'wards': ward_list})


# @auth_admin
# def ViewMembers(request):
#     members_list=WardDetails.objects.select_related('ward_member').exclude(ward_member=None).select_related('pan_id')
#     return render(request,'pswms/SuperAdmin/ViewMembers.html',{'members_list':members_list})

@auth_admin
def DeleteMember(request,member_id):
    member_data=PanchayathMemberDetails.objects.get(pid=member_id)
    member_data.delete()
    return redirect('pswms:view_all_members')

@auth_member
def DeleteDriver(request,driver_id):
    driver_data=DriverDetails.objects.get(driver_id=driver_id)
    driver_data.delete()
    return redirect('pswms:view_driver')


@auth_admin
def AddWaste(request):
    form=WasteForm()
    waste_list=WasteDetails.objects.all()
    current_page=request.GET.get('page')
    waste_list=get_pagination(3,current_page,waste_list)
    if request.method=='POST':
        form=WasteForm(request.POST)
        if form.is_valid():
            p=Paginator(waste_list,4)
            current_page=request.GET.get('page')
            waste_list=p.get_page(current_page)
            waste_type=form.cleaned_data['waste_type']
            waste_price=form.cleaned_data['waste_price']
            data_exist=WasteDetails.objects.filter(waste_type=waste_type.lower()).exists()
            if data_exist:
                error_msg="Waste Type Already Added"
                return render(request,'pswms/SuperAdmin/AddWaste.html',{'form':form,'error_msg':error_msg,'waste_list':waste_list})
        
            else:
                qry=WasteDetails(waste_type=waste_type.lower(),waste_price=waste_price)
                qry.save()
                success_msg="Waste Type Added Succesfully"
                updated_list=WasteDetails.objects.all()
                current_page=request.GET.get('page')
                updated_list=get_pagination(3,current_page,updated_list)
                form=WasteForm()
                return render(request,'pswms/SuperAdmin/AddWaste.html',{'form':form,'success_msg':success_msg,'waste_list':updated_list})
        else:
            print(form.errors)
    return render(request,'pswms/SuperAdmin/AddWaste.html',{'form':form,'waste_list':waste_list})



def WasteDelete(request,w_id):
    waste=WasteDetails.objects.get(waste_id=w_id)
    waste.delete()
    return redirect("pswms:add_waste")


@auth_admin
def AdminViewUsers(request):
    panchayath_list=PanchayathDetails.objects.all()
    msg=""
    if request.method=='POST':
        userward=request.POST['ward']
        users=UserDetails.objects.filter(user_ward=userward)
        if not users:
            msg="No data"
        return render(request,'pswms/SuperAdmin/ViewUsers.html',{'panchayath_list':panchayath_list,'users':users,'msg':msg})
    return render(request,'pswms/SuperAdmin/ViewUsers.html',{'panchayath_list':panchayath_list})



@auth_admin
def ViewAllMembers(request):
    err_display=False;
    panchayath_list=PanchayathDetails.objects.all()
    if request.method=='POST':
        # ward_id=request.POST['ward']
        current_page=request.GET.get('page')
        member_list=PanchayathMemberDetails.objects.filter(ward_id=request.POST['ward']).order_by('pid')
    
        member_list=get_pagination(3,current_page,member_list)
        if not member_list:
           
            err_display=True
       
        return render(request,'pswms/SuperAdmin/ViewAllMembers.html',{'panchayath_list':panchayath_list,'member_list':member_list,'err_display':err_display})
    return render(request,'pswms/SuperAdmin/ViewAllMembers.html',{'panchayath_list':panchayath_list,'err_display':err_display})

def BlockUser(request,user_id):
       
    user_data=UserDetails.objects.get(user_id=user_id)   
    user_data.user_status="blocked"
    user_data.save()
    return redirect('pswms:view_users')


@auth_member
def MemberChangePasswd(request):
    form=ChangePasswordForm()
    member_data=PanchayathMemberDetails.objects.get(pid=request.session['id'])
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
           
            old_passwd=form.cleaned_data['old_passwd']
            new_passwd=form.cleaned_data['new_passwd']
            confirm_passwd=form.cleaned_data['confirm_passwd']
            is_true=pbkdf2_sha256.verify(old_passwd,member_data.p_passwd)
            if is_true:
                if len(new_passwd)>8:
                    if new_passwd==confirm_passwd:
                        new_encrypted_passwd=pbkdf2_sha256.hash(new_passwd,rounds=1000,salt_size=32)
                        member_data.p_passwd=new_encrypted_passwd
                        member_data.save()
                        success_msg="Password Changed Succesfully"
                        return render(request,'pswms/Member/ChangePassword.html',{'form':form,'success_msg':success_msg})
                    else:
                        error_msg="Password Mismatch"
                        return render(request,'pswms/Member/ChangePassword.html',{'form':form,'error_msg':error_msg})
                else:
                    error_msg="Password Should be atleast 8 characters"
                    return render(request,'pswms/Member/ChangePassword.html',{'form':form,'error_msg':error_msg})
            else:
                error_msg="Invalid Password! enter Your correct password"
                return render(request,'pswms/Member/ChangePassword.html',{'form':form,'error_msg':error_msg})
                
    return render(request,'pswms/Member/ChangePassword.html',{'form':form,})
   
@auth_member
def ViewAllUsers(request):
    form=SearchForm()
    users_list=UserDetails.objects.select_related('user_pan').select_related('user_ward').filter(Q(user_status="approved")|Q(user_status="rejected")|Q(user_status="blocked"),user_ward=request.session['ward_id'])  
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            search_text=form.cleaned_data['user_name']
            search_result=UserDetails.objects.select_related('user_pan').select_related('user_ward').filter(Q(user_status="approved")|Q(user_status="rejected"),user_name__startswith=search_text,user_ward=request.session['ward_id'])
            return render(request,'pswms/Member/ViewAllUsers.html',{'users':search_result,'form':form})
    return render(request,'pswms/Member/ViewAllUsers.html',{'users':users_list,'form':form})



  
def DriverRegistration(request):
    form=DriverRegForm()
    lan=""
    if request.method=='POST':
        form=DriverRegForm(request.POST,request.FILES)
        if form.is_valid():
            print('valid')
            driver_id=unique_id()
            driver_name=form.cleaned_data['driver_name'].title()
            driver_address=form.cleaned_data['driver_address']
            driver_dob=form.cleaned_data['driver_dob']
            driver_gender=form.cleaned_data['driver_gender']
            driver_email=form.cleaned_data['driver_email']
            driver_phno=form.cleaned_data['driver_phno']
            driver_img=form.cleaned_data['driver_img']
            driver_vehicle=form.cleaned_data['driver_vehicle']
            driver_qualification=form.cleaned_data['driver_qualification']
            driver_language=form.cleaned_data['driver_language']
            
            driver_status="Active"
            driver_ward=WardDetails.objects.get(ward_id=request.session['ward_id'])
            passwd=get_random_string(length=8)
            driver_passwd=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
            do_exist=DriverDetails.objects.filter(driver_email=driver_email).exists()
            if do_exist:
                error_msg="Driver Already Added"
                return render(request,'pswms/Member/DriverRegistration.html',{'form':form,'error_msg':error_msg})
            else:
                print(driver_language)
                lan=driver_language.lstrip("[")
                lan=lan.rstrip("]")
                print(lan)
                # lan=lan.strip(",")
                qry=DriverDetails(driver_id=driver_id,driver_name=driver_name,driver_img=driver_img,driver_gender=driver_gender,driver_dob=driver_dob,driver_address=driver_address,driver_email=driver_email,driver_phno=driver_phno,driver_passwd=driver_passwd,driver_status=driver_status,driver_ward=driver_ward,driver_qualification=driver_qualification,driver_language=lan,driver_vehicle=driver_vehicle)
                qry.save()
                email_driver(driver_email,driver_id,passwd)
                success_msg="Driver Added Succesfully"
                return render(request,'pswms/Member/DriverRegistration.html',{'form':form,'success_msg':success_msg,})
    return render(request,'pswms/Member/DriverRegistration.html',{'form':form,})
    




def DownloadUserData(request,u_id):
    user_data=UserDetails.objects.get(user_id=u_id)
    member_sign=MemberSignature.objects.get(member_id=request.session['id'])
    if user_data.user_status=='rejected' or user_data.user_status=='blocked':
        st="red"
    else:
        st="green"
    
    return Create_pdf('pswms/Member/UserDataPdf.html',{'user':user_data,'st':st,'sign':member_sign})


def MemberSign(request):

    if request.method=='POST':
        member=PanchayathMemberDetails.objects.get(pid=request.session['id'])
        alreadyExist=MemberSignature.objects.filter(member_id=request.session['id']).exists()
        
        
        if alreadyExist:
            error_msg="Already Added"
            return render(request,'pswms/Member/AddSignature.html',{'error_msg':error_msg})
        else:
            qry=MemberSignature(member_id=member,member_sign=request.FILES['sign'])
            qry.save()
            success_msg="Signature Added Succesfully"
            return render(request,'pswms/Member/AddSignature.html',{'success_msg':success_msg})
    return render(request,'pswms/Member/AddSignature.html')




@auth_user
def UpdateUserProfile(request):
    user_data=UserDetails.objects.get(user_id=request.session['user_id'])
    form=UpdateUserProfileForm(instance=user_data)
    if request.method=='POST':
        form=UpdateUserProfileForm(request.POST)
        
        
        if form.is_valid():
            try:
                address=form.cleaned_data['user_address']
                phno=form.cleaned_data['user_phno']
                email=form.cleaned_data['user_email']
                user_data.user_address=address
                user_data.user_email=email
                user_data.user_phno=phno
                user_data.save()
            # success_msg="updated Successfully"
            except Exception as e:
                print(e)
                return render(request,'pswms/Users/UpdateUserProfile.html',{'form':form})
        else:
            print(form.errors)
       
    return render(request,'pswms/Users/UpdateUserProfile.html',{'form':form})

@auth_user
def ChangeUserPasswd(request):
    form=ChangePasswordForm()
    user_data=UserDetails.objects.get(user_id=request.session['user_id'])
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            print('form is valid')
            user_old_passwd=form.cleaned_data['old_passwd']
            user_new_passwd=form.cleaned_data['new_passwd']
            user_confirm_passwd=form.cleaned_data['confirm_passwd']
            is_true=pbkdf2_sha256.verify(user_old_passwd,user_data.user_passwd)
            if is_true:
                if len(user_new_passwd)>8:
                    if user_new_passwd==user_confirm_passwd:
                        new_encrypted_passwd=pbkdf2_sha256.hash(user_new_passwd,rounds=1000,salt_size=32)
                        user_data.user_passwd=new_encrypted_passwd
                        user_data.save()
                        success_msg="Password Changed Succesfully"
                        return render(request,'pswms/Users/ChangeUserPassword.html',{'form':form,'success_msg':success_msg})
                    else:
                        error_msg="Password Mismatch"
                        return render(request,'pswms/Users/ChangeUserPassword.html',{'form':form,'error_msg':error_msg})
                else:
                    error_msg="Password Should be atleast 8 characters"
                    return render(request,'pswms/Users/ChangeUserPassword.html',{'form':form,'error_msg':error_msg})
            else:
                error_msg="Invalid Password! enter Your correct password"
                return render(request,'pswms/Users/ChangeUserPassword.html',{'form':form,'error_msg':error_msg})
    return render(request,'pswms/Users/ChangeUserPassword.html',{'form':form,})

@auth_driver
def ChangeDriverPasswd(request):
    form=ChangePasswordForm()
    driver_data=DriverDetails.objects.get(driver_id=request.session['driver_id'])
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            print('form is valid')
            driver_old_passwd=form.cleaned_data['old_passwd']
            driver_new_passwd=form.cleaned_data['new_passwd']
            driver_confirm_passwd=form.cleaned_data['confirm_passwd']
            is_true=pbkdf2_sha256.verify(driver_old_passwd,driver_data.driver_passwd)
            if is_true:
                if len(driver_new_passwd)>8:
                    if driver_new_passwd==driver_confirm_passwd:
                        new_encrypted_passwd=pbkdf2_sha256.hash(driver_new_passwd,rounds=1000,salt_size=32)
                        driver_data.driver_passwd=new_encrypted_passwd
                        driver_data.save()
                        success_msg="Password Changed Succesfully"
                        return render(request,'pswms/Driver/ChangeDriverPassword.html',{'form':form,'success_msg':success_msg})
                    else:
                        error_msg="Password Mismatch"
                        return render(request,'pswms/Driver/ChangeDriverPassword.html',{'form':form,'error_msg':error_msg})
                else:
                    error_msg="Password Should be atleast 8 characters"
                    return render(request,'pswms/Driver/ChangeDriverPassword.html',{'form':form,'error_msg':error_msg})
            else:
                error_msg="Invalid Password! enter Your correct password"
                return render(request,'pswms/Users/ChangeUserPassword.html',{'form':form,'error_msg':error_msg})
    return render(request,'pswms/Driver/ChangeDriverPassword.html',{'form':form,})



@auth_member
def ViewDriver(request):
    driver_list=DriverDetails.objects.all()
    context={
                'driver_list':driver_list,
                'm':request.session['m_name'],
                'p':request.session['p_nme'],
                'c':request.session['usr_count']
            }
    return render(request,'pswms/Member/ViewDriver.html',context)


@auth_user
def AddComplaint(request):
    form=ComplaintForm()
    user_id=UserDetails.objects.get(user_id=request.session['user_id'])
    if request.method=='POST':
        form=ComplaintForm(request.POST)
        if form.is_valid():
            ward_id=WardDetails.objects.get(ward_id=request.session['ward_id'])
            user_id=request.session['user_id']
            user_complaint=form.cleaned_data['complaint']
            complaint_date=date.today()
            recipient_type=request.POST['recipient']
            do_exist=ComplaintDetails.objects.filter(user_complaint=user_complaint,complaint_date=complaint_date,recipient_type=recipient_type).exists()

            if do_exist:
                error_msg="Action not submited"
                return render(request,'pswms/Users/ComplaintReg.html',{'form':form,'error_msg':error_msg})

            else:
                qry=ComplaintDetails(user_complaint=user_complaint.lower(),ward_id=ward_id,complaint_date=complaint_date,user_id=UserDetails.objects.get(user_id=request.session['user_id']),recipient_type=recipient_type)
                qry.save()
                success_msg="complaint registered"
                return render(request,'pswms/Users/ComplaintReg.html',{'form':form,'success_msg':success_msg,})

    return render(request,'pswms/Users/ComplaintReg.html',{'form':form,})

@auth_member
def PendingPickUpRequest(request):           
    pending_request=TempryRequest.objects.filter(ward_id=request.session['ward_id'],driver_id=None).order_by('date')
    context={
        'pending_request':pending_request,
        'm':request.session['m_name'],
        'p':request.session['p_nme'],
        'c':request.session['usr_count']
        }
    return render(request,'pswms/Member/PendingRequest.html',context)


@auth_driver
def ViewWorkDetails(request):

    if request.method=='POST':
        requested_data=WasteRequestDetails.objects.filter(user_id=request.session['usr'],date=request.session['dt'])
        
        temp_data=TempryRequest.objects.get(user_id=request.session['usr'],date=request.session['dt'])
        user_email=temp_data.user_id.user_email
        
        del_date=datetime.datetime.strptime(request.session['dt'],'%Y-%m-%d').date()
        new_date=del_date+timedelta(days=2)
        work_status=request.POST['status']
        if work_status=='completed':
            for data in requested_data:
                data.payment_status=data.status='completed'
                data.save()
            
                temp_data.status='completed'
                temp_data.save()
            return redirect("pswms:driver_home")
            
        else:
            for data in requested_data:
                data.status="delayed"
                data.delay_date=new_date
                data.delay_status=request.POST['reason']
                data.save()
            
            temp_data.delay_status=request.POST['reason']
            temp_data.delay_date=new_date
            temp_data.status='delayed'
            temp_data.save()
            delay_user(user_email,request.session['dt'],new_date)
            return redirect("pswms:driver_home")


                  
    user= request.GET.get('user')
    date= request.GET.get('date')
    requested_data=WasteRequestDetails.objects.filter(user_id=user,date=date)
    user_name=requested_data[0].user_id.user_name
    phone_no=requested_data[0].user_id.user_phno
    address=requested_data[0].user_id.user_address
    request.session['dt']=date
    request.session['usr']=int(user)

    return render(request,'pswms/Driver/WorkDetails.html',{'requested_data':requested_data,'user_name':user_name,'phno':phone_no,'address':address})



def getPrice(request):# user-ajax call
    waste_id=request.GET.get('waste_id')
    waste_detail=WasteDetails.objects.get(waste_id=waste_id)
    qty=request.GET.get('qty')
    price=waste_detail.waste_price
    total=int(qty)*int(price)
    print("qty is",qty,"and total is",total)
    return HttpResponse(total)

@auth_member
def RequestDetails(request):
    
    if request.method=='POST':
        # driver=DriverDetails.objects.get(driver_id=request.POST['driver'])
        
        # driver=request.POST['driver']
        dr_id=DriverDetails.objects.get(driver_id=request.POST['driver'])
        fetch_data=WasteRequestDetails.objects.filter(user_id=request.session['req_user'],date=request.session['req_date'])
        temp_data=TempryRequest.objects.filter(user_id=request.session['req_user'],date=request.session['req_date'])
        
        for i in fetch_data:
            i.status='driver assigned'
            i.driver_id=dr_id
            i.save()
        for i in temp_data:
            i.status='driver_assigned'
            i.driver_id=dr_id
            i.save()
        # temp_data=TempryRequest.objects.filter(user_id=request.session['req_user'],date=request.session['req_date'])
        # temp_data.delete()
        user_mail=temp_data[0].user_id.user_email
        req_data=temp_data[0].date
        driver_name=temp_data[0].driver_id.driver_name
        driver_vehicle=temp_data[0].driver_id.driver_vehicle
        driver_assign(user_mail,req_data,driver_name,driver_vehicle)
        
        return redirect("pswms:member_home")
    else:
        user= request.GET.get('user')
        date= request.GET.get('date')
        drivers_list=DriverDetails.objects.filter(driver_ward=request.session['ward_id'])
        requested_data=WasteRequestDetails.objects.filter(user_id=user,date=date)
        # request.session['req_data']=requested_data
        user_name=requested_data[0].user_id.user_name
        phone_no=requested_data[0].user_id.user_phno
        address=requested_data[0].user_id.user_address
        request.session['req_user']=requested_data[0].user_id.user_id
        request.session['req_date']=str(requested_data[0].date)
        img=requested_data[0].user_id.user_img
        context={
        'requested_data':requested_data,
        'drivers_list':drivers_list,
        'user_name':user_name,
        'phno':phone_no,
        'address':address,
        'img':img,
        'm':request.session['m_name'],
        'p':request.session['p_nme'],
        'c':request.session['usr_count']
        }
        
        return render(request,'pswms/Member/RequestDetails.html',context)



@auth_user
def WastePickUpRequest(request):
    form=WastePickUpForm()
    payment_form=PaymentForm()
    bin_details=BinDetails.objects.filter(pan_id=request.session['pan_id'])
    request_date="2021-07-13"
    total_qty=0
    payment_success=request.GET.get('success')
    
    if payment_success=='1':
       
        
        ward_id=WardDetails.objects.get(ward_id=request.session['ward_id'])
        
        waste_id=WasteDetails.objects.get(waste_id=request.session['waste_id'])
        bin=BinDetails.objects.get(bin_id=request.session['bin'])
        user=UserDetails.objects.get(user_id=request.session['user_id'])
        qry=WasteRequestDetails(waste_id=waste_id,pan_id=request.session['pan_id'],date=request_date, ward_id=ward_id, user_id=user,qty=request.session['qty'],total_price=request.session['tot'],status="pending",payment_type='online',payment_status="completed",bin_id=bin)
        qry.save()
                            
        temp_add=TempryRequest.objects.filter(user_id=request.session['user_id'],date=request_date,status='pending')
        
        if not temp_add:
            data=UserDetails.objects.get(user_id=request.session['user_id'])
            ward=WardDetails.objects.get(ward_id=request.session['ward_id'])
            TempryRequest(user_id=data,date=request_date,status='pending',ward_id=ward).save()
                               
    waste_type=WasteDetails.objects.all()
    if request.method=='POST':
        form=WastePickUpForm(request.POST)
        if form.is_valid():
            payment_type=form.cleaned_data['payment_type']
           

            total=form.cleaned_data['total']
            qty=form.cleaned_data['qty']
            request.session['qty']=qty
            request.session['tot']=total
            request.session['bin']=request.POST['bin']
            bin=BinDetails.objects.get(bin_id=request.POST['bin'])
            ward_id=WardDetails.objects.get(ward_id=request.session['ward_id'])
            user_id=UserDetails.objects.get(user_id=request.session['user_id'])
            waste_id=WasteDetails.objects.get(waste_id=request.POST['waste'])
            request.session['waste_id']=waste_id.waste_id
            request_data=WasteRequestDetails.objects.filter(user_id=user_id,date=request_date)
            for i in request_data:
                total_qty=total_qty+i.qty
            if request_data and total_qty<=7:

                if total_qty<7:
                    allowed_qty=7-total_qty
                    if qty<=allowed_qty:
                            
                        if payment_type=='offline':       
                            qry=WasteRequestDetails(waste_id=waste_id,date=request_date, ward_id=ward_id, user_id=user_id,qty=qty,total_price=total,status="pending",payment_type=payment_type,bin_id=bin)
                            qry.save()
                            
                            temp_add=TempryRequest.objects.filter(user_id=request.session['user_id'],date=request_date,status='pending')
                            if not temp_add:
                                data=UserDetails.objects.get(user_id=request.session['user_id'])
                                ward=WardDetails.objects.get(ward_id=request.session['ward_id'])
                                TempryRequest(user_id=data,date=request_date,status='pending',ward_id=ward).save()
                                
                            success_msg="Request Success"
                        else:
                            online=True
                            return render(request,'pswms/Users/WasteRequest.html',{'form':form,'payment_form':payment_form,'waste_type':waste_type,'online':online,'bin_list':bin_details})
                        return render(request,'pswms/Users/WasteRequest.html',{'form':form,'waste_type':waste_type,'success_msg':success_msg,'bin_list':bin_details})
                        
                        

                    else:
                        error_msg="Remaining Quantity Allowed For Today is Only "+str(allowed_qty)+" Kg"
                    return render(request,'pswms/Users/WasteRequest.html',{'form':form,'waste_type':waste_type,'error_msg':error_msg,'bin_list':bin_details})    
                else:
                    error_msg="Your Daily Limit Exceeded"
                    return render(request,'pswms/Users/WasteRequest.html',{'form':form,'waste_type':waste_type,'error_msg':error_msg,'bin_list':bin_details})
            elif not request_data and total_qty<=7:
                if total_qty<7:
                    allowed_qty=7-total_qty
                    if qty<=allowed_qty:
                        if payment_type=='offline':           
                            temp_add=TempryRequest.objects.filter(user_id=request.session['user_id'],date=request_date)
                            if not temp_add:
                                data=UserDetails.objects.get(user_id=request.session['user_id'])
                                ward=WardDetails.objects.get(ward_id=request.session['ward_id'])
                                TempryRequest(user_id=data,date=request_date,status='pending',ward_id=ward).save()
                        
                            qry=WasteRequestDetails(waste_id=waste_id,date=request_date, ward_id=ward_id, user_id=user_id,qty=qty,total_price=total,status="pending",payment_type=payment_type,bin_id=bin)
                            qry.save()
                        
                            
                            success_msg="Request Success"
                            return render(request,'pswms/Users/WasteRequest.html',{'form':form,'waste_type':waste_type,'success_msg':success_msg,'bin_list':bin_details})
                    
                        else:
                            online=True
                            return render(request,'pswms/Users/WasteRequest.html',{'form':form,'payment_form':payment_form,'waste_type':waste_type,'online':online,'bin_list':bin_details})
                    else:
                        error_msg="Remaining Quantity Allowed For Today is Only "+str(allowed_qty)+" Kg"
                    return render(request,'pswms/Users/WasteRequest.html',{'form':form,'waste_type':waste_type,'error_msg':error_msg,'bin_list':bin_details})    
                else:
                    error_msg="Your Daily Limit Exceeded"
                    return render(request,'pswms/Users/WasteRequest.html',{'form':form,'waste_type':waste_type,'error_msg':error_msg,'bin_list':bin_details})
    # print(TempryRequest.objects.get(user_id=request.session['user_id'],date=request_data).query)
    return render(request,'pswms/Users/WasteRequest.html',{'form':form,'waste_type':waste_type,'card_form':PaymentForm,'bin_list':bin_details})




@auth_member
def ViewComplaint(request):
    complaints=ComplaintDetails.objects.filter(reply="pending",recipient_type="1",ward_id=request.session['ward_id']) 
    context={
        'complaints':complaints,
        'm':request.session['m_name'],
        'p':request.session['p_nme'],
        'c':request.session['usr_count']
        }
    return render(request,'pswms/Member/ViewComplaint.html',context)


@auth_admin
def AdminViewComplaint(request):
    complaints=ComplaintDetails.objects.filter(recipient_type=0,reply="pending")
    return render(request,'pswms/SuperAdmin/ViewComplaint.html',{'complaints':complaints,})
    
@auth_admin
def MemberComplaint(request):
    panchayath_list=PanchayathDetails.objects.all()
    if request.method=="POST":
        ward_id=request.POST["ward"]
        complaints=ComplaintDetails.objects.filter(recipient_type=1,ward_id=ward_id)
        return render(request,'pswms/SuperAdmin/MemberComplaints.html',{'complaints':complaints,'panchayath_list':panchayath_list})
    return render(request,'pswms/SuperAdmin/MemberComplaints.html',{'panchayath_list':panchayath_list})



def ForgotPassword(request,login_id):
    form=LoginForm()
   
    
    if '@' in str(login_id):
       
        
        email_exist=UserDetails.objects.filter(user_email=login_id).exists()
        try:
            if email_exist:
                user_data=UserDetails.objects.get(user_email=login_id)
                user_email=user_data.user_email
                usrpaswd=get_random_string(length=8)
                forgot_pass(user_email,usrpaswd)
                enc_passwd=pbkdf2_sha256.hash(usrpaswd,rounds=1000,salt_size=32)
                user_data.user_passwd=enc_passwd
                user_data.save()
               
                
        except Exception as e:
           pass

        return render(request,'pswms/Common/CommonLogin.html',{'form':form})

    if re.match(r'[a-z A-Z]',login_id):
        # print("asdsdgsd")
        do_exist=PanchayathMemberDetails.objects.filter(p_user_name=login_id).exists()
        if do_exist:
            member_data=PanchayathMemberDetails.objects.get(p_user_name=login_id)
            member_mail=member_data.p_email          
            passwd=get_random_string(length=8)
            forgot_pass(member_mail,passwd)
            enc_passwd=pbkdf2_sha256.hash(passwd,rounds=1000,salt_size=32)
            member_data.p_passwd=enc_passwd
            member_data.save()
            # msg="New Password has been sent to your mail"
        return render(request,'pswms/Common/CommonLogin.html',{'form':form})

    if login_id.isdigit():
        data_exist=DriverDetails.objects.filter(driver_id=login_id).exists()
        if data_exist:
            driver_data=DriverDetails.objects.get(driver_id=login_id)
            driver_email=driver_data.driver_email
            passwed=get_random_string(length=8)
            forgot_pass(driver_email,passwed)
            enc_passwd=pbkdf2_sha256.hash(passwed,rounds=1000,salt_size=32)
            driver_data.driver_passwd=enc_passwd
            driver_data.save()
        return render(request,'pswms/Common/CommonLogin.html',{'form':form})



@auth_member
def ViewPayment(request):
    view_payment=TempryRequest.objects.filter(ward_id=request.session['ward_id']).order_by('date')
    print(view_payment)
    context={
        'payments':view_payment,
        'm':request.session['m_name'],
        'p':request.session['p_nme'],
        'c':request.session['usr_count']
        }
    return render(request,'pswms/Member/ViewPayment.html',context)   
    

def PaymentDetails(request):
    
    if request.method=='POST':
        # driver=DriverDetails.objects.get(driver_id=request.POST['driver'])
        print(request.session['req_user'])
        print(request.session['req_date'])
        # driver=request.POST['driver']
        # dr_id=DriverDetails.objects.get(driver_id=request.POST['driver'])
        # fetch_data=WasteRequestDetails.objects.filter(user_id=request.session['req_user'],date=request.session['req_date'])
        temp_data=TempryRequest.objects.filter(user_id=request.session['req_user'],date=request.session['req_date'])
        user_mail=temp_data[0].user_id.user_email
        req_data=temp_data[0].date
        # driver_name=temp_data[0].driver_id.driver_name
        # driver_vehicle=temp_data[0].driver_id.driver_vehicle
        # driver_assign(user_mail,req_data,driver_name,driver_vehicle)
        
        return redirect("pswms:member_home")
    else:
        user= request.GET.get('user')
        date= request.GET.get('date')
        # drivers_list=DriverDetails.objects.filter(driver_ward=request.session['ward_id'])
        requested_data=WasteRequestDetails.objects.filter(user_id=user,date=date)
        user_name=requested_data[0].user_id.user_name
        phone_no=requested_data[0].user_id.user_phno
        address=requested_data[0].user_id.user_address
        request.session['req_user']=requested_data[0].user_id.user_id
        request.session['req_date']=str(requested_data[0].date)
        img=requested_data[0].user_id.user_img
        context={
        'requested_data':requested_data,
        
        'user_name':user_name,
        'phno':phone_no,
        'address':address,
        'img':img
        }
        
        return render(request,'pswms/Member/PaymentDetails.html',context)

@auth_user
def PaymentHistory(request): 
    requested_data=TempryRequest.objects.filter(user_id=request.session['user_id']) 
    return render(request,'pswms/Users/ViewPaymentHistory.html',{'requested_data':requested_data})

def PaymentData(request):
    date= request.GET.get('date')
    payment_data=WasteRequestDetails.objects.filter(user_id=request.session['user_id'],date=date)
    print(request.session['user_id'],date,payment_data)
    return render(request,'pswms/Users/PaymentHistory.html',{'payment_data':payment_data})

@auth_driver
def DriverCompletedWorks(request):
    work_completed=TempryRequest.objects.filter(driver_id=request.session['driver_id'],status='completed')
   
    return render(request,'pswms/Driver/CompletedWork.html',{'works':work_completed})
            
@auth_member
def CompletedWorks(request):
    work_completed=TempryRequest.objects.filter(ward_id=request.session['ward_id'],status='completed')
    context={
        'works':work_completed,
        'm':request.session['m_name'],
        'p':request.session['p_nme'],
        'c':request.session['usr_count']
        
    }
    return render(request,'pswms/Member/CompletedWorkDetails.html',context)        

   
@auth_admin
def AdminDownloadUserData(request,u_id):
    user_data=UserDetails.objects.get(user_id=u_id)
    ward=user_data.user_ward.ward_id
    member=PanchayathMemberDetails.objects.get(ward_id=ward,p_status="Active")
    member_sign=MemberSignature.objects.get(member_id=member.pid)

    if user_data.user_status=='rejected' or user_data.user_status=='blocked':
        st="red"
    else:
        st="green"
    return Create_pdf('pswms/SuperAdmin/UserDataPdf.html',{'user':user_data,'st':st,'sign':member_sign})                  


@auth_admin
def ReplyUser(request):
    
    
   
    if request.method=='POST':
        
        fetch_data=ComplaintDetails.objects.get(id=request.session['c_id'])
       
        fetch_data.reply=request.POST['reply'].strip()
        fetch_data.save()
            
        del request.session['c_id']
        return redirect("pswms:admin_view_complaint") 
    request.session['c_id']= request.GET.get('user')
    
    
    return render(request,'pswms/SuperAdmin/ReplyUser.html') 

@auth_member
def MemberReplyUser(request):
    if request.method=='POST':
        
        fetch_data=ComplaintDetails.objects.get(id=request.session['c_id'])
       
        fetch_data.reply=request.POST['reply'].strip()
        fetch_data.save()
            
        del request.session['c_id']
        return redirect("pswms:view_complaint")
    request.session['c_id']= request.GET.get('user')
    context={
        'm':request.session['m_name'],
        'p':request.session['p_nme'],
        'c':request.session['usr_count']
    }
    return render(request,'pswms/Member/ReplyUser.html',context) 

@auth_user  
def AssignedDriver(request):
    request_data=TempryRequest.objects.filter(user_id=request.session['user_id'],status='driver_assigned')
    return render(request,'pswms/Users/AssignedDriverDetails.html',{'request_data':request_data,}) 

@auth_member
def  MemberChart(request):
    labels=[]
    data=[]
    total=0
    waste_details=WasteDetails.objects.all()
    payment_online=WasteRequestDetails.objects.filter(ward_id=request.session['ward_id'],payment_type='online').count()
    payment_offline=WasteRequestDetails.objects.filter(ward_id=request.session['ward_id'],payment_type='offline').count()
    
    payment_data=[payment_online,payment_offline]
    print(payment_data,'gdf')
    payment_label=['online','offline']
    new_size=[random.randint(10,30),random.randint(10,30)]
    new_explode=(0.1,0)
    newfig1, ax2=plt.subplots()
    ax2.pie(payment_data,labels=payment_label,autopct='%1.1f%%',
            shadow=True,startangle=90,colors=("g","pink"))
    ax2.axis('equal')
    plt.savefig('media/pay_chart.png',dpi=100)
    
    for waste in waste_details:
        total=0
        total_wst=WasteRequestDetails.objects.filter(ward_id=request.session['ward_id'],waste_id=waste.waste_id)
        for i in total_wst:
           
            total=total+i.qty
        
        # for i in total_wst:
        #     total=total+i.qty
        data.append(total)
        
        
        labels.append(waste.waste_type.title())
    lb=str(labels)

    lb=lb.lstrip("[")
    lb=lb.rstrip("]")
    x=list(labels)
    size=[random.randint(10,30),random.randint(10,30)]
    explode=(0.1,0)
    fig1, ax1=plt.subplots()
    ax1.pie(data,labels=x,autopct='%1.1f%%',
            shadow=True,startangle=90,colors=("y","g","r","pink"))
    ax1.axis('equal')
    plt.savefig('media/waste_chart.png',dpi=100)
        
        
    return render(request,"pswms/Member/Chart.html")


def  PayChart(request):
    labels=[]
    data=[]
    tot=0
    
    payment_details=WasteRequestDetails.objects.all()
    
    for payment in payment_details:
        tot=0
        tot=WasteRequestDetails.objects.filter(ward_id=request.session['ward_id'],payment_type='online').count
        print(tot,'dfdzxz')
        for i in tot:
           
            tot=tot+i.qty
        data.append(tot)
        labels.append(payment.payment_type.title())
    lb=str(labels)

    lb=lb.lstrip("[")
    lb=lb.rstrip("]")
    x=list(labels)
    size=[random.randint(10,30),random.randint(10,30)]
    explode=(0.1,0)
    fig1, ax1=plt.subplots()
    ax1.pie(data,labels=x,autopct='%1.1f%%',
            shadow=True,startangle=90,colors=("y","g","r","pink"))
    ax1.axis('equal')
    plt.savefig('media/waste_chart.png',dpi=100)    
    return render(request,"pswms/Member/Chart.html")


@auth_admin
def BarChart(request):
    panchayath=PanchayathDetails.objects.all()
    waste_count=[]
    count=0
    x=[]
    for p in  panchayath:
        x.append(p.pan_name)
        waste_data=WasteRequestDetails.objects.filter(pan_id=p.pan_id)
        exist=WasteRequestDetails.objects.filter(pan_id=p.pan_id).exists()
        count=0
        
        if not exist:
            
            waste_count.append(0)
        else:
            for i in waste_data:
                count=count+int(i.qty)
            waste_count.append(count)
    print("waste count",waste_count)
    
    # Ygrl=[10,20,20,40,21,33]
    # Z_boy=[20,30,25,30,21,89]
    # X_axis = np.arange(len(x))
   
    # plt.bar(X_axis - 0.2, x, 0.4, label='waste')
    # plt.bar(X_axis + 0.2, x, 0.4, label='payment')
    # plt.xticks(X_axis,x)
    # plt.xlabel("Group")
    # plt.ylabel("Number of student")
    # plt.title("Number of student")
    # plt.legend()
   
    y_pos = np.arange(len(x))
    
    plt.bar(y_pos, waste_count, align='center', alpha=0.5)
    plt.xticks(y_pos, x)
    plt.ylabel('Quantity')
    plt.title(' over all Waste')
    plt.savefig('media/barchart.png')
    

    return render(request,"pswms/SuperAdmin/Chart.html")