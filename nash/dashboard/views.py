import sys
import time
import glob
import importlib.util
import pyexcel
from pyexcel.cookbook import merge_all_to_a_book
from os.path import basename
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import InputFile
from .models import Algorithm
from .models import Result
from .models import Project
from .forms import UploadInputFileForm


def projects_view(request, alert=''):
    projects = Project.objects.all()[::-1]

    return render(request, 'dashboard/projects.html', {'projects':projects, 'alert':alert})


def project_view(request, project_id):
    """ Detail project view """
    try:
        files = InputFile.objects.filter(project=project_id)[::-1]
        project = Project.objects.get(id=project_id)
        return render(request, 'dashboard/input-files.html', { 'files':files, 'project':project })
    except:
        return HttpResponseRedirect('/dashboard/')


def file_view(request, file_id, alert=''):
    """ Detail file view """
    try:
        input_file = InputFile.objects.get(id=file_id)
        algorithms = Algorithm.objects.filter(project=input_file.project)[::-1]
        results = Result.objects.filter(file_name=input_file)[::-1]
        input_file.file.name = basename(input_file.file.name)

        return render(request, 'dashboard/file.html', { 'file':input_file, 'algorithms':algorithms, 'results':results, 'alert':alert })
    except Exception as error:
        print(error)
        return HttpResponseRedirect('/dashboard/')


def upload_file(request): # TODO remake for algorithms and excels
    """ Upload file function """
    if request.method == 'POST':
        form = UploadInputFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save data from form to database
            instance = InputFile(file=request.FILES['file'], title=request.POST['title'], project=Project.objects.get(id=request.POST['project_id']))
            instance.save()
            
            # Reload page
            return HttpResponseRedirect(request.META['HTTP_REFERER'] + '#good') # TODO Think up normal notifications
    else:
        form = UploadInputFileForm()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def delete_file(request):
    """ Delete file function """
    if request.method == 'POST':
        try:
            if request.POST['type'] == 'input_file':
                # Delete input file in project
                InputFile.objects.get(id=request.POST['file']).delete()
            elif request.POST['type'] == 'result':
                # Delete file result
                Result.objects.get(id=request.POST['file']).delete()

                # Reload page
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except Exception as error:  # TODO handle exceptions
            print(error)    
    return HttpResponseRedirect('/dashboard/')


def execude_file(request):
    """ Algorithm execude function """
    if request.method == 'POST':

        file_id = request.POST['file-id']
        algorithm_id = request.POST['alorithm-id']

        try:
            algorithm = Algorithm.objects.get(id=algorithm_id)
            excel_file = InputFile.objects.get(id=file_id)

            old_file_path = excel_file.file.url
            new_file_path = './uploads/results/' + time.strftime("%H%M%S") + basename(old_file_path).split('.')[0]

            # Get module
            algorithm_module = importlib.import_module('uploads.algorithms.' + basename(algorithm.file.name).split('.')[0])

            # Execute algorithm
            algorithm_module.get_result('.' + old_file_path, new_file_path)

            # Convert .csv to .xlxs
            merge_all_to_a_book(glob.glob(new_file_path + '.csv'), new_file_path + '.xlsx' )

            new_file_path = new_file_path + '.xlsx'
            # Save result to database
            Result.objects.create(file_name=excel_file, algorithm=algorithm, file=new_file_path)
            
        except Exception as error:
           return file_view(request, file_id, alert=error)

    return redirect('/dashboard/file/' + file_id)