from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .models import ExelFile


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ExelFile(file=request.FILES['file'], title=request.POST['title'])
            instance.save()
            return HttpResponseRedirect('/dashboard#good')
    else:
        form = UploadFileForm()
    return render(request, 'dashboard/upload.html', {'form': form})


def index_view(request):

    files = ExelFile.objects.all()[::-1]

    return render(request, 'dashboard/index.html', {'files':files})

