import sys
import time
import glob
import importlib.util
from pyexcel.cookbook import merge_all_to_a_book
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


@login_required
def projects_view(request, alert=''):
    """ Projects list view on /dashboard/ page """
    projects = Project.objects.all()[::-1]

    return render(request, 'dashboard/projects.html',
                  {'projects': projects, 'alert': alert})

@login_required
def project_view(request, project_id):
    """ Detail project view """
    try:
        algorithms = Algorithm.objects.filter(project=project_id)[::-1]
        project = Project.objects.get(id=project_id)

        return render(request, 'dashboard/project.html',
                      {'algorithms': algorithms, 'project': project})
    except BaseException:
        return redirect('/')

@login_required
def algorithm_view(request, algorithm_id, project_id, alert=''):
    # try:
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

    # except Exception as error:
        # print(error) 
        # return redirect('/algorithm/' + algorithm_id)

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
                file_id = upload_file(request)

                algorithm_id = request.POST['alorithm-id']
                
                algorithm = Algorithm.objects.get(id=algorithm_id)
                excel_file = InputFile.objects.get(id=file_id)

                old_file_path = excel_file.file.url
                new_file_path = './uploads/results/' + \
                    time.strftime("%H%M%S") + basename(old_file_path).split('.')[0] + '.csv'

                # Getting module
                algorithm_module = importlib.import_module(
                    'uploads.algorithms.' + basename(algorithm.file.name).split('.')[0])

                # Execute algorithm
                data = {
                    'input_path': '.' + old_file_path, 
                    'output_path' : new_file_path 
                }
                algorithm_module.get_result(data)

                # Convert .csv to .xlxs
                # merge_all_to_a_book(glob.glob(new_file_path + '.csv'), new_file_path + '.xlsx')
                # new_file_path = new_file_path + '.xlsx'

                # Save result to database
                Result.objects.create(
                    file_name=excel_file,
                    algorithm=algorithm,
                    file=new_file_path,
                    project=Project.objects.get(id=request.POST['project_id']))
                
                return redirect(request.META['HTTP_REFERER'])
            elif request.POST['type'] == 'input_api':
                # forming data for API request
                data = {
                    'output_name': './uploads/results/' + time.strftime("%H%M%S") + '.csv',
                    'url_token': request.POST['url_token'],
                    'client_id': request.POST['client_id'],
                    'client_secret': request.POST['client_secret'],
                    'user_agent': request.POST['user_agent'],
                    'host_api': request.POST['host_api']
                }
                algorithm_id = request.POST['alorithm-id']
                
                # Getting module
                algorithm = Algorithm.objects.get(id=algorithm_id)
                algorithm_module = importlib.import_module(
                    'uploads.algorithms.' + basename(algorithm.file.name).split('.')[0])

                new_file_path = data['output_name']
                # data['output_name'] += '.csv'
                # Execute algorithm
                algorithm_module.get_result(data)


                # Convert .csv to .xlxs
                # try:
                    # merge_all_to_a_book(glob.glob(new_file_path + '.csv'), new_file_path + '.xlsx')
                    # new_file_path = new_file_path + '.xlsx'
                # except IOError as e:
                    # print(u'File not found')

                project = Project.objects.get(id=request.POST['project_id'])

                # Save result if algorithm sended across api
                if len(new_file_path) < 7:
                    new_file_path = ''

                    Result.objects.create(
                    algorithm=algorithm,
                    project=project)
                # Save result if algorithm create local file 
                else:
                    Result.objects.create(
                    algorithm=algorithm,
                    file=new_file_path,
                    project=project)

                return redirect('/algorithm/{}/{}'.format(request.POST['alorithm-id'], request.POST['project_id']) )
        except Exception as error:
            return algorithm_view(request, request.POST['alorithm-id'], request.POST['project_id'] , alert=error)

    return redirect('/')
