# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-30 05:54
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hab_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllHostelMetaData',
            fields=[
                ('hostelName', models.CharField(choices=[('Barak', 'Barak'), ('Bramhaputra', 'Bramhaputra'), ('Dhansiri', 'Dhansiri'), ('Dibang', 'Dibang'), ('Dihing', 'Dihing'), ('Kameng', 'Kameng'), ('Kapili', 'Kapili'), ('Lohit', 'Lohit'), ('Manas', 'Manas'), ('Siang', 'Siang'), ('Subansiri', 'Subansiri'), ('Umiam', 'Umiam')], max_length=255, primary_key=True, serialize=False)),
                ('hostelCode', models.CharField(max_length=255, unique=True)),
                ('hostelGensec', models.CharField(max_length=255)),
                ('hostelCTid', models.CharField(max_length=255, unique=True)),
                ('hostelRoom', models.CharField(max_length=255, unique=True)),
                ('hostelRoomOccupant', models.CharField(max_length=255, unique=True)),
                ('hostelViewPermission', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'AllHostelMetaData',
                'verbose_name_plural': 'AllHostelMetaData',
            },
        ),
        migrations.CreateModel(
            name='Automation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=9)),
                ('year', models.IntegerField(choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)])),
                ('feed_on_off', models.BooleanField()),
                ('feed_start_date', models.DateField(blank=True, null=True)),
                ('feed_off_date', models.DateField(blank=True, null=True)),
                ('pref_on_off', models.BooleanField()),
                ('pref_start_date', models.DateField(blank=True, null=True)),
                ('pref_off_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Automation',
                'verbose_name_plural': 'Automation',
            },
        ),
        migrations.CreateModel(
            name='ChrViewAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('webmail', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='HostelRoom',
            fields=[
                ('roomNo', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('floorInfo', models.CharField(choices=[('Ground Floor', 'Ground Floor'), ('First Floor', 'First Floor'), ('Second Floor', 'Second Floor'), ('Third Floor', 'Third Floor'), ('Fourth Floor', 'Fourth Floor')], max_length=255)),
                ('roomStatus', models.CharField(choices=[('Usable', 'Usable'), ('Abandoned', 'Abandoned'), ('Partially Damaged', 'Partially Damaged')], max_length=255)),
                ('roomOccupancyGender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=255, null=True)),
                ('special_category', models.IntegerField(default=0)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'HostelRoom',
                'verbose_name_plural': 'HostelRoom',
            },
        ),
        migrations.CreateModel(
            name='HostelRoomOccupantRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostelName', models.CharField(choices=[('Barak', 'Barak'), ('Bramhaputra', 'Bramhaputra'), ('Dhansiri', 'Dhansiri'), ('Dibang', 'Dibang'), ('Dihing', 'Dihing'), ('Kameng', 'Kameng'), ('Kapili', 'Kapili'), ('Lohit', 'Lohit'), ('Manas', 'Manas'), ('Siang', 'Siang'), ('Subansiri', 'Subansiri'), ('Umiam', 'Umiam')], max_length=255)),
                ('roomNo', models.CharField(default='', max_length=255)),
                ('occupantId', models.CharField(default='', max_length=255)),
                ('messStatus', models.CharField(blank=True, choices=[('Subscribed', 'Subscribed'), ('Unsubscribed', 'Unsubscribed'), ('PayAndEat', 'PayAndEat')], max_length=255, null=True)),
                ('toMess', models.DateField(blank=True, null=True)),
                ('fromMess', models.DateField(blank=True, null=True)),
                ('toRoomStay', models.DateField(blank=True, null=True)),
                ('fromRoomStay', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'HostelRoomOccupantRelation',
                'verbose_name_plural': 'HostelRoomOccupantRelation',
            },
        ),
        migrations.CreateModel(
            name='HostelViewAccess',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('webmail', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'HostelViewAccess',
                'verbose_name_plural': 'HostelViewAccess',
            },
        ),
        migrations.CreateModel(
            name='ImportExportFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostelName', models.CharField(choices=[('Barak', 'Barak'), ('Bramhaputra', 'Bramhaputra'), ('Dhansiri', 'Dhansiri'), ('Dibang', 'Dibang'), ('Dihing', 'Dihing'), ('Kameng', 'Kameng'), ('Kapili', 'Kapili'), ('Lohit', 'Lohit'), ('Manas', 'Manas'), ('Siang', 'Siang'), ('Subansiri', 'Subansiri'), ('Umiam', 'Umiam')], max_length=255)),
                ('month', models.CharField(choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=9)),
                ('year', models.IntegerField(choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)])),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('webmail', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OccupantCategory',
            fields=[
                ('occupantId', models.IntegerField()),
                ('abbrevation', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'OccupantCategory',
                'verbose_name_plural': 'OccupantCategory',
            },
        ),
        migrations.CreateModel(
            name='OccupantDetails',
            fields=[
                ('name', models.CharField(default='', max_length=255)),
                ('idType', models.CharField(choices=[('Rollno', 'Rollno'), ('Project Id', 'Project Id'), ('IITG Employee Id', 'IITG Employee Id'), ('GovtId_VoterCard', 'GovtId_VoterCard'), ('PAN Card', 'PAN Card'), ('GovtID_AadharCard', 'GovtID_AadharCard'), ('GovtIDPassportNo', 'GovtIDPassportNo')], default='Rollno', max_length=255)),
                ('idNo', models.CharField(default='', max_length=255, primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=255)),
                ('saORda', models.CharField(choices=[('Specially/Differently Abled', 'Specially/Differently Abled'), ('No', 'No')], default='No', max_length=255)),
                ('webmail', models.CharField(blank=True, max_length=255, null=True)),
                ('altEmail', models.EmailField(default='abc@xyz.com', max_length=255)),
                ('mobNo', models.CharField(default='', max_length=12)),
                ('emgercencyNo', models.CharField(default='', max_length=12)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_pics')),
                ('idPhoto', models.ImageField(blank=True, null=True, upload_to='id_pics')),
                ('Address', models.CharField(default='', max_length=300)),
                ('Pincode', models.PositiveIntegerField(default='0', validators=[django.core.validators.MaxValueValidator(999999)])),
                ('bankName', models.CharField(blank=True, max_length=255, null=True)),
                ('bankAccount', models.CharField(blank=True, max_length=255, null=True)),
                ('IFSCCode', models.CharField(blank=True, max_length=255, null=True)),
                ('accHolderName', models.CharField(blank=True, max_length=255, null=True)),
                ('flag', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'OccupantDetails',
                'verbose_name_plural': 'OccupantDetails',
            },
        ),
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('roomId', models.IntegerField()),
                ('abbrevation', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'RoomCategory',
                'verbose_name_plural': 'RoomCategory',
            },
        ),
        migrations.CreateModel(
            name='TemporaryDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('idType', models.CharField(choices=[('Rollno', 'Rollno'), ('Project Id', 'Project Id'), ('IITG Employee Id', 'IITG Employee Id'), ('GovtId_VoterCard', 'GovtId_VoterCard'), ('PAN Card', 'PAN Card'), ('GovtID_AadharCard', 'GovtID_AadharCard'), ('GovtIDPassportNo', 'GovtIDPassportNo')], default='Rollno', max_length=255)),
                ('idNo', models.CharField(default='', max_length=255)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=255)),
                ('saORda', models.CharField(choices=[('Specially/Differently Abled', 'Specially/Differently Abled'), ('No', 'No')], default='No', max_length=255)),
                ('webmail', models.CharField(blank=True, max_length=255, null=True)),
                ('altEmail', models.CharField(default='abc@xyz.com', max_length=255)),
                ('mobNo', models.CharField(default='', max_length=12)),
                ('emgercencyNo', models.CharField(default='', max_length=12)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_pics')),
                ('idPhoto', models.ImageField(blank=True, null=True, upload_to='id_pics')),
                ('Address', models.CharField(default='', max_length=300)),
                ('Pincode', models.PositiveIntegerField(default='0', validators=[django.core.validators.MaxValueValidator(999999)])),
                ('bankName', models.CharField(blank=True, max_length=255, null=True)),
                ('bankAccount', models.CharField(blank=True, max_length=255, null=True)),
                ('IFSCCode', models.CharField(blank=True, max_length=255, null=True)),
                ('accHolderName', models.CharField(blank=True, max_length=255, null=True)),
                ('ct_approval', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved')], default='Pending', max_length=255)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('flag', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'TemporaryDetails',
                'verbose_name_plural': 'TemporaryDetails',
            },
        ),
        migrations.CreateModel(
            name='UpcomingOccupant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupantName', models.CharField(max_length=255)),
                ('idType', models.CharField(choices=[('Rollno', 'Rollno'), ('Project Id', 'Project Id'), ('IITG Employee Id', 'IITG Employee Id'), ('GovtId_VoterCard', 'GovtId_VoterCard'), ('PAN Card', 'PAN Card'), ('GovtID_AadharCard', 'GovtID_AadharCard'), ('GovtIDPassportNo', 'GovtIDPassportNo')], max_length=255)),
                ('occupantId', models.CharField(max_length=255)),
                ('hostelName', models.CharField(choices=[('Barak', 'Barak'), ('Bramhaputra', 'Bramhaputra'), ('Dhansiri', 'Dhansiri'), ('Dibang', 'Dibang'), ('Dihing', 'Dihing'), ('Kameng', 'Kameng'), ('Kapili', 'Kapili'), ('Lohit', 'Lohit'), ('Manas', 'Manas'), ('Siang', 'Siang'), ('Subansiri', 'Subansiri'), ('Umiam', 'Umiam')], max_length=255)),
                ('roomNo', models.CharField(blank=True, max_length=255, null=True)),
                ('fromStay', models.DateField()),
                ('toStay', models.DateField()),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'UpcomingOccupant',
                'verbose_name_plural': 'UpcomingOccupant',
            },
        ),
        migrations.CreateModel(
            name='UpcomingOccupantRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guestname', models.CharField(max_length=255)),
                ('hostelName', models.CharField(choices=[('Barak', 'Barak'), ('Bramhaputra', 'Bramhaputra'), ('Dhansiri', 'Dhansiri'), ('Dibang', 'Dibang'), ('Dihing', 'Dihing'), ('Kameng', 'Kameng'), ('Kapili', 'Kapili'), ('Lohit', 'Lohit'), ('Manas', 'Manas'), ('Siang', 'Siang'), ('Subansiri', 'Subansiri'), ('Umiam', 'Umiam')], max_length=255)),
                ('id_type', models.CharField(choices=[('Rollno', 'Rollno'), ('Project Id', 'Project Id'), ('IITG Employee Id', 'IITG Employee Id'), ('GovtId_VoterCard', 'GovtId_VoterCard'), ('PAN Card', 'PAN Card'), ('GovtID_AadharCard', 'GovtID_AadharCard'), ('GovtIDPassportNo', 'GovtIDPassportNo')], max_length=255)),
                ('id_no', models.CharField(max_length=20)),
                ('Gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=255)),
                ('saORda', models.CharField(choices=[('Specially/Differently Abled', 'Specially/Differently Abled'), ('No', 'No')], default='No', max_length=255)),
                ('Address', models.CharField(max_length=300)),
                ('Pincode', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999)])),
                ('Mobile_No', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('Emergency_Mobile_No', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('Webmail_id', models.CharField(blank=True, max_length=255, null=True)),
                ('Alternate_email_id', models.EmailField(max_length=254)),
                ('Bank_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('Account_Holder_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('Bank_Account_No', models.IntegerField(blank=True, null=True)),
                ('IFSCCode', models.CharField(blank=True, max_length=255, null=True)),
                ('From_Date', models.DateField()),
                ('To_Date', models.DateField()),
                ('Purpose_Of_Stay', models.CharField(blank=True, choices=[('Intern', 'Intern'), ('Project', 'Project'), ('Unofficial', 'Unofficial')], max_length=255, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_pics', validators=[hab_app.models.UpcomingOccupantRequest.validate_image])),
                ('idPhoto', models.ImageField(blank=True, null=True, upload_to='id_pics', validators=[hab_app.models.UpcomingOccupantRequest.validate_image])),
                ('Host_Name', models.CharField(max_length=255)),
                ('Host_Webmail_Id', models.CharField(max_length=255)),
                ('Host_Id', models.CharField(max_length=255)),
                ('isApprovedChr', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved')], default='Pending', max_length=255)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('Preference_Room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hab_app.RoomCategory')),
            ],
            options={
                'verbose_name': 'allotment',
                'verbose_name_plural': 'allotment',
            },
        ),
        migrations.CreateModel(
            name='BarakRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'barakRoom',
                'verbose_name_plural': 'barakRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='BarakRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'barakRORelation',
                'verbose_name_plural': 'barakRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='BarakView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'barakView',
                'verbose_name_plural': 'barakView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='BramhaputraRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'bramhaputraRoom',
                'verbose_name_plural': 'bramhaputraRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='BramhaputraRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'bramhaputraRORelation',
                'verbose_name_plural': 'bramhaputraRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='BramhaputraView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'bramhaputraView',
                'verbose_name_plural': 'bramhaputraView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='DhansiriRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'dhansiriRoom',
                'verbose_name_plural': 'dhansiriRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='DhansiriRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'dhansiriRORelation',
                'verbose_name_plural': 'dhansiriRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='DhansiriView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'dhansiriView',
                'verbose_name_plural': 'dhansiriView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='DibangRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'dibangRoom',
                'verbose_name_plural': 'dibangRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='DibangRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'dibangRORelation',
                'verbose_name_plural': 'dibangRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='DibangView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'dibangView',
                'verbose_name_plural': 'dibangView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='DihingRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'dihingRoom',
                'verbose_name_plural': 'dihingRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='DihingRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'dihingRORelation',
                'verbose_name_plural': 'dihingRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='DihingView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'dihingView',
                'verbose_name_plural': 'dihingView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='KamengRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'kamengRoom',
                'verbose_name_plural': 'kamengRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='KamengRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'kamengRORelation',
                'verbose_name_plural': 'kamengRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='KamengView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'kamengView',
                'verbose_name_plural': 'kamengView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='KapiliRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'kapiliRoom',
                'verbose_name_plural': 'kapiliRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='KapiliRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'kapiliRORelation',
                'verbose_name_plural': 'kapiliRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='KapiliView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'kapiliView',
                'verbose_name_plural': 'kapiliView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='Log_Table',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Log_Table',
                'verbose_name_plural': 'Log_Table',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='Log_Table2',
            fields=[
                ('occupantdetails_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.OccupantDetails')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Log_Table2',
                'verbose_name_plural': 'Log_Table2',
            },
            bases=('hab_app.occupantdetails',),
        ),
        migrations.CreateModel(
            name='LohitRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'lohitRoom',
                'verbose_name_plural': 'lohitRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='LohitRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'lohitRORelation',
                'verbose_name_plural': 'lohitRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='LohitView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'lohitView',
                'verbose_name_plural': 'lohitView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='ManasRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'manasRoom',
                'verbose_name_plural': 'manasRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='ManasRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'manasRORelation',
                'verbose_name_plural': 'manasRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='ManasView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'manasView',
                'verbose_name_plural': 'manasView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='SiangRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'siangRoom',
                'verbose_name_plural': 'siangRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='SiangRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'siangRORelation',
                'verbose_name_plural': 'siangRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='SiangView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'siangView',
                'verbose_name_plural': 'siangView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='SubansiriRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'subansiriRoom',
                'verbose_name_plural': 'subansiriRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='SubansiriRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'subansiriRORelation',
                'verbose_name_plural': 'subansiriRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='SubansiriView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'subansiriView',
                'verbose_name_plural': 'subansiriView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.CreateModel(
            name='UmiamRoom',
            fields=[
                ('hostelroom_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoom')),
            ],
            options={
                'verbose_name': 'umiamRoom',
                'verbose_name_plural': 'umiamRoom',
            },
            bases=('hab_app.hostelroom',),
        ),
        migrations.CreateModel(
            name='UmiamRORelation',
            fields=[
                ('hostelroomoccupantrelation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelRoomOccupantRelation')),
            ],
            options={
                'verbose_name': 'umiamRORelation',
                'verbose_name_plural': 'umiamRORelation',
            },
            bases=('hab_app.hostelroomoccupantrelation',),
        ),
        migrations.CreateModel(
            name='UmiamView',
            fields=[
                ('hostelviewaccess_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hab_app.HostelViewAccess')),
            ],
            options={
                'verbose_name': 'umiamView',
                'verbose_name_plural': 'umiamView',
            },
            bases=('hab_app.hostelviewaccess',),
        ),
        migrations.AddField(
            model_name='hostelroom',
            name='roomOccupancyType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hab_app.RoomCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='automation',
            unique_together=set([('month', 'year')]),
        ),
    ]
