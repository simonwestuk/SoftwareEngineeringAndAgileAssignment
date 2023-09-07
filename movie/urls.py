from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/<int:id>', views.display, name='display'),
    path('<int:id>/reviews', include('review.urls'))
]