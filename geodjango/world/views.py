from django.shortcuts import render
from django.views import generic
from .models import Stops
from django.db.models import Q
from .forms import QueryInputForm
from django.db import connection
import psycopg2
import re
import functools
import operator


def home(request):
    """View function for home page of site."""


    context = {}
    return render(request, 'base.html', context=context)


def input_query(request):

    new_schema(request)

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
            query_result = cursor.fetchone()
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

    query_result_parsed = ""
    query_result_parsed = functools.reduce(operator.add, (query_result))
    

    context = {
        'query_result': query_result_parsed,
        'error_case': error_case
    }
    

    return render(request, 'output_query.html', context)


def new_schema(request):

    raw = """
        DO LANGUAGE plpgsql
        $body$
        DECLARE
        old_schema NAME = 'public';
        new_schema NAME = 'sample';
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

def delete_schema(request):

    raw = """
        DROP SCHEMA IF EXISTS sample CASCADE;
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
    return render(request, 'base.html', context=context)