from django.urls import path
from . import views  

urlpatterns = [
    path('', views.load_landing_page, name='load_landing_page'),
    path('dialog/',views.load_search_page, name='load_search_page'),
    path('chatbot/', views.chat_view, name='chatbot'),
    path('search/', views.load_search_page, name='load_search_page'), 
    path('search_symptoms/', views.search_symptoms, name='search_symptoms'),
    path('store_symptoms/', views.store_symptoms, name="store_symptoms"),
    path('get_conditions/', views.get_conditions, name='get_conditions'),
    path('show_categories/', views.show_categories, name='show_categories'),
    path('search_categories/', views.search_categories, name='search_categories'),
    path('get_answer/', views.get_answer_view, name='get_answer'),
]
