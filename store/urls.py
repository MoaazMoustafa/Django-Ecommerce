from django.urls import path
from . import views
app_name = 'store'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('item/<slug:slug>/', views.product_details, name='prduct_details'),
    path('category/<slug:slug>/', views.category_list, name='category_details'),
]
