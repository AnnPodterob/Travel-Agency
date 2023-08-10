from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .forms import UserLoginForm
from .views import AddReviewView

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/login/', LoginView.as_view(authentication_form=UserLoginForm), name="login_url"),
    path('register/', views.register_view, name="register_url"),
    path('logout/', LogoutView.as_view(next_page='home'), name="logout"),
    path('package/', views.package_view, name="package"),
    path('flights/', views.flight_view, name="flights"),
    path('hotels/', views.hotel_view, name="hotels"),
    path('places/', views.places_view, name="places"),
    path('cancelflight/<str:flight>/<str:date>/<int:seat>', views.cancel_flight, name='CancelFlight'),
    path('concanflight/<str:flight>/<str:date>/<int:seat>', views.confirm_cancel_flight, name='ConfirmCancelFlight'),
    path('cancelhotel/<str:hotel>/<str:date>/<int:room>', views.cancel_hotel, name='CancelHotel'),
    path('concanhotel/<str:hotel>/<str:date>/<int:room>', views.confirm_cancel_hotel, name='ConfirmCancelHotel'),
    path('cancelpackage/<str:flight>/<int:seat>/<str:hotel>/<str:date>/<int:room>', views.cancel_package,
         name='CancelPackage'),
    path('concanpackage/<str:flight>/<int:seat>/<str:hotel>/<str:date>/<int:room>', views.confirm_cancel_package,
         name='ConfirmCancelPackage'),
    path('bookflight/<str:flight_number>/<str:date>', views.book_flight, name="bookflight"),
    path('userflight/<str:flight_number>/<str:date>/<int:seat>', views.submit_flight, name='userflight'),
    path('bookhotel/<str:hotel>/<str:date>', views.hotel_book, name="bookhotel"),
    path('userhotel/<str:hotel>/<str:date>/<int:room>', views.hotel_submit, name='userhotel'),
    path('bookpackage/<str:source>/<str:destination>/<str:date>', views.package_book, name="bookpackage"),
    path('userpackage/<str:flight>/<str:hotel>/<str:date>/<int:room>/<int:seat>', views.submit_package,
         name='userpackage'),
    path('accounts/profile/', views.dashboard, name='dashboard'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('hotel/<int:pk>/review/', AddReviewView.as_view(), name='add_review'),
]

urlpatterns += staticfiles_urlpatterns()

