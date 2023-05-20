from django.db import models

# Create your models here.

# Model for company
class Company(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for location
class Location(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for department
class Department(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for asset category
class AssetCategory(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for asset status
class AssetStatus(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name


# Model for OS version
class OperationSystem(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for office version
class OfficeVersion(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for Memory
class Memory(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for hard disk
class HardDisk(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for vendor
class Vendor(models.Model):
    name = models.CharField('Name',max_length=50)
    phone = models.CharField('Phone',max_length=20)
    address = models.CharField('Address',max_length=100)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)
    def __str__(self):
        return self.name

# Model for user
class User(models.Model):
    account = models.CharField(verbose_name='Account',max_length=20,unique=True)
    name = models.CharField(verbose_name='User Name',max_length=100)
    company = models.CharField(verbose_name='Company',max_length=20)
    department = models.CharField(verbose_name='Department',max_length=20)
    is_active = models.BooleanField(verbose_name='Status',default=1)
    location = models.CharField(verbose_name='Location',max_length=20)
    comment = models.TextField(verbose_name='Comment',null=True,blank=True)
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
    create_by = models.CharField(verbose_name='Create By',max_length=20,default='')
    def __str__(self):
        return self.name

# Model for asset
class Asset(models.Model):
    company = models.CharField(verbose_name='Company',max_length=20)
    category = models.CharField(verbose_name='Category',max_length=20)
    model = models.CharField(verbose_name='Model',max_length=50)
    sn = models.CharField(verbose_name='Serial Number',max_length=20,unique=True)
    name = models.CharField(verbose_name='Asset Name',max_length=20)
    price = models.DecimalField(verbose_name='Price',max_digits=10,decimal_places=2)
    comment = models.TextField(verbose_name='Comment',null=True,blank=True)   
    purchase_date = models.DateField('Purchase Date',default='')
    warranty = models.SmallIntegerField(verbose_name='Warranty')
    user = models.ForeignKey(verbose_name='User',to=User,on_delete=models.SET_NULL,null=True)    
    initial_os = models.CharField(verbose_name='Initial OS',max_length=50,null=True,blank=True)
    os = models.CharField(verbose_name='OS',max_length=50,null=True,blank=True)
    office = models.CharField(verbose_name='Office',max_length=50,null=True,blank=True)
    cpu = models.CharField(verbose_name='CPU',max_length=50,null=True,blank=True)
    memory = models.CharField(verbose_name='Memory',max_length=20,null=True,blank=True)
    hdd = models.CharField(verbose_name='HDD',max_length=20,null=True,blank=True)
    vendor = models.CharField(verbose_name='Vendor',max_length=50,null=True,blank=True)
    status = models.ForeignKey(verbose_name='Status',to=AssetStatus,on_delete=models.SET_NULL,null=True,default=1)
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
    create_by = models.CharField(verbose_name='Create_by',max_length=20,default='')
    def __str__(self):
        return self.name
    def tanium_lastsee(self):
        # Check if exist in Tanium
        check_exist = Tanium.objects.filter(name__icontains=self.name)
        if check_exist.exists():
            return '%s'%(check_exist.first().lastsee)
        return 'Not found in Tanium'

# Model for asset history
class AssetHistory(models.Model):
    asset = models.ForeignKey(verbose_name='Asset',to=Asset,on_delete=models.CASCADE)
    operator = models.CharField(verbose_name='Operator',max_length=20)
    action = models.CharField(verbose_name='Action',max_length=20,default='None')
    comment = models.TextField(verbose_name='Comment',null=True)  
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)  

# Model for user history
class UserHistory(models.Model):
    user = models.ForeignKey(verbose_name='Asset',to=User,on_delete=models.CASCADE)
    operator = models.CharField(verbose_name='Operator',max_length=20)
    action = models.CharField(verbose_name='Action',max_length=20,default='None')
    comment = models.TextField(verbose_name='Comment',null=True,blank=True)  
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True) 

# Model for tanium
class Tanium(models.Model):
    name = models.CharField(verbose_name='Computer Name',max_length=300)
    lastsee = models.CharField(verbose_name='Last See',max_length=150,null=True,blank=True)
    os_install_date = models.CharField(verbose_name='OS Install Date',max_length=150,null=True,blank=True)
    os = models.CharField(verbose_name='OS',max_length=150,null=True,blank=True)
    username = models.CharField(verbose_name='User Name',max_length=150,null=True,blank=True)
    model = models.CharField(verbose_name='Model',max_length=150,null=True,blank=True)
    last_reboot = models.CharField(verbose_name='Last Reboot',max_length=150,null=True,blank=True)
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True) 