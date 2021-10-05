from django import db
from django.db import models
from numpy import mod
from passlib.hash import pbkdf2_sha256
# Create your models here.


class AdminDetails(models.Model):
    login_id=models.CharField(max_length=20,db_column="log_id")
    login_passwd=models.CharField(max_length=120,db_column='passwd')

    class Meta:
        db_table="tb_super"

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.login_passwd)


class PanchayathDetails(models.Model):
    pan_id=models.AutoField(primary_key=True,db_column='pan_id')
    pan_name=models.CharField(max_length=20,db_column='p_name')

    class Meta:
        db_table="tb_panchayath"
    

class PanchayathMemberDetails(models.Model):
    pid=models.AutoField(primary_key=True,db_column="m_id")
    ward_id=models.IntegerField(default=0)
    p_name=models.CharField(max_length=20,db_column="m_name")
    p_gender=models.CharField(max_length=10,db_column="m_gender")
    p_dob=models.CharField(max_length=20,db_column="m_dob")
    p_address=models.CharField(max_length=200,db_column="m_addr")
    p_email=models.CharField(max_length=50,db_column="m_email")
    p_phno=models.IntegerField(db_column="m_iph")
    p_img=models.ImageField(upload_to="Members/",db_column="m_pic")
    p_user_name=models.CharField(max_length=20,db_column="m_uname")
    p_passwd=models.CharField(max_length=120,db_column="m_passwd")
    p_year=models.CharField(max_length=20,db_column="m_year")
    p_status=models.CharField(max_length=20,db_column="m_status")
    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.p_passwd)

    class Meta:
        db_table='tb_pachayathMember'

class MemberSignature(models.Model):
    member_id=models.ForeignKey(PanchayathMemberDetails,on_delete=models.CASCADE,db_column="m_id")
    member_sign=models.ImageField(upload_to="Sign/",db_column="m_sign")
    class Meta:
        db_table='tb_sign'


class WardDetails(models.Model):
    ward_id=models.AutoField(primary_key=True,db_column="w_id")
    pan_id=models.ForeignKey(PanchayathDetails,on_delete=models.CASCADE,db_column="p_id")
    ward_no=models.IntegerField(db_column="w_no")
    ward_member=models.ForeignKey(PanchayathMemberDetails, on_delete=models.SET_NULL,blank=True, null=True,db_column="w_member")
    
    class Meta:
        db_table="tb_wardDetails"


class NotificationDetails(models.Model):
    n_id=models.AutoField(primary_key=True,db_column="not_id")
    date=models.DateField(db_column="date")
    notification_title=models.CharField(max_length=100,db_column="not_title" ,default="")
    notification=models.CharField(max_length=200,db_column="notfn")
    class Meta:
        db_table="tb_notification"



class DriverDetails(models.Model):
    driver_id=models.IntegerField(primary_key=True,db_column="d_id")
    driver_ward=models.ForeignKey(WardDetails,on_delete=models.CASCADE)
    driver_name=models.CharField(max_length=100,db_column="d_name")
    driver_gender=models.CharField(max_length=10,db_column="d_gender")
    driver_dob=models.CharField(max_length=30,db_column="d_dob")
    driver_address=models.CharField(max_length=200,db_column="d_addr")
    driver_email=models.CharField(max_length=50,db_column="d_mail")
    driver_phno=models.IntegerField(db_column="d_ph")
    driver_img=models.ImageField(upload_to="Driver/",db_column="d_pic")
    driver_passwd=models.CharField(max_length=120,db_column="d_passwd")
    driver_status=models.CharField(max_length=20,db_column="d_status")
    driver_work_status=models.CharField(max_length=20,db_column="work_status")
    driver_qualification=models.CharField(max_length=250,default='empty',db_column='d_qualification')
    driver_language=models.CharField(max_length=200,default='empty',db_column='d_language')
    driver_vehicle=models.CharField(max_length=30,db_column="vehicle_number")
    class Meta:
        db_table='tb_driverDetails'

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.driver_passwd)




