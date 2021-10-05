from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import *
import re



class LoginForm(forms.Form):
    user_name=forms.CharField(label="User Name",widget=forms.TextInput(attrs={'class':'form-control',}))
    passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))
    
    
class PanchayathForm(forms.ModelForm):
    pan_name=forms.CharField(label="Panchayath Name", widget=forms.TextInput(attrs={'class':'form-control',}),)
    
    class Meta:
        model=PanchayathDetails
        fields=('pan_name',)
    
    def clean_pan_name(self):
        name=self.cleaned_data['pan_name']
        if not re.match(r'^[A-Za-z]+$', name):
            raise forms.ValidationError("Name should be a  of Alphabets only ")
        return name



class BinForm(forms.ModelForm):
    bin_name=forms.CharField(label=" Enter Bin Name",widget=forms.TextInput(attrs={'class':'form-control',}))

    class Meta:
        model=BinDetails
        fields=('bin_name',)



class WardForm(forms.ModelForm):
    ward_no=forms.CharField(label="Ward No",widget=forms.NumberInput(attrs={'class':'form-control',}))

    class Meta:
        model=WardDetails
        fields=('ward_no',)
    def clean_ward_no(self):
        num=self.cleaned_data['ward_no']
        if int(num)<=0:
            raise forms.ValidationError("Invalid Price")
        return num

class NotificationForm(forms.ModelForm):
    notification_title=forms.CharField(label="Title",widget=forms.TextInput(attrs={'class':'form-control'}))
    notification=forms.CharField(label="Notification",widget=forms.Textarea(attrs={'class':'form-control','rows':'6','cols':'6'}))
    
    class Meta:
        model=NotificationDetails
        fields=('notification',)
    

class PanchayathMemberForm(forms.ModelForm):
    gender_choice=(
            ('male','Male'),
            ('female','Female'),
        )
    p_name=forms.CharField(label="Member Name", widget=forms.TextInput(attrs={'class':'form-control'}))
    p_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'row':5,'col':5,'class':'form-control'}))
    p_dob=forms.CharField(label="D.O.B",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'dd/mm/yyy'}))
    p_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choice))
    p_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control'}))
    p_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'class':'form-control',}))
    p_img=forms.ImageField(label="Select Picture",widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model=PanchayathMemberDetails
        fields=('p_name','p_address','p_dob','p_gender','p_email','p_phno','p_img')
    def clean_p_name(self):
        name=self.cleaned_data['p_name']
        if not re.match(r'^[A-Z a-z ]+$', name):
            raise forms.ValidationError("Name should be a  of Alphabets only ")
        return name
    def clean_p_phno(self):
        phone=self.cleaned_data['p_phno']
        length=len(str(phone))
        if length!=10:
            raise forms.ValidationError("Phone number must be 10 digits")
        return phone
    def clean_p_email(self):
        email=self.cleaned_data['p_email']
        if not re.match(r'\b[\w.-]+@[\w.-]+.\w{2,4}\b', email):
            raise forms.ValidationError("Email should be of correct format")
        return email


class MemberUpdateForm(forms.ModelForm):
    gender_choice=(
            ('male','Male'),
            ('female','Female'),
        )
    p_name=forms.CharField(label="Member Name", widget=forms.TextInput(attrs={'class':'form-control','readonly':'true'}))
    p_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'row':5,'col':5,'class':'form-control'}))
    p_dob=forms.CharField(label="D.O.B",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'dd/mm/yyy','readonly':'true'}))
    p_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choice))
    p_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control'}))
    p_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'class':'form-control',}))
    p_year=forms.CharField(label="year",widget=forms.TextInput(attrs={'class':'form-control','readonly':'true'}))
    #p_img=forms.ImageField(label="Select Picture",widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model=PanchayathMemberDetails
        fields=('p_name','p_address','p_dob','p_gender','p_email','p_phno','p_year')
    def clean_p_name(self):
        name=self.cleaned_data['p_name']
        if not re.match(r'^[A-Z a-z ]+$', name):
            raise forms.ValidationError("Name should be a  of Alphabets only ")
        return name
    def clean_p_phno(self):
        phone=self.cleaned_data['p_phno']
        length=len(str(phone))
        if length!=10:
            raise forms.ValidationError("Phone number must be 10 digits")
        return phone
    def clean_p_email(self):
        email=self.cleaned_data['p_email']
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email):
            raise forms.ValidationError("Email should be of correct format")
        return email



