# Generated by Django 3.1.7 on 2021-05-28 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_id', models.CharField(db_column='log_id', max_length=20)),
                ('login_passwd', models.CharField(db_column='passwd', max_length=120)),
            ],
            options={
                'db_table': 'tb_super',
            },
        ),
        migrations.CreateModel(
            name='BinDetails',
            fields=[
                ('bin_id', models.AutoField(db_column='bin_id', primary_key=True, serialize=False)),
                ('bin_name', models.CharField(db_column='bin_name', max_length=30)),
            ],
            options={
                'db_table': 'tb_bin',
            },
        ),
        migrations.CreateModel(
            name='DriverDetails',
            fields=[
                ('driver_id', models.IntegerField(db_column='d_id', primary_key=True, serialize=False)),
                ('driver_name', models.CharField(db_column='d_name', max_length=100)),
                ('driver_gender', models.CharField(db_column='d_gender', max_length=10)),
                ('driver_dob', models.CharField(db_column='d_dob', max_length=30)),
                ('driver_address', models.CharField(db_column='d_addr', max_length=200)),
                ('driver_email', models.CharField(db_column='d_mail', max_length=50)),
                ('driver_phno', models.IntegerField(db_column='d_ph')),
                ('driver_img', models.ImageField(db_column='d_pic', upload_to='Driver/')),
                ('driver_passwd', models.CharField(db_column='d_passwd', max_length=120)),
                ('driver_status', models.CharField(db_column='d_status', max_length=20)),
                ('driver_work_status', models.CharField(db_column='work_status', max_length=20)),
                ('driver_vehicle', models.CharField(db_column='vehicle_number', max_length=30)),
            ],
            options={
                'db_table': 'tb_driverDetails',
            },
        ),
        migrations.CreateModel(
            name='NotificationDetails',
            fields=[
                ('n_id', models.AutoField(db_column='not_id', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='date')),
                ('notification_title', models.CharField(db_column='not_title', default='', max_length=100)),
                ('notification', models.CharField(db_column='notfn', max_length=200)),
            ],
            options={
                'db_table': 'tb_notification',
            },
        ),
        migrations.CreateModel(
            name='PanchayathDetails',
            fields=[
                ('pan_id', models.AutoField(db_column='pan_id', primary_key=True, serialize=False)),
                ('pan_name', models.CharField(db_column='p_name', max_length=20)),
            ],
            options={
                'db_table': 'tb_panchayath',
            },
        ),
        migrations.CreateModel(
            name='PanchayathMemberDetails',
            fields=[
                ('pid', models.AutoField(db_column='m_id', primary_key=True, serialize=False)),
                ('ward_id', models.IntegerField(default=0)),
                ('p_name', models.CharField(db_column='m_name', max_length=20)),
                ('p_gender', models.CharField(db_column='m_gender', max_length=10)),
                ('p_dob', models.CharField(db_column='m_dob', max_length=20)),
                ('p_address', models.CharField(db_column='m_addr', max_length=200)),
                ('p_email', models.CharField(db_column='m_email', max_length=50)),
                ('p_phno', models.IntegerField(db_column='m_iph')),
                ('p_img', models.ImageField(db_column='m_pic', upload_to='Members/')),
                ('p_user_name', models.CharField(db_column='m_uname', max_length=20)),
                ('p_passwd', models.CharField(db_column='m_passwd', max_length=120)),
                ('p_year', models.CharField(db_column='m_year', max_length=20)),
                ('p_status', models.CharField(db_column='m_status', max_length=20)),
            ],
            options={
                'db_table': 'tb_pachayathMember',
            },
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('user_id', models.AutoField(db_column='u_id', primary_key=True, serialize=False)),
                ('user_name', models.CharField(db_column='u_name', max_length=100)),
                ('user_gender', models.CharField(db_column='u_gender', max_length=10)),
                ('user_dob', models.CharField(db_column='u_dob', max_length=30)),
                ('user_address', models.CharField(db_column='u_addr', max_length=200)),
                ('user_email', models.CharField(db_column='u_mail', max_length=50)),
                ('user_house_no', models.IntegerField(db_column='u_house_no')),
                ('user_phno', models.IntegerField(db_column='u_ph')),
                ('user_img', models.ImageField(db_column='u_pic', upload_to='Users/')),
                ('user_passwd', models.CharField(db_column='u_passwd', max_length=120)),
                ('user_status', models.CharField(db_column='u_status', max_length=20)),
                ('user_pan', models.ForeignKey(db_column='p_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.panchayathdetails')),
            ],
            options={
                'db_table': 'tb_userDetails',
            },
        ),
        migrations.CreateModel(
            name='WardDetails',
            fields=[
                ('ward_id', models.AutoField(db_column='w_id', primary_key=True, serialize=False)),
                ('ward_no', models.IntegerField(db_column='w_no')),
                ('pan_id', models.ForeignKey(db_column='p_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.panchayathdetails')),
                ('ward_member', models.ForeignKey(blank=True, db_column='w_member', null=True, on_delete=django.db.models.deletion.SET_NULL, to='WasteManagementApp.panchayathmemberdetails')),
            ],
            options={
                'db_table': 'tb_wardDetails',
            },
        ),
        migrations.CreateModel(
            name='WasteDetails',
            fields=[
                ('waste_id', models.AutoField(primary_key=True, serialize=False)),
                ('waste_type', models.CharField(max_length=40)),
                ('waste_price', models.FloatField()),
            ],
            options={
                'db_table': 'tb_wasteDetails',
            },
        ),
        migrations.CreateModel(
            name='WasteRequestDetails',
            fields=[
                ('id', models.AutoField(db_column='req_id', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='req_date')),
                ('qty', models.IntegerField(db_column='req_qty')),
                ('payment_type', models.CharField(default='', max_length=10)),
                ('card_holder', models.CharField(db_column='card_holder', default='', max_length=20)),
                ('card_type', models.CharField(default='', max_length=10)),
                ('card_no', models.IntegerField(default=0)),
                ('card_expiry', models.CharField(default='', max_length=30)),
                ('total_price', models.FloatField(db_column='req_total')),
                ('status', models.CharField(db_column='req_status', max_length=20)),
                ('delay_status', models.CharField(db_column='delay', max_length=20)),
                ('bin_id', models.ForeignKey(db_column='wst_bin', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.bindetails')),
                ('driver_id', models.ForeignKey(blank=True, db_column='drv_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.driverdetails')),
                ('user_id', models.ForeignKey(db_column='usr_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.userdetails')),
                ('ward_id', models.ForeignKey(db_column='wrd_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.warddetails')),
                ('waste_id', models.ForeignKey(db_column='wst_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.wastedetails')),
            ],
            options={
                'db_table': 'tb_waste_request',
            },
        ),
        migrations.AddField(
            model_name='userdetails',
            name='user_ward',
            field=models.ForeignKey(db_column='w_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.warddetails'),
        ),
        migrations.CreateModel(
            name='TempryRequest',
            fields=[
                ('id', models.AutoField(db_column='tmp_id', primary_key=True, serialize=False)),
                ('date', models.DateField(db_column='req_date')),
                ('status', models.CharField(db_column='req_status', default='', max_length=20)),
                ('driver_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='WasteManagementApp.driverdetails')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.panchayathmemberdetails')),
                ('user_id', models.ForeignKey(db_column='usr_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.userdetails')),
            ],
            options={
                'db_table': 'tb_temp_request',
            },
        ),
        migrations.CreateModel(
            name='MemberSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_sign', models.ImageField(db_column='m_sign', upload_to='Sign/')),
                ('member_id', models.ForeignKey(db_column='m_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.panchayathmemberdetails')),
            ],
            options={
                'db_table': 'tb_sign',
            },
        ),
        migrations.AddField(
            model_name='driverdetails',
            name='driver_ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.warddetails'),
        ),
        migrations.CreateModel(
            name='ComplaintDetails',
            fields=[
                ('id', models.AutoField(db_column='cmp_id', primary_key=True, serialize=False)),
                ('user_complaint', models.CharField(db_column='usr_complaint', max_length=200)),
                ('complaint_date', models.DateField(db_column='complaint_date')),
                ('admin_reply', models.CharField(db_column='reply', max_length=200)),
                ('user_id', models.ForeignKey(db_column='u_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.userdetails')),
            ],
            options={
                'db_table': 'tb_complaint',
            },
        ),
        migrations.AddField(
            model_name='bindetails',
            name='pan_id',
            field=models.ForeignKey(db_column='pan_id', on_delete=django.db.models.deletion.CASCADE, to='WasteManagementApp.panchayathdetails'),
        ),
    ]
