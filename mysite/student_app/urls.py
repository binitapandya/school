
from django.urls import path, re_path
from . import views 
urlpatterns = [
    path('registrat/', views.UserRegistrationView.as_view(), name='registrat'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('teacher/<int:pk>/', views.TeacherView.as_view(), name='teacher'),
    path('student/<int:pk>/', views.StudentView.as_view(), name='student'),
    path('marks/', views.MarksCreate.as_view(), name='marks'),
    path('marks/<int:pk>', views.MarksCreate.as_view(), name="marks/pk")
]