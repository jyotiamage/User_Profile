from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user_profiles'
urlpatterns = [
	
	url(r'^login/$', views.login_view, name='login'),
	url(r'^signup/$', views.signup_view, name='signup'),
	url(r'^user_profile/(?P<username>[a-zA-Z0-9]+)/change_password$', views.changePassword_view, name='change_password'),
	url(r'^user_profile/(?P<username>[a-zA-Z0-9]+)/logout$', views.logout_view, name='logout'),
	url(r'^edit_profile/(?P<username>[a-zA-Z0-9]+)$', views.update_profile, name='edit_profile'),
	url(r'^user_profile/(?P<username>[a-zA-Z0-9]+)$', views.user_profile, name='view_profile'),
	url(r'^(?P<username>[a-zA-Z0-9]+)/home$', views.admin_view, name='home'),
]
