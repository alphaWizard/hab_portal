from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime
import calendar

HOSTEL_CHOICES = (
        ('Barak', 'Barak'),
        ('Bramhaputra', 'Bramhaputra'),
        ('Dhansiri', 'Dhansiri'),
        ('Dibang', 'Dibang'),
        ('Dihing', 'Dihing'),
        ('Kameng', 'Kameng'),
        ('Kapili', 'Kapili'),
        ('Lohit', 'Lohit'),
        ('Manas', 'Manas'),
        ('Siang', 'Siang'),
        ('Subansiri', 'Subansiri'),
        ('Umiam', 'Umiam'),
    )
ID_CHOICES =(
    ('Rollno','Rollno'),
    ('ProjectId','ProjectId'),
    ('IITG_Employee Id','IITG_Employee Id'),
    ('GovtId_VoterCard','GovtId_VoterCard'),
    ('GovtId_PANCard','GovtId PANCard'),
    ('GovtID_AadharCard','GovtID_AadharCard'),
    ('GovtID_PassportNo','GovtID_PassportNo')
)

GENDER_CHOICES =(
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
)
STATUS_CHOICES =(
    ('Pending','Pending'),
    ('Approved','Approved'),
    ('Disapproved','Disapproved'),
)
TOAPPROVEDBY_CHOICES =(
    ('hodcse','hodcse'),
    ('HOSAA','HOSAA'),
    ('chr_hab','chr_hab'),
)
MESS_CHOICES =(
    ('Subscribed','Subscribed'),
    ('Unsubscribed','Unsubscribed'),
    ('PayAndEat','PayAndEat'),
)
PURPOSE_CHOICES =(
    ('Intern','Intern'),
    ('Project','Project'),
    ('Unofficial','Unofficial'),
)
ROOM_STATUS_CHOICES =(
    ('Usable','Usable'),
    ('Abandoned','Abandoned'),
    ('Partially Damaged','Partially Damaged'),
)
FLOOR_CHOICES =(
    ('Ground Floor','Ground Floor'),
    ('First Floor','First Floor'),
    ('Second Floor','Second Floor'),
    ('Third Floor','Third Floor'),
    ('Fourth Floor','Fourth Floor'),
)
ABILITY_CHOICES =(
    ('Specially/Differently Abled','Specially/Differently Abled'),
    ('No','No'),
)

#table with general information regarding all hostels

class AllHostelMetaData(models.Model):

    class Meta:
        verbose_name = "AllHostelMetaData"
        verbose_name_plural = "AllHostelMetaData"

    hostelName = models.CharField(max_length=255,primary_key=True,choices = HOSTEL_CHOICES)
    hostelCode = models.CharField(max_length=255,unique=True)
    #gensec webmail id
    hostelGensec = models.CharField(max_length=255,null=False)
    #caretaker office id
    hostelCTid = models.CharField(max_length=255,unique=True)
    #hostel rooms table name
    hostelRoom = models.CharField(max_length=255,unique=True)
    #room occupant relation table name
    hostelRoomOccupant = models.CharField(max_length=255,unique=True)
    #view permission table name
    hostelViewPermission = models.CharField(max_length=255,null=False)

    def __str__(self):
        return self.hostelName

#table with different room categories and its abbrevations used

class RoomCategory(models.Model):
    class Meta:
        verbose_name = "RoomCategory"
        verbose_name_plural = "RoomCategory"

    roomId = models.IntegerField(null=False)
    abbrevation = models.CharField(max_length=255,primary_key=True)
    #description such as single occupancy/double occupancy/attached toilets etc
    description = models.CharField(max_length=255,null=False)
    def __str__(self):
        return str(self.description)
#table with different occupant categories and its abbrevations used

class OccupantCategory(models.Model):
    class Meta:
        verbose_name = "OccupantCategory"
        verbose_name_plural = "OccupantCategory"
    occupantId = models.IntegerField(null=False)
    abbrevation = models.CharField(max_length=255,primary_key=True)
    #description - student/project staff etc
    description = models.CharField(max_length=255,null=False)
    def __str__(self):
        return self.description
#table with details of rooms in hostels .one for each hostel

