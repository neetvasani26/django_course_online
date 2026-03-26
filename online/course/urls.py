from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course_details_bootstrap/<int:id>/', views.course_details_bootstraps, name='course_details_bootstrap'),
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_result'),
]