class UserRegForm(forms.ModelForm):
    gender_choice=(
            ('male','Male'),
            ('female','Female'),
        )
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name',}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name',}))
    user_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'7','cols':'15','class':'form-control'}))
    user_dob=forms.CharField(label="D.O.B",widget=forms.DateInput(attrs={'placeholder':'dd/mm/yyyy','class':'form-control','style':'position:relative; top:40px'}))
    user_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choice,))
    user_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email',}))
    user_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Contact No','style':'position:relative; top:10px'}))
    user_house_no=forms.CharField(label="House No",widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'House No',}))
    user_img=forms.ImageField(label="Select Picture",widget=forms.FileInput(attrs={'class':'form-control',}))
    user_passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password',}))
    confirm_passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Again',}))
    class Meta:
        model=UserDetails
        fields=('user_address','user_dob','user_gender','user_email','user_phno','user_img','user_passwd','user_house_no')
    def clean_user_name(self):
        uname=self.cleaned_data['user_name']
        if not re.match(r'^[A-Z a-z ]+$',uname):
            raise forms.ValidationError("Name should be a  of Alphabets only ")
        return uname
    def clean_user_phno(self):
        uphone=self.cleaned_data['user_phno']
        length=len(str(uphone))
        if length!=10:
            raise forms.ValidationError("Phone number must be 10 digits")
        return uphone
    def clean_user_email(self):
        uemail=self.cleaned_data['user_email']
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",uemail):
            raise forms.ValidationError("Email should be of correct format")
        return uemail



class ChangePasswordForm(forms.Form):
    old_passwd=forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))
    new_passwd=forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))
    confirm_passwd=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:300px'}))

class SearchForm(forms.ModelForm):
    user_name=forms.CharField(widget=forms.TextInput(attrs={'style':'width:250px'}))
    
    class Meta:
        model=UserDetails
        fields=('user_name',)



class DriverRegForm(forms.ModelForm):
    gender_choice=(
            ('male','Male'),
            ('female','Female'),
        )
    language_choice=(
        ('Malayalam','Malayalam'),
        ('Hindi','Hindi'),
        ('English','English'),
    )
    qualification=(
        ('sslc','SSLC'),
        ('hse','HSE'),
        ('ug','UG'),
    )
    driver_name=forms.CharField(widget=forms.TextInput(attrs={'style':'width:200px; height:25px',}))
    driver_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'7','cols':'15','class':'form-control'}))
    driver_dob=forms.CharField(label="D.O.B",widget=forms.DateInput(attrs={'placeholder':'dd/mm/yyyy','style':'width:200px; height:25px',}))
    driver_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choice,))
    driver_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'style':'width:200px; height:25px',}))
    driver_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'style':'width:200px; height:25px',}))
    driver_img=forms.ImageField(label="Select Picture",widget=forms.FileInput())
    driver_vehicle=forms.CharField(label="Vehicle No",widget=forms.TextInput(attrs={'style':'width:200px; height:25px',}))
    driver_language=forms.CharField(label="language Known",widget=forms.CheckboxSelectMultiple(choices=language_choice))
    driver_qualification=forms.CharField(label="qualification",widget=forms.Select(choices=qualification))
    class Meta:
        model=DriverDetails
        fields=('driver_name','driver_address','driver_dob','driver_gender','driver_email','driver_phno','driver_img','driver_vehicle')



class WasteForm(forms.ModelForm):
    waste_type=forms.CharField(label="Waste Type",widget=forms.TextInput(attrs={'style':'width:250px','class':'form-control'}))
    waste_price=forms.FloatField(label="Price",widget=forms.NumberInput(attrs={'step':'1.0','style':'width:250px','class':'form-control'}))

    class Meta:
        model=WasteDetails
        fields=('waste_type','waste_price',)

    def clean_waste_type(self):
        waste_type=self.cleaned_data['waste_type']
        if not re.match(r'^[A-Z a-z  ]+$', waste_type):
            raise forms.ValidationError("Waste Type Should Not Contain Numbers")
        return waste_type
    def clean_waste_price(self):
        price=self.cleaned_data['waste_price']
        if price<=0:
            raise forms.ValidationError("Invalid Price")
        return price

