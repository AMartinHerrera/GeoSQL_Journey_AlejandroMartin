from django.urls import path

from . import views


urlpatterns = [
    
    #Optional, in order to let it run with just url: /world
    path('', views.home, name='home'),
    path('first_stage_input_query/', views.first_stage_input_query, name='first_stage_input_query'),
    path('first_stage_output_query/', views.first_stage_output_query, name='first_stage_output_query'),
    path('second_stage_input_query/', views.second_stage_input_query, name='second_stage_input_query'),
    path('second_stage_output_query/', views.second_stage_output_query, name='second_stage_output_query'),
    path('new_schema/', views.new_schema, name='new_schema'),
    path('delete_schema/', views.delete_schema, name='delete_schema'),
    
    ]