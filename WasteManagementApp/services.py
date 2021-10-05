from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
from django.shortcuts import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from .models import DriverDetails
from django.core.paginator import Paginator
import os
import random

def email_admin(mail_recipient,user_name,passwd):
    subject="username and password"
    message="Hi your username is "+user_name+" and temporary password is "+passwd
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)



def email_user(mail_recipient,account_status):
    subject="Account Approval"
    message="Hi your Account has been "+account_status+ " by Panchayath Member"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient]
    send_mail(subject,message,email_from,recipient_list)


def email_driver(mail_recipient,user_name,passwd):
    subject="username and password"
    message="Hi your username is "+ str(user_name)+" and temporary password is "+passwd
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)



def fetch_resources(url,rel):
    path=os.path.join(url.replace(settings.STATIC_URL,""))
    return path


def Create_pdf(path: str, params: dict):
    template = get_template(path)
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response,link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(response.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error Renderingn PDF", status= 400)




def unique_id():
    rand = random.random()
    rand_id=int(rand*10000)
    exist=DriverDetails.objects.filter(driver_id=rand_id)
    if exist:
        unique_id()
    return rand_id



def get_pagination(pg_no,cur_page,list):
    p=Paginator(list,pg_no)
    current_page=cur_page
    list=p.get_page(current_page)
    return list

def forgot_pass(mail_recipient,passwd):
    subject="old password"
    message="Hi your old password is "+str(passwd) 
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient]
    send_mail(subject,message,email_from,recipient_list)

def delay_user(mail_recipient,req_date,delay_date):
    
    subject="waste pick up delay "
    message="Hi your waste pick up request dated on "+str(req_date)+" is delayed by "+str(delay_date)
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)


def driver_assign(mail_recipient,date,driver_name,vehicle_no):
    
    subject="request details"
    message="Hi your waste pick up request has been recorded "+str(date)+" will be collected by "+str(driver_name)  +"("+str(vehicle_no)+ " )."
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[mail_recipient,]
    send_mail(subject,message,email_from,recipient_list)