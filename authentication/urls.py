from django.urls import path, include
from knox import views as knox_views
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('change/password', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls',
                                    namespace='password_reset')),

    path('activate/email', views.activateView.as_view(),
         name='activate'),
]
