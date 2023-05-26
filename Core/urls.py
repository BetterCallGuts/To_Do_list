from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.HomePage, name='HomePage'),
    path('login/', views.Login, name='Login'),
    path('Signup/', views.Signup, name='Signup'),
    path('AddATask/', views.Add_A_Task, name="AddATask"),
    path('Logout/', views.Logout, name="Logout"),
    path('delete/<int:pk>', views.delete, name="delete"),
    path('Edit/<int:pk>', views.Edit, name="Edit"),
]
