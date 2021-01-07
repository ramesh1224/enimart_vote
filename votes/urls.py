
from django.urls import path
from . import views

app_name = 'votes'
urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('', views.login_in, name='login'),
    path('logout/', views.logout_out, name='logout'),
    path('regions/', views.all_regions, name='allregions'),
    path('regions/<int:region_id>/', views.details, name='details'),
    path('regions/<int:region_id>/votes/', views.vote, name='vote'),
]
