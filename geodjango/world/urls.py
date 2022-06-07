from django.urls import path

from . import views


urlpatterns = [
    
    #Optional, in order to let it run with just url: /world
    path('', views.home, name='home'),
    path('input_query/', views.input_query, name='input_query'),
    path('output_query/', views.output_query, name='output_query'),
    # path('second_stage_input_query/', views.second_stage_input_query, name='second_stage_input_query'),
    # path('second_stage_output_query/', views.second_stage_output_query, name='second_stage_output_query'),
    path('new_schema/', views.new_schema, name='new_schema'),
    path('delete_schema/', views.delete_schema, name='delete_schema'),
    path('show_hint/', views.show_hint, name='show_hint'),
    # path('second_stage_hint/', views.second_stage_hint, name='second_stage_hint'),    
    ]