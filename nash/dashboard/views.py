from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .models import ExcelFile


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ExcelFile(file=request.FILES['file'], title=request.POST['title'])
            instance.save()
            return HttpResponseRedirect('/dashboard#good')
    else:
        form = UploadFileForm()
    return HttpResponseRedirect('/dashboard')


def index_view(request):

    files = ExcelFile.objects.all()[::-1]

    return render(request, 'dashboard/index.html', {'files':files})

