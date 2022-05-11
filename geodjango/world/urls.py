from django.urls import path

from . import views


urlpatterns = [
    
    #Optional, in order to let it run with just url: /world
    path('', views.home, name='home'),
    path('input_query/', views.input_query, name='input_query'),
    path('output_query/', views.output_query, name='output_query'),
    path('new_schema/', views.new_schema, name='new_schema'),
    path('delete_schema/', views.delete_schema, name='delete_schema'),
    
    ]