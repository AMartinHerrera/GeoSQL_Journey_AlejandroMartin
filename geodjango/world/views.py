from django.shortcuts import render
from django.views import generic
from .models import Stops
from django.db.models import Q
from .forms import QueryInputForm
from django.db import connection
import psycopg2


# Create your views here.

def home(request):
    """View function for home page of site."""


    context = {}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'base.html', context=context)


def input_query(request):

    if request.method == 'POST':
        form = QueryInputForm(request.POST)
        # if form.is_valid():
        #     query = form.cleaned_data['query']

    else:
        form = QueryInputForm()

    context = {
        'form': form,
    }

    return render(request, 'input_query.html', context)


def output_query(request):

    query = request.POST['query']
    query_result = ""
    error_case = ""


    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            query_result = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error) 
            error_case = "Error while fetching data from PostgreSQL"

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")  

    if query_result is "":
        error_case = "Error with the geoSQL query executed. Try again!"

    context = {
        'query_result': query_result,
        'error_case': error_case
    }
    

    return render(request, 'output_query.html', context)
