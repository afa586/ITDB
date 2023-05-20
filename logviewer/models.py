from django.db import models


#Class for windows event logs
class NetEventLog(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=True)
    server = models.CharField(max_length=50, null=True)
    event_id = models.CharField(max_length=50, null=True)
    count = models.IntegerField(null=True)
    check_date = models.DateTimeField(null=True)
    check_by = models.CharField(max_length=50, null=True)
    action = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    def solution(self):
        # Check solution status
        check_exist = NetEventSolution.objects.filter(event_id=self.event_id.strip())
        if check_exist.exists():
            return check_exist.first()
        return NetEventLog()

    class Meta:
        db_table = 'TB_NetEventlog'

#Class for windows event log solution
class NetEventSolution(models.Model):
    id = models.AutoField(primary_key=True)
    solution_id = models.CharField(max_length=255, null=True,verbose_name='Solution ID', unique=True)
    date = models.DateField(null=True,verbose_name='Date')
    source = models.CharField(max_length=255, null=True,verbose_name='Source')
    event_id = models.CharField(max_length=50,null=True,verbose_name='Event ID')
    error_desc = models.TextField(null=True,verbose_name='Error Description')
    cause = models.TextField(null=True,verbose_name='Cause&Solution')
    severity_choices = (('Low','Low'),('High','High'))
    severity = models.CharField(max_length=255, null=True,verbose_name='Severity',choices=severity_choices)
    action = models.TextField(null=True,verbose_name='Action')
    approve_by = models.CharField(max_length=255, null=True)
    fix_by_choices = (('Network','Network'),('APP','APP'))
    fix_by = models.CharField(choices=fix_by_choices,max_length=255, null=True)
    os = models.CharField(max_length=50, null=True,verbose_name='OS')
    approve_date = models.DateField(null=True)
    recorder = models.CharField(max_length=50, null=True)
    add_date = models.DateTimeField(null=True)
    changed_by = models.CharField(max_length=50, null=True)
    changed_date = models.DateTimeField(null=True)
    # status = models.CharField(max_length=50, null=True)
    status_choices = (('','Status'),('1','Pending for solution'),('2','Pending approve'),('3','Approved'),('4','Reviewed'))
    status = models.CharField(choices=status_choices,max_length=10, null=True,default='1')
    temp2 = models.CharField(max_length=200, null=True)
    solution_by = models.CharField(max_length=50, null=True)
    solution_date = models.DateTimeField(null=True)
    review_by = models.CharField(max_length=50, null=True)
    review_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'TB_NetEventSolution'


# Model for Net Event Solution history
class NetEventSolutionHistory(models.Model):
    solution = models.ForeignKey(verbose_name='Net Event Solution',to=NetEventSolution,on_delete=models.CASCADE)
    operator = models.CharField(verbose_name='Operator',max_length=20)
    action = models.CharField(verbose_name='Action',max_length=20,default='None')
    comment = models.TextField(verbose_name='Comment',null=True)  
    create_time = models.DateTimeField(verbose_name='Create Time',auto_now_add=True) 

    class Meta:
        db_table = 'TB_NetEventSolutionHistory' 