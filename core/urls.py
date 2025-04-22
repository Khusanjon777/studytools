from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ProductListAPIView
from .views import create_order
from . import views

urlpatterns = [
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/create-order/', create_order, name="create_order"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

