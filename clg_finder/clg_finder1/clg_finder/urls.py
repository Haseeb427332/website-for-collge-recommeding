"""clg_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import views
from .import urls 
import users.urls
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
#app_name = "clg_finder"
#from .views import redirect_root

urlpatterns = [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='commons/password-reset/password_reset.html',
             subject_template_name='commons/password-reset/password_reset_subject.txt',
             email_template_name='commons/password-reset/password_reset_email.html',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    url(r'^signup/$', views.signup, name='signup'),
    #url(r'^login/$', auth_views.LoginView, name='login'),
    url( r'^login/$',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView, name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('admin_panel/deleted/',views.ajax_view_delete.as_view(), name="ajax_view_delete"),
    path('profileUpdate/',views.profileUpdate,name="crud_profile_update"),
    path("add_to fav/",views.addTo_fav,name = 'addTo_fav'),
    path("admin_panel/",views.admin_panel,name = 'admin_panel'),
    url(r'^password/$', views.change_password, name='change_password'),
    path('admin_panel/view_info/',views.view_info.as_view(),name="ajax_view"),
    path('admin_panel/Auth/',views.Auth_ajax_view.as_view(), name="Auth_ajax_view"),
    # path('admin_panel/view_info/',views.view_info.as_view(),name="ajax_view"),
    path('admin_panel/AuthDel/',views.Auth_ajax_view_delete.as_view(), name="Auth_ajax_view_delete"),
    path('admin_panel/newAdmin/',views.ajax_adminReg.as_view(), name="ajax_newAdmin"),
    path('profile/',users.views.edit_profile, name='profile'),
    path('admin/', admin.site.urls),
    path('detailpage/',users.views.detailpage,name='detailpage'),
    #path('detailpage/<clg_id>/',users.views.detailpage,name='detailpage'),
    path('detailpage/<value>/<clg_id>/',users.views.detailpage,name='detailpage'),
    path('clg_infoUpdate/',views.clg_infoUpdate,name = "clg_infoUpdate"),
    #path('ext/',views.i,name='i')
    path('hp/',views.hp,name='hp'),
    path('users/',include('users.urls')),
    url(r'^validate_username/$', views.validate_username, name='validate_username'),
    path('',views.index,name='index'),
    path(r'xl_upload/',views.xl_upload,name='simple_upload'),
    #path(r'xl_submission/',views.xl,name='xl'),
    path(r'form_submission/',views.form_submission,name='form_submission'),
    path(r'authentication/',views.authentication,name='authentication'),
    path('search/',views.search,name="search"),
    path('clg_finder/end/',views.end,name='end'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)