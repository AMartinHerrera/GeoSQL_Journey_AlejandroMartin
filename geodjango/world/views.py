
# This file is where all the functions that need to be executed are defined

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

# Here are defined the global variables for the management of the context and users schemas
global_var = 0
global_context_request = 0

#Functions to add, substract, and reset the global variables:

def add_global_context_request():
    global global_context_request
    global_context_request = global_context_request + 1

def sub_global_context_request():
    global global_context_request
    global_context_request = global_context_request - 1

def reset_global_context_request():
    global global_context_request
    global_context_request = 0

def add_global_user_var():
    global global_var
    global_var = global_var + 1

def sub_global_user_var():
    global global_var
    global_var = global_var - 1

# This home function just redirects to base.html template, the main template 
def home(request):
    """View function for home page of site."""

    # Create an empty context and render the template with it
    context = {}
    return render(request, 'base.html', context=context)

# The purpose of this function is to render the input.html template with the information that reads from the config.json file
def input_query(request):

    description=""
    stage=""

    # Request with the form created to insert the query
    if request.method == 'POST':
        form = QueryInputForm(request.POST)

    else:
        form = QueryInputForm()

    #read the information fromt he config.json file
    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']

    f.close()

    # Create the context with the information and render the template with it
    context = {
        'form': form,
        'stage': stage,
        'description': description,
    }

    return render(request, 'input_query.html', context)

# This function do the same as the input_query, but now using the result of the query obtained
# It access to the user schema, and checks if different errors are happening while running the statements, 
# if those errors occur, the system will inform the user using pop-ups
# if not, it compare the result obtained with the one expected, and then render the ouput_query template with all the context information
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

    # executing the query in the database
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

    #read the information fromt he config.json file
    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']
            solution = i['solution']

    f.close()

    # In case the query result obtained have errors
    if flag == 1:
        if request.method == 'POST':
            form = QueryInputForm(request.POST)
        else:
            form = QueryInputForm()

        # Create the context with the information and render the template with it
        context = {
            'form': form,
            'stage': stage,
            'description': description,
        }
        return render(request, 'input_query.html', context)

    # No error case situation 
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

            # Create the context with the information and render the template with it
            context = {
                'form': form,
                'stage': stage,
                'description': description,
            }
            return render(request, 'input_query.html', context)

    # Create the context with the information and render the template with it
    context = {
        'query_result': query_result_parsed,
        'error_case': error_case
    }

    return render(request, 'output_query.html', context)

# This function is the one that shows a message with the hint that reads from the config.file for each stage
def show_hint(request):

    form = QueryInputForm()

    #read the information fromt he config.json file
    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']
            hint = i['hint']

    f.close()

    # Show the message with a pop-up
    success_alert_popup("Message", hint)

    # Create the context with the information and render the template with it
    context = {
        'form': form,
        'stage': stage,
        'description': description,
    }

    return render(request, 'input_query.html', context)

# Pop-up function for the errors
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

# Pop-up function for the succesful messages
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

# Function that creates a new schema of a new user that start a new game
def new_schema(request):

    # adding one to the global variables, context_request and
    add_global_context_request()
    add_global_user_var()

    #query to execute with the determined user
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

    # executing the query in the database
    with connection.cursor() as cursor:
        try:
            cursor.execute(raw)
        except (Exception, psycopg2.Error) as error:
            print("Error while creating new schema in the database", error) 

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed") 

    # Create the request with the form
    if request.method == 'POST':
        form = QueryInputForm(request.POST)

    else:
        form = QueryInputForm()

    #read the information fromt he config.json file
    f = open('static/config.json')
    data = json.load(f)

    for i in data['app_info']:
        if i['stage'] == str(global_context_request):
            stage = i['stage']
            description = i['description']


    f.close()
    
    # Create the context with the information and render the template with it
    context = {
        'form': form,
        'stage': stage,
        'description': description
    }

    return render(request, 'input_query.html', context)

#Function that deletes the schema of the user that exit the game
def delete_schema(request):

    # query to execute
    raw = """
        DROP SCHEMA IF EXISTS user"""+str(global_var)+""" CASCADE;
        """

    # executing the query in the database
    with connection.cursor() as cursor:
        try:
            cursor.execute(raw)
        except (Exception, psycopg2.Error) as error:
            print("Error while creating new schema in the database", error) 

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed") 
    
    # substract one to the global user variable and reset the stage global variable
    context = {}
    sub_global_user_var()
    reset_global_context_request()
    return render(request, 'base.html', context=context)