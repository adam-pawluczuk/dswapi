import csv as csv_builtin

from django.http import HttpResponse
from django.views.generic import ListView
from django_tables2 import SingleTableView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
import petl

from dswapi.services.etl_pipeline import get_page, execute_pipeline
from dswapi.tables import CSVListTable, CSVTable
from dswapi.models import CSVFile


def index(request):
    response = get_page()
    return HttpResponse(response)


def download(request):
    execute_pipeline()
    return HttpResponseRedirect('/')


def csv_view(request, id):
    csv_file = CSVFile.objects.get(pk=id)
    file_path = f"{settings.CSV_ROOT_PATH}/{csv_file.file_name}"
    input_file = csv_builtin.DictReader(open(file_path))
    table = CSVTable(input_file)

    return render(request, "csv_view.html", {
        "table": table
    })


class CSVListView(SingleTableView):
    model = CSVFile
    table_class = CSVListTable
    template_name = 'csv_list_view.html'
