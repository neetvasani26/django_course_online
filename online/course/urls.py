from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course_details_bootstrap/<int:id>/', views.course_details_bootstraps, name='course_details_bootstrap'),

    # ✅ Required route 1
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # ✅ Required route 2
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]