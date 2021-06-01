from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signin/newuser/', views.signin, name='newuser'),
    path('menu/<user_id>/', views.menu, name='menu'),
    path('menu/<user_id>/data/<str:station>/<str:name>/', views.check_data, name='indextag'),
    path('menu/<user_id>/data/<str:station>/<str:name>/<str:type_chart>', views.check_data, name='changechart'),
    path('menu/<user_id>/geolocation/<str:station>/<str:name>', views.check_location, name='location'),
    path('menu/<user_id>/subscribe/<str:station>/<str:name>', views.subscribe, name='subscribe'),
    path('menu/<user_id>/addparam/<str:station>', views.create_parameter, name='addparam'),
    path('menu/<user_id>/delete/station/<int:station_id>', views.delete_station, name='delstation'),
    path('menu/<user_id>/delete/parameter/<int:parameter_id>', views.delete_parameter, name='delstation'),
    path('menu/api/station/<int:station_id>/', views.api_station, name='serialstation'),
    path('menu/api/stations/', views.api_station, name='serialstationall'),
    path('menu/api/parameter/<int:parameter_id>/', views.api_parameter, name='serialparam'),
    path('menu/api/parameters/', views.api_parameter, name='serialparameterall'),
    path('menu/api/values/<int:parameter_id>/', views.api_values, name='serialvalues'),
    path('menu/api/users/', views.api_users, name='serialusersall'),
    path('menu/api/users/<int:user_id>/', views.api_users, name='serialuser')
]