__author__ = 'berluskuni'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout_out, name='logout'),
    url(r'^login/', views.login_in, name='login'),
    url(r'^reset_password/', views.ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^guest/', views.account_reg_or_guest, name='guest_or_register'),
    url(r'^profile_update/', views.profile_update, name='profile_update'),



]
