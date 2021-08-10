from django.urls import path, include
from . import views
from . import SuperAdminView

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('problem/', views.problem, name="problem"),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', SuperAdminView.admin_home, name="admin_home"),
    path('manage_members/', SuperAdminView.manage_members, name="manage_members"),
    path('superadmin_profile/', SuperAdminView.superadmin_profile, name="superadmin_profile"),
    path('add_sacco_admin/', SuperAdminView.add_sacco_admin, name="add_sacco_admin"),
    path('add_sacco_admin_save/', SuperAdminView.add_sacco_admin_save, name="add_sacco_admin_save"),
    path('manage_sacco_admin/', SuperAdminView.manage_sacco_admin, name="manage_sacco_admin"),
    path('add_sacco/', SuperAdminView.add_sacco, name="add_sacco"),
    path('edit_sacco_save/', SuperAdminView.edit_sacco_save, name="edit_sacco_save"),
    path('add_sacco_save/', SuperAdminView.add_sacco_save, name="add_sacco_save"),
    path('manage_saccos/', SuperAdminView.manage_saccos, name="manage_saccos"),
    path('add_member/', SuperAdminView.add_member, name="add_member"),
    path('edit_sacco_admin/<sacco_admin_id>/', SuperAdminView.edit_sacco_admin, name="edit_sacco_admin"),
    path('superadmin_profile_update/', SuperAdminView.superadmin_profile_update, name="superadmin_profile_update"),
    path('check_email_exist/', SuperAdminView.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', SuperAdminView.check_username_exist, name="check_username_exist"),
]
