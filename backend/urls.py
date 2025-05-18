from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('index/',views.index,name = 'index'),
    path('index/customer/', views.customer, name='customer'),
    path('index/client/', views.client, name='customer'),
    path('index/employee/', views.employee, name='customer'),
    path('customer/', views.customer, name='customer'),
    path('login-or-create-account/', views.login_or_create_account, name='login_or_create_account'),
    path('login/', views.login, name='login'),
    path('account_creation/', views.account_creation, name='account_creation'),
    path('success/', views.success, name='success'),
    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.today_orders, name='orders'),
    path('customer_history/', views.customer_history, name='customer_history'),
    path('client/',views.client,name = 'client'),
    path('create_account/', views.create_account, name='create_account'),
    path('client_login/',views.client_login,name = 'client_login'),
    path('client_create_account/',views.client_create_account,name = 'client_create_account'),
    path('employee/',views.employee,name = 'employee' ),
    path('track_order/',views.track_order,name = 'track_order'),
    path('customer_dashboard/',views.customer_dashboard,name = 'customer_dashboard'),
    path('client_dashboard/',views.client_dashboard,name = 'client_dashboard'),
    path('date_order/<int:year>/<int:month>/<int:day>/', views.date_order, name='date_order'),
    path('update_status/',views.update_status,name = 'update_status'),
    path('get_routes/', views.get_routes, name='get_routes'),
    
    # ...

    
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)