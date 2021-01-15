
from django.urls import path
from .views import myBlogView
urlpatterns = [
    path('myblog/',myBlogView,name='myblog'),
]