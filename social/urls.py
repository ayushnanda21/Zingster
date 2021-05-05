from django.urls import path
from .views import PostListView
from .import views

urlpatterns = [
    path("", views.PostListView.as_view(),name='post-list'),
]
