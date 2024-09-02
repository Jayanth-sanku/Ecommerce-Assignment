from django.urls import path
from . import views
from .views import custom_logout

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('edit-product/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('delete-product/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
    path('view-order/<int:order_id>/', views.admin_view_order, name='admin_view_order'),
    path('admin/product/add/', views.admin_add_product, name='admin_add_product'),
    path('logout/', custom_logout, name='logout'),
]
