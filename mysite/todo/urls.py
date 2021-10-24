from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('delete/<int:id>', views.deletetask, name="delete"),

    path('deletetask/<int:id>', views.deleteconfirm, name="deletetask"),


    path('add_task', views.add_task, name="add_task"),
    path('search', views.search, name="search"),

    # authentication
    path('login', views.loginuser, name="login"),
    path('logout', views.logoutuser, name="logout"),
    path('register', views.register, name="register"),

]