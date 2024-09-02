from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from payments.views import payment_success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),  
    path('api/catalog/', include('catalog.urls')),  
    path('api/orders/', include('orders.urls')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('authentication.urls', namespace='authentication')),  
    path('adminapp/', include('adminapp.urls')),  
    path('api/cart/', include('cart.urls')),  
    path('payments/', include('payments.urls')),
    path('payment-success/', payment_success, name='payment_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
