import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from document.my_forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count,Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator


# Home view
class HomeView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'document.view_document'
    def get(self,request):
        # If no data request return home page, else return data
        if not request.GET:
            count = Document.objects.all().count()
            return render(request,'document/home.html',{'count':count})

        # Get folder list
        if request.GET.get('folder') == 'all':
            folder_list = [item[0] for item in Document.objects.values_list('rootfolder').annotate(dcount=Count('rootfolder'))]
            while None in folder_list:
                folder_list.remove(None)
            folder_list.sort()
        else:
            folder_list = [request.GET.get('folder'),]
        data = []
        for folder in folder_list:
            totalCount = Document.objects.filter(rootfolder=folder).count()
            groupByYear = Document.objects.filter(rootfolder=folder).values_list('lastwrite__year').annotate(dcount=Count('lastwrite__year')).order_by('lastwrite__year')
            if groupByYear:           
                yearName,yearCount = zip(*groupByYear)
                data.append([folder,yearName,yearCount,totalCount])
            if data:
                result = {'Status':True,'data':data}
            else:
                result = {'Status':False,'data':'No data was found!'}
        return HttpResponse(json.dumps(result))
       

# Document search view
class SearchView(LoginRequiredMixin,PermissionRequiredMixin,View):
   permission_required = 'document.view_document'
   def get(self,request):
        #Define table head
        tableHead = ['Name','Last Write','Folder']
        # Get keywords
        if not request.GET.get('keywords'):
            return HttpResponse('Please type in a keywords!')
        keywords = request.GET.get('keywords')
        # Get documents 
        documentList = Document.objects.filter(Q(name__icontains=keywords)|Q(folder__icontains=keywords))         
        # Get tablebody
        tableBody = documentList.order_by('-lastwrite').values_list('name','lastwrite','folder')
        return render(request,'document/search.html',{'keywords':keywords,'tableHead':tableHead,'tableBody':tableBody})


# Document filter view
class DocumentFilterView(LoginRequiredMixin,PermissionRequiredMixin,View):
   permission_required = 'document.view_document'
   def get(self,request):
        #Define table head
        tableHead = ['Name','Last Write','Folder']
        # Get all documents 
        documentList = Document.objects.all()

        annotate_data = list(Document.objects.values('lastwrite__year','rootfolder').annotate(count=Count('rootfolder')))   
        # Get year choices
        year_choices = list({(item['lastwrite__year'],item['lastwrite__year']) for item in annotate_data})
        year_choices.sort(reverse=True)
        # Get root folder choices
        folder_choices = list({(item['rootfolder'],item['rootfolder']) for item in annotate_data})
        while (None,None) in folder_choices:
            folder_choices.remove((None,None))
        folder_choices.sort()

        # Get selected year and folder
        if request.GET:
            selected_year = request.GET.get('year','')
            selected_folder = request.GET.get('folder','')
        # If request.GET is nothing, set slected items as first choice
        else:
            selected_year = year_choices[0][0]
            selected_folder = folder_choices[0][0]
  
        # Filter document list
        if selected_year != '':                
            documentList = documentList.filter(lastwrite__year=selected_year)         
        if selected_folder != '':                
            documentList = documentList.filter(rootfolder=selected_folder)
        
        # Create form
        form = DocumentFilterForm({'year':selected_year,'folder':selected_folder})         
        form.fields['year'].choices += year_choices
        form.fields['folder'].choices += folder_choices 

        # Get tablebody
        tableBody = documentList.order_by('-lastwrite').values_list('name','lastwrite','folder')  
        return render(request,'document/document_filter.html',{'form':form,'tableHead':tableHead,'tableBody':tableBody})


# Custom search view
class CustomSearchView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'document.view_document'
    def get(self,request):
        # Define table head        
        tableHead = ['Name','Last Write','Folder']
        if not request.GET:
            form = CustomSearchForm()
            return render(request,'document/custom_search.html',{'form':form,'tableHead':tableHead})

        # Create form    
        form = CustomSearchForm(request.GET)

        # Get all documents
        documentList = Document.objects.all()

        # Filter documents
        if request.GET.get('name'):
            documentList = documentList.filter(name__icontains=request.GET.get('name'))
        if request.GET.get('folder'):
            documentList = documentList.filter(folder__icontains=request.GET.get('folder'))
        if request.GET.get('year'):
            documentList = documentList.filter(lastwrite__year=request.GET.get('year'))
        
        # Define table tablebody                                                             
        tableBody = documentList.order_by('-lastwrite').values_list('name','lastwrite','folder') 
        return render(request,'document/custom_search.html',{'form':form,'tableHead':tableHead,'tableBody':tableBody})


# Report view
class ReportView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'document.view_document'
    def get(self,request):

        # Report for duplicate document name
        if request.GET.get('reportname') == 'document_duplicate':
            tableHead = ['Name','Count']                                                   
            tableBody = Document.objects.values_list('name').annotate(c=Count('name')).filter(c__gt=1)
            return render(request,'document/reports/document_duplicate.html',{'tableHead':tableHead,'tableBody':tableBody})

        # Report for folder summary
        if request.GET.get('reportname') == 'folder_summary':
            tableHead = ['Folder','Year','Count']
            tableBody = Document.objects.values_list('folder','lastwrite__year').annotate(dcount=Count('folder'))
            return render(request,'document/reports/folder_summary.html',{'tableHead':tableHead,'tableBody':tableBody})

        # If no report name match, return 
        return HttpResponse('Please select a correct report name!')


# API view
@method_decorator(csrf_exempt, name='dispatch')
class APIView(View):
    def post(self,request,apiname):
        if apiname in ['documentsimport']:
            post_data = request.body.decode('utf-8')
            document_list = []
            for data in json.loads(post_data):
                # document = Document(**data)
                document_list.append(Document(**data))                
            try:
                # Clean old documents
                Document.objects.all().delete()
                new_documents = Document.objects.bulk_create(document_list)
                return HttpResponse(json.dumps({'status':True,'msg':f'Imported {len(new_documents)} documents'}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({'status':False}))                
        else:
            return HttpResponse(json.dumps({'status':False,'error':'The api do not exist'}))
        
