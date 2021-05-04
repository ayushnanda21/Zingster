from django.urls import path
from landing.views import Index
from .import views

urlpatterns = [
    path("",views.Index.as_view(),name="index"),
]
