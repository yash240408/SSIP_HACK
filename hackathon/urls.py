from django import urls
from django.urls import path
from . import views

urlpatterns=[
    path('',views.login,name='index.html'),
    path('dashboard', views.admin_dashboard, name='dashboard.html'),
    path('add', views.admin_add, name='form-basic.html'),
    path('admin_add', views.admin_add, name='form-basic.html'),
    path('profile', views.admin_profile, name='profile.html'),
    path('fprofile', views.farmer_profile, name='farmer_profile.html'), #farmer
    path('map', views.admin_map, name='sitemap.html'),
    path('login', views.login),
    path('logout', views.logout,name='logout.html'),

    path('water', views.admin_water,name='Water_Level.html'),
    path('obstacle', views.admin_obstacle,name='Obstacle_Detection.html'),
    path('height', views.admin_height,name='Height_Measure.html'),
    path('moisture', views.admin_moisture,name='Moisture_Level.html'),
    path('temp', views.admin_temp,name='Temp_Hum.html'),

    path('warning', views.admin_warning,name='datatable.html'),
    path('fdashboard', views.farmer_dash,name='farmer_dash.html'), #farmer
    path('status', views.admin_status,name='form-wizard.html'),
    path('farmer_logout', views.farmer_logout,name='farmer_logout.html'), #farmer
    path('addcomplain', views.farmer_complain,name='farmer_form-wizard.html'), #farmer
]