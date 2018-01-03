import sys
import time
import glob
import importlib.util
import pyexcel.ext.xlsx 
from pyexcel.cookbook import merge_all_to_a_book
from os.path import basename
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import ExcelFile
from .models import Algorithm
from .models import Result
from .forms import UploadFileForm


def index_view(request): # TODO Rename template
    """ List of all files in database """
    files = ExcelFile.objects.all()[::-1]
    return render(request, 'dashboard/index.html', {'files':files})


def file_view(request, pk):
    """ Detail file view """
    try:
        excel_file = ExcelFile.objects.get(id=pk)
        algorithms = Algorithm.objects.all()[::-1]
        results = Result.objects.filter(file_name=excel_file)

        return render(request, 'dashboard/file.html', {'file':excel_file, 'algorithms':algorithms, 'results':results})
    except:
        return HttpResponseRedirect('/dashboard/')


def upload_file(request): # TODO remake for algorithms and excels
    """ Upload file function """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save data with form to database
            instance = ExcelFile(file=request.FILES['file'], title=request.POST['title'])
            instance.save()
            return HttpResponseRedirect('/dashboard/#good') # TODO Think up normal notifications
    else:
        form = UploadFileForm()
    return HttpResponseRedirect('/dashboard/')


def del_file(request): # TODO remake for delete algorithms and excels
    """ Delete file function """
    if request.method == 'POST':
        try:
            file = ExcelFile.objects.get(id=request.POST['file'])
            file.delete()
        except:  # TODO handle exceptions
            pass    
    return HttpResponseRedirect('/dashboard/')


def execude_file(request):
    """ Algorithm execude function """
    if request.method == 'POST':
        try:
            algorithm = Algorithm.objects.get(id=request.POST['alorithm-id'])
            excel_file = ExcelFile.objects.get(id=request.POST['file-id'])

            old_file_path = excel_file.file.url
            new_file_path = './uploads/results/' + time.strftime("%H%M%S") + basename(old_file_path).split('.')[0]

            # Get module
            algorithm_module = importlib.import_module('uploads.algorithms.' + basename(algorithm.file.name).split('.')[0])
            algorithm_module.get_result('.' + old_file_path, new_file_path)

            # Convert .csv to .xlxs
            merge_all_to_a_book(glob.glob(new_file_path + '.csv'), new_file_path +'.xlsx' )

            new_file_path = new_file_path + '.xlsx'
            # Save result to database
            Result.objects.create(file_name=excel_file, algorithm=algorithm, file=new_file_path)
            
        except:
            # TODO handle exceptions
            pass
    return HttpResponseRedirect('/dashboard/file/'+request.POST['file-id'])