import json
from django.http import HttpResponse
from django.shortcuts import redirect, render,get_list_or_404,get_object_or_404
from django.views import View
from datetime import date,datetime
from logviewer.models import *
from logviewer.my_forms import *
from django.http import JsonResponse
from django.forms.utils import ErrorDict

# View to list windows event logs
class NetEventLogList(View):
    def get(self,request):
        user_group = get_groups(request)
        date_from = request.GET.get('date_from',date.today())
        date_to = request.GET.get('date_to',date.today())
        log_list = NetEventLog.objects.filter(date__gte=date_from).filter(date__lte=date_to)
        form = NetEventFilter({'date_from':date_from,'date_to':date_to})
        return render(request,'logviewer/netlog/list.html',locals())  

    def post(self,request):
        # data = request.POST.getlist('data[]')
        data = json.loads(request.POST.get('data'))
        
        # Loop through the rows and update the corresponding records
        for row in data:
            obj = NetEventLog.objects.get(pk=row[0])
            obj.action = row[7]
            obj.description = row[8]
            obj.check_by = get_user_name(request)
            obj.check_date = date.today()
            obj.save()
        
        # Return a success response
        return JsonResponse({'success': True})


# View to list all windows event solution
class NetEventSolutionList(View):
    def get(self,request):
        user_group = get_groups(request)
        solution_list = NetEventSolution.objects.all().order_by('-id')
        form = NetEventSolutionFilter()
        # Filter data and create filter form
        if request.GET:
            form = NetEventSolutionFilter(request.GET)
            for k,v in dict(request.GET).items():
                if v[0] != '':
                    solution_list = solution_list.filter(**{k:v[0]})
        solution_form = NetEventSolutionForm()
        return render(request,'logviewer/netlogsolution/list.html',locals())  
    
# View to add new windows event solution
class NetEventSolutionAdd(View):
    def post(self,request):
        form = NetEventSolutionForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.add_date = date.today()
            obj.recorder = get_user_name(request)
            obj.save()
            # Add history
            NetEventSolutionHistory.objects.create(solution=obj,action="Create",operator=get_user_name(request),comment=f'Create {obj.solution_id}')
            return JsonResponse({'status': True})
        else:
            # Return an error response with the detailed error messages
            errors = ErrorDict()
            for field, messages in form.errors.items():
                errors[field] = [str(m) for m in messages]
            return JsonResponse({'status': False, 'message': 'Invalid form.', 'errors': errors})
        

# View to edit windows event solution(Basic information)
class NetEventSolutionEdit(View):
    def post(self,request,pk):
        if NetEventSolution.objects.filter(pk=pk).exists():
            solution_obj = NetEventSolution.objects.filter(pk=pk).first()
            solution_before_edit = dict(solution_obj.__dict__) 
            form = NetEventSolutionForm(request.POST,instance=solution_obj)
            if form.is_valid():
                obj = form.save()
                obj.changed_date = date.today()
                obj.changed_by = get_user_name(request)
                obj.save()
                # Add history
                # Check what changed
                comment = []
                for item in form.changed_data:
                    comment.append('Change %s from %s to %s'%(item,solution_before_edit[item],form.cleaned_data[item]))
                if comment != []:
                    NetEventSolutionHistory.objects.create(solution=obj,action="Edit",operator=get_user_name(request),comment=', '.join(comment))
                return JsonResponse({'status': True})
            else:
                # Return an error response with the detailed error messages
                errors = ErrorDict()
                for field, messages in form.errors.items():
                    errors[field] = [str(m) for m in messages]
                return JsonResponse({'status': False, 'message': 'Invalid form!', 'errors': errors})
        else:
            return JsonResponse({'status': False, 'message': 'Object do not exist!'})
        
