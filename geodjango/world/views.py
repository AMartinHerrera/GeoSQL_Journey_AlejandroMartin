from django.shortcuts import render
from .forms import QueryInputForm
from django.db import connection
import psycopg2
import functools
import operator

global_var = -1

def add_global_var():
    global global_var
    global_var = global_var + 1

def sub_global_var():
    global global_var
    global_var = global_var - 1

def home(request):
    """View function for home page of site."""


    context = {}
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

    conn = psycopg2.connect(host="localhost", 
                    port="5432", 
                    user="postgres", 
                    password="postgres", 
                    database="geodjango", 
                    options="-c search_path=dbo,user" + str(global_var))

    conn.autocommit = True

    # sql="""CREATE TABLE siiuuuu ( PersonID int, City varchar(255));"""
    
    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
            query_result = cursor.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error) 
            error_case = "Error while fetching data from PostgreSQL"

        finally:
            # closing database connection.
            if conn:
                cursor.close()
                conn.commit()
                conn.close()
                print("PostgreSQL connection is closed")  

    

    if query_result is "":
        error_case = "The return of your query is empty!"

    query_result_parsed = ""
    # query_result_parsed = functools.reduce(operator.add, (query_result))
    

    context = {
        'query_result': query_result_parsed,
        'error_case': error_case
    }

    return render(request, 'output_query.html', context)


def new_schema(request):

    add_global_var()

    raw = """
        DO LANGUAGE plpgsql
        $body$
        DECLARE
        old_schema NAME = 'public';
        new_schema NAME = 'user""" +str(global_var)+ """';
        tbl TEXT;
        sql TEXT;
        BEGIN
        EXECUTE format('CREATE SCHEMA IF NOT EXISTS %I', new_schema);

        FOR tbl IN
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema=old_schema
        LOOP
            sql := format(
                    'CREATE TABLE IF NOT EXISTS %I.%I '
                    '(LIKE %I.%I INCLUDING INDEXES INCLUDING CONSTRAINTS)'
                    , new_schema, tbl, old_schema, tbl);

            EXECUTE sql;

            sql := format(
                    'INSERT INTO %I.%I '
                    'SELECT * FROM %I.%I'
                    , new_schema, tbl, old_schema, tbl);

            EXECUTE sql;
        END LOOP;
        END
        $body$;
        """

    error_case = ""

    with connection.cursor() as cursor:
        try:
            cursor.execute(raw)
        except (Exception, psycopg2.Error) as error:
            print("Error while creating new schema in the database", error) 
            error_case = "Error while creating new schema in the database"

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed") 


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


def delete_schema(request):

    raw = """
        DROP SCHEMA IF EXISTS user"""+str(global_var)+""" CASCADE;
        """

    error_case = ""

    with connection.cursor() as cursor:
        try:
            cursor.execute(raw)
        except (Exception, psycopg2.Error) as error:
            print("Error while creating new schema in the database", error) 
            error_case = "Error while creating new schema in the database"

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed") 
    
    context = {}
    sub_global_var()
    return render(request, 'base.html', context=context)