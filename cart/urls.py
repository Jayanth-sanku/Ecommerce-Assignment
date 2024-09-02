from django.urls import path
from .views import cart_detail, cart_item_add, cart_item_update, cart_item_delete, cart_page

urlpatterns = [
    path('mycart/', cart_page, name='cart_page'),  
    path('detail/', cart_detail, name='cart_detail'),  
    path('add/', cart_item_add, name='cart_item_add'),  
    path('<int:pk>/update/', cart_item_update, name='cart_item_update'),  
    path('<int:pk>/delete/', cart_item_delete, name='cart_item_delete'), 
]
