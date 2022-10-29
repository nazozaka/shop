from django.urls import path
from . import views

# Для отображения фотографий
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page),
    path('products', views.get_all_products),
    path('product/<str:pk>', views.get_exact_product),
    path('category/<int:pk>', views.get_exact_category),
    path('search', views.search_exact_product),
    path('add_to_cart/<int:pk>', views.add_product_to_user_cart),
    path('user_cart', views.get_exact_user_cart),
    path('delete_product/<int:pk>', views.delete_exact_user_cart),
    path('checkout', views.sent_cart_by_bot),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#Добавить изображение


