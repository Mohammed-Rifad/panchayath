from django.shortcuts import render,redirect
from.models import UserDetails

def auth_admin(func):
    def wrap(request,*args,**kwargs):
        if 'admin_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect('pswms:common_login')


    return wrap


def auth_member(func):
    def wrap(request,*args,**kwargs):
        if 'ward_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect('pswms:common_login')


    return wrap



def auth_user(func):
    def wrap(request,*args,**kwargs):
        data=UserDetails.objects.get(user_id=request.session['user_id'])
        status=data.user_status
        if 'user_id' in request.session and status!='blocked':
            
            return func(request,*args,**kwargs)
        else:
            return redirect('pswms:common_login')


    return wrap


def auth_driver(func):
    def wrap(request,*args,**kwargs):
        if 'driver_id' in request.session:
            return func(request,*args,**kwargs)
        else:
            return redirect('pswms:common_login')


    return wrap