class WastePickUpForm(forms.ModelForm):
    total=forms.CharField(label="Total",widget=forms.TextInput(attrs={'style':'width:250px','class':'form-control'}))
    class Meta:
        models=WasteRequestDetails
        fields=('qty',)


    def clean_qty(self):
        qty=self.cleaned_data['qty']
        if qty<=0:
            raise forms.ValidationError("Invalid Data")
            return qty


class UpdateUserProfileForm(forms.ModelForm):
    gender_choice=(
            ('male','Male'),
            ('female','Female'),
        )
    # first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name','readonly':'true' }))
    # last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name',}))
    user_address=forms.CharField(label="Address",widget=forms.Textarea(attrs={'rows':'7','cols':'15','class':'form-control'}))
    # user_dob=forms.CharField(label="D.O.B",widget=forms.DateInput(attrs={'placeholder':'dd/mm/yyyy','class':'form-control','style':'position:relative; top:40px'}))
    user_gender=forms.CharField(label="Gender",widget=forms.RadioSelect(choices=gender_choice))
    user_email=forms.CharField(label="Email",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email',}))
    user_phno=forms.CharField(label="Phone No",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Contact No','style':'position:relative; top:10px'}))
    # user_house_no=forms.CharField(label="House No",widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'House No',}))
    # user_img=forms.ImageField(label="Select Picture",widget=forms.FileInput(attrs={'class':'form-control',}))
    # user_passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password',}))
    # confirm_passwd=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Again',}))
    class Meta:
        model=UserDetails
        fields=('user_name','user_address','user_gender','user_email','user_phno')
    def clean_user_name(self):
        uname=self.cleaned_data['user_name']
        if not re.match(r'^[A-Z a-z ]+$',uname):
            raise forms.ValidationError("Name should be a  of Alphabets only ")
        return uname
    def clean_user_phno(self):
        uphone=self.cleaned_data['user_phno']
        length=len(str(uphone))
        if length!=10:
            raise forms.ValidationError("Phone number must be 10 digits")
        return uphone
    def clean_user_email(self):
        uemail=self.cleaned_data['user_email']
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",uemail):
            raise forms.ValidationError("Email should be of correct format")
        return uemail



class WastePickUpForm(forms.ModelForm):
    payment_choices=(
        ('online','Online'),
        ('offline','Offline')
    )
    qty=forms.IntegerField(label="Quantity",widget=forms.NumberInput(attrs={'style':'width:250px','class':'form-control'}))
    total=forms.CharField(label="Total",widget=forms.TextInput(attrs={'style':'width:250px','class':'form-control','readonly':'true'}))
    payment_type=forms.CharField(label="Payment Type",widget=forms.Select(choices=payment_choices,attrs={'style':'width:250px','class':'form-control'}))
    class Meta:
        model=WasteRequestDetails
        fields=('qty',)


    def clean_qty(self):
        qty=self.cleaned_data['qty']
        if qty<=0:
            raise forms.ValidationError("Invalid Data")
        return qty


class PaymentForm(forms.Form):
    card_exp_frm=()
    card_choices=(
        ('Debit','Debit'),
        ('Credit','Credit')
    )
    
    for exp_from in range(2002,2071):
        card_exp_frm=card_exp_frm+((exp_from,exp_from))
        card_holder=forms.CharField(label="Card Holder Name",widget=forms.TextInput(attrs={'style':'width:250px','class':'form-control'}))
        card_no=forms.CharField(label="Card No",widget=forms.TextInput(attrs={'style':'width:250px','class':'form-control'}))
        card_type=forms.CharField(label="Card Type",widget=forms.Select(choices=card_choices,attrs={'style':'width:250px','class':'form-control'}))
    # exp_from=forms.CharField(widget=forms.Select(choices=card_exp_frm))
    
    amount=forms.FloatField(label="Total Amount",widget=forms.TextInput(attrs={'style':'width:250px','class':'form-control'}))

class ComplaintForm(forms.ModelForm):
    complaint=forms.CharField(label="Complaint",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Complaint'}))

    class Meta:
        model=ComplaintDetails
        fields=('complaint',)
    
  