class HostelRoom(models.Model):
    class Meta:
        verbose_name = "HostelRoom"
        verbose_name_plural = "HostelRoom"
    roomNo = models.CharField(max_length=255,primary_key=True)
    #occupancy as singlee/double etc
    roomOccupancyType = models.ForeignKey(RoomCategory)
    #floor as 1st/2nd etc
    floorInfo = models.CharField(max_length=255,choices = FLOOR_CHOICES)
    #status as abandoned/partially damaged etc
    roomStatus = models.CharField(max_length=255,choices=ROOM_STATUS_CHOICES)
    roomOccupancyGender = models.CharField(max_length=255,choices=GENDER_CHOICES,blank=True,null=True)
    special_category = models.IntegerField(default=0)
    comments = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return str(self.roomNo)

#table with information regarding occupants staying in hostel.one for each hostel

class HostelRoomOccupantRelation(models.Model):
    class Meta:
        verbose_name = "HostelRoomOccupantRelation"
        verbose_name_plural = "HostelRoomOccupantRelation"
    hostelName = models.CharField(max_length=255,null = False,blank= False,choices = HOSTEL_CHOICES)
    roomNo = models.CharField(max_length=255,null = False,blank= False,default="")
    occupantId = models.CharField(max_length=255,null = False,blank= False,default="")
    #mess subscription status
    messStatus = models.CharField(max_length=255 ,choices = MESS_CHOICES,null = True,blank= True)
    #toMess - end date of mess subscription
    toMess = models.DateField(null = True,blank= True)
    #fromMess - start date of mess subscription
    fromMess = models.DateField(null = True,blank= True)
    #toRoomStay - end date of room stay
    toRoomStay = models.DateField(null = True,blank= True)
    #fromRoomStay - start date of room stay
    fromRoomStay = models.DateField(null = True,blank= True)
    comment = models.CharField(max_length=255,null = True,blank= True)

    def __str__(self):
        return str(self.occupantId)
#table with name and webmail of the people with access permissions(view only).one for each hostel

class HostelViewAccess(models.Model):
    class Meta:
        verbose_name = "HostelViewAccess"
        verbose_name_plural = "HostelViewAccess"
    name = models.CharField(max_length=255,null=False)
    webmail = models.CharField(max_length=255,primary_key=True)

    def __str__(self):
        return self.webmail

#table with all information of a particular OccupantDetails

class OccupantDetails(models.Model):
    # def validate_image(fieldfile_obj):
    #     filesize = fieldfile_obj.file.size
    #     megabyte_limit = 0.5
    #     if filesize > megabyte_limit*1024*1024:
    #         raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
    class Meta:
        verbose_name = "OccupantDetails"
        verbose_name_plural = "OccupantDetails"
    name = models.CharField(max_length=255,null = False,blank= False,default="")
    #id type - roll no/aadhar no/project id etc
    idType = models.CharField(max_length=255,choices = ID_CHOICES,null = False,blank= False,default="Rollno")
    #rollno/aadhar no etc
    #primary_key removed temp
    idNo = models.CharField(max_length=255,primary_key=True,null=False,blank=False,default="")
#vgv
    gender = models.CharField(max_length=255,choices = GENDER_CHOICES,null = False,blank= False,default="Male")
    #specially abled/differently abled
    saORda = models.CharField(max_length=255,choices = ABILITY_CHOICES,null = False,blank= False,default="No")
    webmail = models.CharField(max_length=255,null = True,blank= True)
    altEmail = models.EmailField(max_length=255,null = False,blank= False,default="abc@xyz.com")
    mobNo = models.CharField(max_length=12,null = False,blank= False,default="")
    emgercencyNo = models.CharField(max_length=12,null = False,blank= False,default="")
    photo = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    idPhoto = models.ImageField(upload_to='id_pics',blank=True,null=True)
    Address=models.CharField(max_length=300,null = False,blank= False,default="")
    Pincode=models.PositiveIntegerField( validators=[MaxValueValidator(999999)],null = False,blank= False,default="0")
    bankName = models.CharField(max_length=255,null = True,blank= True)
    bankAccount = models.CharField(max_length=255,null = True,blank= True)
    IFSCCode = models.CharField(max_length=255,null = True,blank= True)
    #account holder name
    accHolderName = models.CharField(max_length=255,null = True,blank= True)
    flag = models.IntegerField(default=0)
    def __str__(self):
        return str(self.name)
