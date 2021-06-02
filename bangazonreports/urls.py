from django.urls import path
from .views import favseller_list

urlpatterns = [
    path('reports/userfavorites', favseller_list)
]