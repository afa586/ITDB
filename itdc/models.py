from email.policy import default
from django.db import models

# Create your models here.

# Model for location
class Location(models.Model):
    name = models.CharField('Name',max_length=50)
    comment = models.TextField('Comment')
    create_time = models.DateTimeField('Create Time',auto_now_add=True)

    def __str__(self):
        return self.name

# Model for Element(Server,Switch,Firewall,VM,Service...)
class Asset(models.Model):
    location = models.CharField(verbose_name='Location',max_length=20)
    category = models.CharField(verbose_name='Category',max_length=20)
    model = models.CharField(verbose_name='Model',max_length=50,null=True)
    sn = models.CharField(verbose_name='Serial Number',max_length=20,null=True)
    name = models.CharField(verbose_name='Name',max_length=50,unique=True)
    container = models.ForeignKey('self',on_delete=models.CASCADE,verbose_name='Container',null=True,default=None)
    os = models.CharField(verbose_name='OS',max_length=50,null=True,blank=True)
    cpu = models.CharField(verbose_name='CPU',max_length=50,null=True,blank=True)
    memory = models.CharField(verbose_name='Memory',max_length=50,null=True,blank=True)
    hdd = models.CharField(verbose_name='HDD',max_length=50,null=True,blank=True)
    price = models.DecimalField(verbose_name='Price',max_digits=10,decimal_places=2,null=True,blank=True)
    vendor = models.CharField(verbose_name='Vendor',max_length=50,null=True,blank=True)
    comment = models.TextField(verbose_name='Comment',null=True,blank=True)   
    purchase_date = models.DateField(verbose_name='Purchase Date',null=True)
    expire_date = models.DateField(verbose_name='Expire Date',null=True)
    is_active = models.BooleanField(verbose_name='Is Active',default=True,choices =((True,'Yes'),(False,'No')))  
    is_poweron = models.BooleanField(verbose_name='Is PowerOn',default=True,choices =((True,'Yes'),(False,'No')))  
    is_container = models.BooleanField(verbose_name='Is Container',default=False,choices =((True,'Yes'),(False,'No')))  
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
    create_by = models.CharField(verbose_name='Create_by',max_length=20,null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'itdc_all_asset'

# Model for asset comment
class AssetComment(models.Model):
    asset = models.ForeignKey(verbose_name='Asset',to=Asset,on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='Comment',null=True)  
    create_by = models.CharField(verbose_name='Create By',max_length=20)    
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True) 

# Model for network port
class NetworkPort(models.Model):
    asset = models.ForeignKey(verbose_name='Asset',to=Asset,on_delete=models.CASCADE)
    port_number = models.SmallIntegerField(verbose_name='Port Number')
    connect_to = models.CharField(verbose_name='Connect To',max_length=100,null=True,blank=True)
    comment = models.TextField(verbose_name='Comment',blank=True) 
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
    create_by = models.CharField(verbose_name='Create_by',max_length=20,default='') 
    def __str__(self) -> str:
        return self.address

# Model for IP address
class IpAddress(models.Model):
    location = models.CharField(verbose_name='Location',max_length=30,null=True)
    address = models.GenericIPAddressField(verbose_name='IP Address')
    asset = models.ForeignKey(verbose_name='Asset',to=Asset,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.TextField(verbose_name='Comment',blank=True) 
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
    create_by = models.CharField(verbose_name='Create_by',max_length=20,default='') 
    def __str__(self) -> str:
        return self.address


# Model for software
class Software(models.Model):
    name = models.CharField(verbose_name='Software Name',max_length=150)
    softwarekey = models.CharField(verbose_name='Software Key',max_length=150)
    quantity = models.SmallIntegerField(verbose_name='Quantity')
    asset = models.ManyToManyField(verbose_name='Asset',to=Asset)
    comment = models.TextField(verbose_name='Comment',blank=True) 
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
    create_by = models.CharField(verbose_name='Create_by',max_length=20,default='') 
    def __str__(self) -> str:
        return self.name
    # Get used count
    def used_count(self):
        return self.asset.all().count()