#following are the hostelRoom,roomOccupantRelation and view access tables for each hostel(13*3=39 tables)
#hostelRoom inherits HostelRoom
#hostelView inherits HostelViewAccess
#hostelRORelation inherits HostelRoomOccupantRelation

class TemporaryDetails(models.Model):
    # def validate_image(fieldfile_obj):
    #     filesize = fieldfile_obj.file.size
    #     megabyte_limit = 0.5
    #     if filesize > megabyte_limit*1024*1024:
    #         raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
    class Meta:
        verbose_name = "TemporaryDetails"
        verbose_name_plural = "TemporaryDetails"
    name = models.CharField(max_length=255,null = False,blank= False,default="")
    #id type - roll no/aadhar no/project id etc
    idType = models.CharField(max_length=255,choices = ID_CHOICES,null = False,blank= False,default="Rollno")
    #rollno/aadhar no etc
    #primary_key removed temp
    idNo = models.CharField(max_length=255,null=False,blank=False,default="")
#vgv
    gender = models.CharField(max_length=255,choices = GENDER_CHOICES,null = False,blank= False,default="Male")
    #specially abled/differently abled
    saORda = models.CharField(max_length=255,choices = ABILITY_CHOICES,null = False,blank= False,default="No")
    webmail = models.CharField(max_length=255,null = True,blank= True)
    altEmail = models.CharField(max_length=255,null = False,blank= False,default="abc@xyz.com")
    mobNo = models.CharField(max_length=12,null = False,blank= False,default="")
    emgercencyNo = models.CharField(max_length=12,null = False,blank= False,default="")
    photo = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    idPhoto = models.ImageField(upload_to='id_pics',blank=True,null=True)
    Address=models.CharField(max_length=300,null = False,blank= False,default="")
    Pincode=models.PositiveIntegerField( validators=[MaxValueValidator(999999)],null = False,blank= False,default="0")
    bankName = models.CharField(max_length=255,null = True,blank= True)
    bankAccount = models.CharField(max_length=255,null = True,blank= True)
    IFSCCode = models.CharField(max_length=255,null = True,blank= True)
    #account holder name
    accHolderName = models.CharField(max_length=255,null = True,blank= True)
    ct_approval = models.CharField(max_length=255,choices = STATUS_CHOICES,default = "Pending")
    comments = models.CharField(max_length=255,null = True,blank= True)
    flag = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.name)

class UpcomingOccupantRequest(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 0.5
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))
    # hostelName = models.CharField(max_length=255,choices = HOSTEL_CHOICES)
    guestname=models.CharField(max_length=255,null = False)
    hostelName = models.CharField(max_length = 255,choices = HOSTEL_CHOICES)
    id_type=models.CharField(max_length=255,choices = ID_CHOICES)
    id_no=models.CharField(max_length=20,null=False)
    Gender=models.CharField(max_length=255,choices = GENDER_CHOICES)
    saORda = models.CharField(max_length=255,choices = ABILITY_CHOICES,default="No")
    Address=models.CharField(max_length=300,null=False)
    Pincode=models.PositiveIntegerField(null=False, validators=[MaxValueValidator(999999)])
    Mobile_No=models.PositiveIntegerField(null=False, validators=[MaxValueValidator(9999999999)])
    Emergency_Mobile_No=models.PositiveIntegerField(null=False, validators=[MaxValueValidator(9999999999)])
    Webmail_id=models.CharField(max_length=255,null=True,blank=True)
    Alternate_email_id=models.EmailField(null=False)
    Bank_Name=models.CharField(max_length=255,null=True,blank=True)
    Account_Holder_Name =models.CharField(max_length=255,null=True,blank=True)
    Bank_Account_No=models.IntegerField(null=True,blank=True)
    IFSCCode = models.CharField(max_length=255,null=True,blank=True)
    From_Date=models.DateField()
    To_Date=models.DateField()
    Purpose_Of_Stay=models.CharField(max_length=255,choices = PURPOSE_CHOICES,null=True,blank=True)
    Preference_Room=models.ForeignKey(RoomCategory,null=True,blank=True)
    photo = models.ImageField(upload_to='profile_pics',blank=True,validators=[validate_image],null=True)
    idPhoto = models.ImageField(upload_to='id_pics',blank=True,validators=[validate_image],null=True)
    #
    #prefernce??
    Host_Name=models.CharField(max_length=255,null=False)
    Host_Webmail_Id=models.CharField(max_length=255)
    Host_Id=models.CharField(max_length=255,null=False)
    # To_be_approved_by=models.CharField(max_length=255,choices = TOAPPROVEDBY_CHOICES)
    #approved by hod,hosaa etc
    # isApprovedFirst = models.CharField(max_length=255,choices = STATUS_CHOICES,default = "Pending")
    #is aproved by chr_hab
    isApprovedChr = models.CharField(max_length=255,choices = STATUS_CHOICES,default = "Pending")
    comments = models.CharField(max_length=255,null=True,blank=True)
    class Meta:
        verbose_name = "allotment"
        verbose_name_plural = "allotment"
        # unique_together = ('Mobile_No', 'Emergency_Mobile_No',)
    def __str__(self):
        return self.guestname

