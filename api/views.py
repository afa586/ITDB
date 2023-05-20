import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from itasset.models import Tanium
from itasset.my_forms import TaniumForm
from document.models import Document
from document.my_forms import documentForm

# Create your views here.
# View for Tanium import
@method_decorator(csrf_exempt, name='dispatch')
class TaniumImport(View):
    def post(self,request):
        # Check if the record exist
        check_exist = Tanium.objects.filter(name=request.POST.get('name'))
        if check_exist.exists():
            form = TaniumForm(data=request.POST,instance=check_exist.first())
        else:
            form = TaniumForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                result = {'status':True}
            except Exception as e:
                result = {'status':False,'error':str(e)}
        else:
            result = {'status':False,'error':str(form.errors)}
        return HttpResponse(json.dumps(result))


# View for document import
@method_decorator(csrf_exempt, name='dispatch')
class DocumentImport(View):
    def post(self,request):
        # Get post data
        post_data = request.body.decode('utf-8')
        document_list = []
        for data in json.loads(post_data):
            document_list.append(Document(**data))                
        try:
            # Clean old documents
            Document.objects.all().delete()
            new_documents = Document.objects.bulk_create(document_list)
            return HttpResponse(json.dumps({'status':True,'msg':f'Imported {len(new_documents)} documents'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status':False}))                
