from django.conf import settings
from django.conf.urls.static import static
from django.urls import path  # Make sure this line is present
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('croptypes/', views.crop_type_list, name='crop_type_list'),
    path('croptypes/<int:crop_id>/', views.crop_type_detail, name='crop_type_detail'),
    path('farmer-crops/', views.farmer_crop_list, name='farmer_crop_list'),
    path('farmer-crops/<int:crop_id>/', views.farmer_crop_detail, name='farmer_crop_detail'),
    path('croptypes/<int:crop_type_id>/crops/', views.crops_by_type, name='crops_by_type'),
    path('market-price/', views.market_price, name='market_price'),
    path('calendar/', views.crop_calendar_view, name='crop_calendar'),
    path('calendar/events/', views.crop_events, name='crop_events'),
    path('submit-crop', views.submit_crop_entry, name='crop_entry'),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
