from django.shortcuts import render
from .forms import QueryInputForm
from django.db import connection
import psycopg2
import functools
import operator
from tkinter import *
import tkinter.messagebox
import json
import os
import requests


global_var = 0
global_context_request = 0

def add_global_context_request():
    global global_context_request
    global_context_request = global_context_request + 1

def sub_global_context_request():
    global global_context_request
    global_context_request = global_context_request - 1

def reset_global_context_request():
    global global_context_request
    global_context_request = 0

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

    description=""
    stage=""

    if request.method == 'POST':
        form = QueryInputForm(request.POST)

    else:
        form = QueryInputForm()

    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']

    f.close()

    context = {
        'form': form,
        'stage': stage,
        'description': description,
    }

    return render(request, 'input_query.html', context)


def output_query(request):

    query = request.POST['query']
    query_result = ""
    query_result_parsed = ""
    error_case = ""
    solution=""
    description=""
    stage=""
    flag=0

    # conn = psycopg2.connect(host="localhost", 
    #                 port="5432", 
    #                 user="postgres", 
    #                 password="postgres", 
    #                 database="geodjango", 
    #                 options="-c search_path=dbo,user" + str(global_var))

    conn = psycopg2.connect(host="localhost", 
                    port="5432", 
                    user="postgres", 
                    password="postgres", 
                    database="geodjango", 
                    options="-c search_path=dbo,public")

    conn.autocommit = True

    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
            query_result = cursor.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error) 
            error_case = error
            error_alert_popup("Error!", error_case)
            flag = 1
        finally:
            # closing database connection.
            if conn:
                cursor.close()
                conn.commit()
                conn.close()
                print("PostgreSQL connection is closed")  

    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']
            solution = i['solution']

    f.close()

    


    if flag == 1:
        if request.method == 'POST':
            form = QueryInputForm(request.POST)
        else:
            form = QueryInputForm()
        context = {
            'form': form,
            'stage': stage,
            'description': description,
        }
        return render(request, 'input_query.html', context)

    else:
        query_result_parsed = functools.reduce(operator.add, (query_result))
        if str(query_result_parsed) == solution:
            add_global_context_request()
            success_alert_popup("Message", "Correct! Well done!!")
        else:
            message = "The result obtained '" + str(query_result_parsed) + "' is not the expected."
            error_alert_popup("Error!", message)
            if request.method == 'POST':
                form = QueryInputForm(request.POST)
            else:
                form = QueryInputForm()
            context = {
                'form': form,
                'stage': stage,
                'description': description,
            }
            return render(request, 'input_query.html', context)

    context = {
        'query_result': query_result_parsed,
        'error_case': error_case
    }

    return render(request, 'output_query.html', context)


def show_hint(request):

    form = QueryInputForm()

    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']
            hint = i['hint']

    f.close()

    success_alert_popup("Message", hint)

    next_page="output_query"

    context = {
        'form': form,
        'stage': stage,
        'description': description,
        'next_page': next_page
    }

    return render(request, 'input_query.html', context)


def error_alert_popup(title, message):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 700     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    # m += '\n'
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="Try again!", command=root.destroy, width=10)
    b.pack()
    mainloop()


def success_alert_popup(title, message):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 700     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    # m += '\n'
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK!", command=root.destroy, width=10)
    b.pack()
    mainloop()

def new_schema(request):

    add_global_context_request()
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

    else:
        form = QueryInputForm()

    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']


    f.close()
    
    context = {
        'form': form,
        'stage': stage,
        'description': description
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
    reset_global_context_request()
    return render(request, 'base.html', context=context)