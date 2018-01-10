import sys
import time
import importlib.util
from os.path import basename
from .models import InputFile
from .models import Algorithm
from .models import Result
from .models import Project

def execute_file_type(request):
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


def execute_api_type(request):
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