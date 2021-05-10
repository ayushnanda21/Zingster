from django.urls import path
from landing.views import Index
from .import views
from landing.views import Contact

urlpatterns = [
    path("",views.Index.as_view(),name="index"),
    path("contact/",views.Contact,name="contact"),
]