# View to edit windows event solution(Cause related)
class NetEventSolutionCauseEdit(View):
    def post(self,request,pk):
        if NetEventSolution.objects.filter(pk=pk).exists():
            solution_obj = NetEventSolution.objects.filter(pk=pk).first()
            solution_before_edit = dict(solution_obj.__dict__) 
            form = NetEventSolutionCauseForm(request.POST,instance=solution_obj)
            if form.is_valid():
                obj = form.save()
                obj.changed_date = date.today()
                obj.changed_by = get_user_name(request)
                if obj.status == '1':
                    obj.status = '2'
                if obj.solution_by == None:
                    obj.solution_by = get_user_name(request)
                if obj.solution_date == None:
                    obj.solution_date = date.today()
                obj.save()
                # Add history
                # Check what changed
                comment = []
                for item in form.changed_data:
                    comment.append('Change %s from %s to %s'%(item,solution_before_edit[item],form.cleaned_data[item]))
                if comment != []:
                    NetEventSolutionHistory.objects.create(solution=obj,action="Edit Cause",operator=get_user_name(request),comment=', '.join(comment))
                return JsonResponse({'status': True})
            else:
                # Return an error response with the detailed error messages
                errors = ErrorDict()
                for field, messages in form.errors.items():
                    errors[field] = [str(m) for m in messages]
                return JsonResponse({'status': False, 'message': 'Invalid form!', 'errors': errors})
        else:
            return JsonResponse({'status': False, 'message': 'Object do not exist!'})
        
# View to approve windows event solution
class NetEventSolutionApprove(View):
    def post(self,request,pk):
        if NetEventSolution.objects.filter(pk=pk).exists():
            solution_obj = NetEventSolution.objects.filter(pk=pk).first()
            if solution_obj.status == '2':
                try:
                    solution_obj.status = '3'
                    solution_obj.approve_by = get_user_name(request)
                    solution_obj.approve_date = date.today()
                    solution_obj.save()
                    # Add history
                    NetEventSolutionHistory.objects.create(solution=solution_obj,action="Approve",operator=get_user_name(request))
                    return JsonResponse({'status': True})
                except Exception as e:            
                    return JsonResponse({'status': False, 'errors': str(e)})
            return JsonResponse({'status': False, 'errors': 'Only pending approve solution can be approved!'})
        else:
            return JsonResponse({'status': False, 'errors': 'Object do not exist!'})
        
# View to review windows event solution
class NetEventSolutionReview(View):
    def post(self,request,pk):
        if NetEventSolution.objects.filter(pk=pk).exists():
            solution_obj = NetEventSolution.objects.filter(pk=pk).first()
            if solution_obj.status == '3':
                try:
                    solution_obj.status = '4'
                    solution_obj.review_by = get_user_name(request)
                    solution_obj.review_date = date.today()
                    solution_obj.save()
                    # Add history
                    NetEventSolutionHistory.objects.create(solution=solution_obj,action="Review",operator=get_user_name(request))
                    return JsonResponse({'status': True})
                except Exception as e:            
                    return JsonResponse({'status': False, 'errors': str(e)})
            return JsonResponse({'status': False, 'errors': 'Only approved solution can be reviewed!'})
        else:
            return JsonResponse({'status': False, 'errors': 'Object do not exist!'})
        
# View to unapprove windows event solution
class NetEventSolutionUnApprove(View):
    def post(self,request,pk):
        if NetEventSolution.objects.filter(pk=pk).exists():
            solution_obj = NetEventSolution.objects.filter(pk=pk).first()
            if solution_obj.status == '3' or solution_obj.status == '4':
                try:
                    solution_obj.status = '2'
                    solution_obj.review_by = None
                    solution_obj.review_date = None
                    solution_obj.approve_by = None
                    solution_obj.approve_date = None
                    solution_obj.save()
                    # Add history
                    NetEventSolutionHistory.objects.create(solution=solution_obj,action="UnApprove",operator=get_user_name(request),comment= request.POST.get('comment'))
                    return JsonResponse({'status': True})
                except Exception as e:            
                    return JsonResponse({'status': False, 'errors': str(e)})
            return JsonResponse({'status': False, 'errors': 'Only approved or reviewed solution can be unapproved!'})
        else:
            return JsonResponse({'status': False, 'errors': 'Object do not exist!'})
        
# View to show net solution details
class NetEventSolutionDetail(View):
    def get(self,request,pk):
        user_group = get_groups(request)
        solution_obj = get_object_or_404(NetEventSolution, pk=pk)
        fixby_group = f'LogViewer_{solution_obj.fix_by}'
        history = solution_obj.neteventsolutionhistory_set.all()
        edit_form = NetEventSolutionForm(instance=solution_obj)
        cause_form = NetEventSolutionCauseForm(instance=solution_obj)
        return render(request,'logviewer/netlogsolution/detail.html',locals()) 
    


# Function to get user group
def get_groups(request):
    return [obj.name for obj in request.user.groups.all()]

# Function to get user name
def get_user_name(request):
    if request.user.first_name:
        return f'{request.user.last_name}, {request.user.first_name}'
    return request.user.name
