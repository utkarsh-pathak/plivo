from django.urls import path

from . import views

urlpatterns = [
    path('/', views.ContactBookCRUD.as_view()),
    path('/<int:id>/', views.ContactBookCRUD.as_view()),
    path('/search/', views.SearchByParams.as_view()),
]