class UpcomingOccupant(models.Model):
    class Meta:
        verbose_name = "UpcomingOccupant"
        verbose_name_plural = "UpcomingOccupant"
    occupantName = models.CharField(max_length=255)
    idType = models.CharField(max_length=255,choices = ID_CHOICES)
    occupantId = models.CharField(max_length=255)
    hostelName = models.CharField(max_length=255,choices = HOSTEL_CHOICES)
    roomNo = models.CharField(max_length=255,blank=True,null=True)
    fromStay = models.DateField()
    toStay = models.DateField()
    comments = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        return self.occupantName


class Login(models.Model):
    name = models.CharField(max_length=255,null=False)
    webmail = models.CharField(max_length=255,null=False)
    password = models.CharField(max_length=255,null=False)
class ChrViewAccess(models.Model):
    name = models.CharField(max_length=255,null=False)
    webmail = models.CharField(max_length=255,null=False)
class Log_Table(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "Log_Table"
        verbose_name_plural = "Log_Table"
    created = models.DateTimeField(auto_now_add=True)

class Log_Table2(OccupantDetails):
    class Meta:
        verbose_name = "Log_Table2"
        verbose_name_plural = "Log_Table2"
    created = models.DateTimeField(auto_now_add=True)

class SiangRoom(HostelRoom):
    class Meta:
        verbose_name = "siangRoom"
        verbose_name_plural = "siangRoom"

class SiangView(HostelViewAccess):
    class Meta:
        verbose_name = "siangView"
        verbose_name_plural = "siangView"
class SiangRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "siangRORelation"
        verbose_name_plural = "siangRORelation"

class LohitRoom(HostelRoom):
    class Meta:
        verbose_name = "lohitRoom"
        verbose_name_plural = "lohitRoom"
class LohitView(HostelViewAccess):
    class Meta:
        verbose_name = "lohitView"
        verbose_name_plural = "lohitView"
class LohitRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "lohitRORelation"
        verbose_name_plural = "lohitRORelation"

class DihingRoom(HostelRoom):
    class Meta:
        verbose_name = "dihingRoom"
        verbose_name_plural = "dihingRoom"
class DihingView(HostelViewAccess):
    class Meta:
        verbose_name = "dihingView"
        verbose_name_plural = "dihingView"
class DihingRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "dihingRORelation"
        verbose_name_plural = "dihingRORelation"

class DibangRoom(HostelRoom):
    class Meta:
        verbose_name = "dibangRoom"
        verbose_name_plural = "dibangRoom"
class DibangView(HostelViewAccess):
    class Meta:
        verbose_name = "dibangView"
        verbose_name_plural = "dibangView"
class DibangRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "dibangRORelation"
        verbose_name_plural = "dibangRORelation"

class KapiliRoom(HostelRoom):
    class Meta:
        verbose_name = "kapiliRoom"
        verbose_name_plural = "kapiliRoom"
class KapiliView(HostelViewAccess):
    class Meta:
        verbose_name = "kapiliView"
        verbose_name_plural = "kapiliView"
class KapiliRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "kapiliRORelation"
        verbose_name_plural = "kapiliRORelation"

class ManasRoom(HostelRoom):
    class Meta:
        verbose_name = "manasRoom"
        verbose_name_plural = "manasRoom"
class ManasView(HostelViewAccess):
    class Meta:
        verbose_name = "manasView"
        verbose_name_plural = "manasView"
class ManasRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "manasRORelation"
        verbose_name_plural = "manasRORelation"

class BarakRoom(HostelRoom):
    class Meta:
        verbose_name = "barakRoom"
        verbose_name_plural = "barakRoom"
class BarakView(HostelViewAccess):
    class Meta:
        verbose_name = "barakView"
        verbose_name_plural = "barakView"
class BarakRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "barakRORelation"
        verbose_name_plural = "barakRORelation"

class UmiamRoom(HostelRoom):
    class Meta:
        verbose_name = "umiamRoom"
        verbose_name_plural = "umiamRoom"
class UmiamView(HostelViewAccess):
    class Meta:
        verbose_name = "umiamView"
        verbose_name_plural = "umiamView"
class UmiamRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "umiamRORelation"
        verbose_name_plural = "umiamRORelation"

class BramhaputraRoom(HostelRoom):
    class Meta:
        verbose_name = "bramhaputraRoom"
        verbose_name_plural = "bramhaputraRoom"
class BramhaputraView(HostelViewAccess):
    class Meta:
        verbose_name = "bramhaputraView"
        verbose_name_plural = "bramhaputraView"
class BramhaputraRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "bramhaputraRORelation"
        verbose_name_plural = "bramhaputraRORelation"

class DhansiriRoom(HostelRoom):
    class Meta:
        verbose_name = "dhansiriRoom"
        verbose_name_plural = "dhansiriRoom"
class DhansiriView(HostelViewAccess):
    class Meta:
        verbose_name = "dhansiriView"
        verbose_name_plural = "dhansiriView"
class DhansiriRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "dhansiriRORelation"
        verbose_name_plural = "dhansiriRORelation"

class SubansiriRoom(HostelRoom):
    class Meta:
        verbose_name = "subansiriRoom"
        verbose_name_plural = "subansiriRoom"
class SubansiriView(HostelViewAccess):
    class Meta:
        verbose_name = "subansiriView"
        verbose_name_plural = "subansiriView"

class SubansiriRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "subansiriRORelation"
        verbose_name_plural = "subansiriRORelation"

class KamengRoom(HostelRoom):
    class Meta:
        verbose_name = "kamengRoom"
        verbose_name_plural = "kamengRoom"
class KamengView(HostelViewAccess):
    class Meta:
        verbose_name = "kamengView"
        verbose_name_plural = "kamengView"
class KamengRORelation(HostelRoomOccupantRelation):
    class Meta:
        verbose_name = "kamengRORelation"
        verbose_name_plural = "kamengRORelation"

# MESS automation
# default=m2  default=y2
MONTHS_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
YEARS_CHOICES = [(i,i) for i in range(2010,datetime.now().year+1)]
curr_month = datetime.now().month
curr_year = datetime.now().year
m1 = curr_month
y1 = curr_year
m1 = m1 - 1
m1_y1 = ""
if m1 < 1:
    m1 = 12
    y1 = y1 - 1
# MESS automation
# default=m2  default=y2
class Automation(models.Model):
    class Meta:
        verbose_name = "Automation"
        verbose_name_plural = "Automation"
        unique_together = ('month','year')

    month = models.CharField(max_length=9, choices=MONTHS_CHOICES)
    year = models.IntegerField(choices = YEARS_CHOICES)

    feed_on_off = models.BooleanField()
    feed_start_date = models.DateField(null=True,blank=True)
    feed_off_date = models.DateField(null=True,blank=True)

    pref_on_off = models.BooleanField()
    pref_start_date = models.DateField(null=True,blank=True)
    pref_off_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return '%s_%s' % (self.month, self.year)

# MESS model for csv files import and export


class ImportExportFiles(models.Model):
    hostelName = models.CharField(max_length=255,choices = HOSTEL_CHOICES)
    month = models.CharField(max_length=9, choices=MONTHS_CHOICES)
    year = models.IntegerField(choices = YEARS_CHOICES)
