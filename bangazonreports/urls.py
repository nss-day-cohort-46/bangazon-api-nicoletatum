from django.urls import path
from .views import favseller_list, unpaidorders_list, paidorders_list

urlpatterns = [
    path('reports/userfavorites', favseller_list),
    path('reports/unpaidorders', unpaidorders_list),
    path('reports/paidorders', paidorders_list)
]