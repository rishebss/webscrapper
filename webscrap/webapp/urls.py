from django.urls import path
from . import views
app_name='webapp'


urlpatterns = [
    path('', views.home, name='home'),
    path('scrapall/',views.scrapall,name='scrapall'),
    

]