class UserDetails(models.Model):
    user_id=models.AutoField(primary_key=True,db_column="u_id")
    user_pan=models.ForeignKey(PanchayathDetails,on_delete=models.CASCADE,db_column="p_id")
    user_ward=models.ForeignKey(WardDetails,on_delete=models.CASCADE,db_column="w_id")
    user_name=models.CharField(max_length=100,db_column="u_name")
    user_gender=models.CharField(max_length=10,db_column="u_gender")
    user_dob=models.CharField(max_length=30,db_column="u_dob")
    user_address=models.CharField(max_length=200,db_column="u_addr")
    user_email=models.CharField(max_length=50,db_column="u_mail")
    user_house_no=models.IntegerField(db_column="u_house_no")
    user_phno=models.IntegerField(db_column="u_ph")
    user_img=models.ImageField(upload_to="Users/",db_column="u_pic")
    user_passwd=models.CharField(max_length=120,db_column="u_passwd")
    user_status=models.CharField(max_length=20,db_column="u_status")

    class Meta:
        db_table='tb_userDetails'

    def verifyPasswd(self,raw_passwd):
        return pbkdf2_sha256.verify(raw_passwd,self.user_passwd)


class WasteDetails(models.Model):
    waste_id=models.AutoField(primary_key=True)
    waste_type=models.CharField(max_length=40)
    waste_price=models.FloatField()
    class Meta:
        db_table="tb_wasteDetails"


class BinDetails(models.Model):
    bin_id=models.AutoField(primary_key=True,db_column="bin_id")
    pan_id=models.ForeignKey(PanchayathDetails,on_delete=models.CASCADE,db_column="pan_id")
    bin_name=models.CharField(max_length=30,db_column="bin_name")
    class Meta:
        db_table="tb_bin"


class WasteRequestDetails(models.Model):
    id=models.AutoField(primary_key=True,db_column="req_id")
    user_id=models.ForeignKey(UserDetails,on_delete=models.CASCADE,db_column="usr_id")
    waste_id=models.ForeignKey(WasteDetails,on_delete=models.CASCADE,db_column="wst_id")
    bin_id=models.ForeignKey(BinDetails,on_delete=models.CASCADE,db_column="wst_bin")
    pan_id=models.ForeignKey(PanchayathDetails,on_delete=models.CASCADE,null=True,db_column="pan_id")
    ward_id=models.ForeignKey(WardDetails,on_delete=models.CASCADE,db_column="wrd_id")
    driver_id=models.ForeignKey(DriverDetails,on_delete=models.CASCADE,null=True,blank=True,  db_column="drv_id")
    date=models.DateField(db_column="req_date")
    qty=models.IntegerField(db_column="req_qty")
    payment_type=models.CharField(max_length=10,default="")
    payment_status=models.CharField(max_length=20,db_column="pay_status",default="pending")
    card_holder=models.CharField(max_length=20, default="", db_column="card_holder")
    card_type=models.CharField(max_length=10,default="")
    card_no=models.IntegerField(default=0)
    card_expiry=models.CharField(max_length=30,default="")
    total_price=models.FloatField(db_column="req_total")
    status=models.CharField(max_length=20,db_column="req_status")
    delay_status=models.CharField(max_length=20,db_column="delay")
    
  
    class Meta:
        db_table='tb_waste_request'

class TempryRequest(models.Model):
    id=models.AutoField(primary_key=True,db_column="tmp_id")
    ward_id=models.ForeignKey(WardDetails,on_delete=models.CASCADE,db_column="ward_id",default=0)
    user_id=models.ForeignKey(UserDetails,on_delete=models.CASCADE,db_column="usr_id")
    # member_id=models.ForeignKey(PanchayathMemberDetails,on_delete=models.CASCADE)
    date=models.DateField(db_column="req_date")
    status=models.CharField(max_length=20,default="",db_column="req_status")
    driver_id=models.ForeignKey(DriverDetails,on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        db_table='tb_temp_request'


class ComplaintDetails(models.Model):
    id=models.AutoField(primary_key=True,db_column="cmp_id")
    user_id=models.ForeignKey(UserDetails,on_delete=models.CASCADE,db_column="u_id")
    ward_id=models.ForeignKey(WardDetails,on_delete=models.CASCADE,db_column="w_id")
    recipient_type=models.IntegerField(default=None,db_column="r_type")
    user_complaint=models.CharField(max_length=200,db_column="usr_complaint")
    complaint_date=models.DateField(db_column="complaint_date")
    
    reply=models.CharField(max_length=200,db_column="reply",default="pending")
   

    class Meta:
        db_table='tb_complaint'