import sys
import time
import glob
import importlib.util
# from pyexcel.cookbook import merge_all_to_a_book
from os.path import basename
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import InputFile
from .models import Algorithm
from .models import Result
from .models import Project
from .forms import UploadInputFileForm
from .forms import UploadAlgorithmFileForm
from django.contrib.auth.decorators import login_required
from .scripts import *
import logging


logger = logging.getLogger(__name__)


@login_required
def projects_view(request, alert=''):
    """ Projects list view on /dashboard/ page """
    projects = Project.objects.all()[::-1]
    return render(request, 'dashboard/projects.html',
                  {'projects': projects, 'alert': alert})

@login_required
def project_view(request, project_id, alert=''):
    """ Detail project view """
    try:
        algorithms = Algorithm.objects.filter(project=project_id)[::-1]
        project = Project.objects.get(id=project_id)

        return render(request, 'dashboard/project.html',
                      {'algorithms': algorithms, 'project': project, 'alert':alert})
    except BaseException:
        return redirect('/')

@login_required
def algorithm_view(request, algorithm_id, project_id, alert=''):
    try:
        algorithm_data = {}
        algorithm = Algorithm.objects.get(id=algorithm_id)
        project = Project.objects.get(id=project_id)
        results = Result.objects.filter(algorithm=algorithm, project=project)[::-1]

        # Get module
        algorithm_module = importlib.import_module('uploads.algorithms.' + \
                            basename(algorithm.file.name).split('.')[0])
        
        # Check algorithm type
        if algorithm_module.EXECUTE_TYPE == 'API':
            algorithm_data['type'] = 'API'
        elif algorithm_module.EXECUTE_TYPE == 'FILE':
            algorithm_data['type'] = 'FILE'
        else:
            algorithm_data['type'] = 'NONE'

        return render(request,
                        'dashboard/algorithm.html',
                        {'algorithm': algorithm,
                        'results': results,
                        'algorithm_data': algorithm_data,
                        'project': project,
                        'alert': alert })

    except Exception as error:
        logger.error(error)
        return project_view(request, project_id, alert='')

@login_required
def file_view(request, file_id, alert=''):
    """  Temporarily not used!!
    Detail file view """
    try:
        input_file = InputFile.objects.get(id=file_id)
        algorithms = Algorithm.objects.filter(project=input_file.project)[::-1]
        results = Result.objects.filter(file_name=input_file)[::-1]
        input_file.file.name = basename(input_file.file.name)

        return render(request,
                      'dashboard/file.html',
                      {'file': input_file,
                       'algorithms': algorithms,
                       'results': results,
                       'alert': alert})
    except Exception as error:
        print(error)
        return redirect('/')

@login_required
def upload_file(request):  # TODO remake for algorithms and excels
    """ Upload file function """
    if request.method == 'POST':
        # Upload xlsx/xls file
        if request.POST['type'] == 'input_file':
            form = UploadInputFileForm(request.POST, request.FILES)
            if form.is_valid():
                # Save data from form to database
                instance = InputFile(
                    file=request.FILES['file'],
                    title=request.POST['title'],
                    project=Project.objects.get(
                        id=request.POST['project_id']))
                instance.save()

                # Reload page
                return instance.id
        # Upload algorithm
        elif request.POST['type'] == 'algorithm_file':
            form = UploadAlgorithmFileForm(request.POST, request.FILES)
            if form.is_valid():
                # Save data from form to database
                instance = Algorithm(
                    file=request.FILES['file'],
                    title=request.POST['title'])
                instance.save()
                instance.project.add(Project.objects.get(id=request.POST['project_id']))
                
                # Reload page
                return redirect(
                    request.META['HTTP_REFERER'] +
                    '#good')  # TODO Think up normal notifications
    # else:
        # form = UploadInputFileForm()
    return redirect(request.META['HTTP_REFERER'])

@login_required
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
                return redirect(request.META['HTTP_REFERER'])
        except Exception as error:  # TODO handle exceptions
            print(error)
    return redirect('/')

@login_required
def execude_file(request):
    """ Function execude algorithm """
    if request.method == 'POST':
        try:
            if request.POST['type'] == 'input_file':

                execute_file_type(request)
                
                return redirect(request.META['HTTP_REFERER'])
            elif request.POST['type'] == 'input_api':

                execute_api_type(request)                

                return redirect('/algorithm/{}/{}'.format(request.POST['alorithm-id'], request.POST['project_id']) )
        except Exception as error:
            return algorithm_view(request, request.POST['alorithm-id'], request.POST['project_id'] , alert=error)
    return redirect('/')
