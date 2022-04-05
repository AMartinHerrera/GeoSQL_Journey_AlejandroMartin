from django.shortcuts import render
from django.views import generic
from .models import Stops
from django.db.models import Q
from .forms import QueryInputForm
from django.db import connection
import psycopg2


# Create your views here.

global_query = 'query'

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


# def my_custom_sql(query):
#     with connection.cursor() as cursor:
#         try:
#             cursor.execute(query)
#             row = cursor.fetchall()

#             if row is None:
#                 return

#         except (Exception, psycopg2.Error) as error:
#             print("Error while fetching data from PostgreSQL", error) 

#         finally:
#             # closing database connection.
#             if connection:
#                 cursor.close()
#                 connection.close()
#                 print("PostgreSQL connection is closed")       
        
#     return row

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




# def output_query(request):

#     query = request.POST['query']

#     try:
#         connection = psycopg2.connect(user="postgres",
#                                     password="postgres",
#                                     host="localhost",
#                                     port="5432",
#                                     database="geodjango")

#         print("Selecting rows from mobile table using cursor.fetchall")
#         cursor = connection.cursor()
#         postgreSQL_select_Query = "SELECT * FROM world_stops"

#         cursor.execute(postgreSQL_select_Query)
#         mobile_records = cursor.fetchmany(2)

#         print("Fetching 2 rows")
#         for row in mobile_records:
#             print("Id = ", row[0], )
#             print("Model = ", row[1])
#             print("Price  = ", row[2], "\n")

#         mobile_records = cursor.fetchmany(2)

#         print("Printing next 2 rows")
#         for row in mobile_records:
#             print("Id = ", row[0], )
#             print("Model = ", row[1])
#             print("Price  = ", row[2], "\n")

#     except (Exception, psycopg2.Error) as error:
#         print("Error while fetching data from PostgreSQL", error)

#     finally:
#         # closing database connection.
#         if connection:
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")


#     context = {
#         'query_result': query_result
#     }

#     return render(request, 'output_query.html', context)







# class ResultQuery(generic.ListView):
#     model = Stops
#     template_name = 'result_query.html'

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         # self.request.session['query'] = query
#         object_list = query

#         return object_list