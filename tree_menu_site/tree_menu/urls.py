from django.urls import path
from tree_menu import views

urlpatterns = [
    path('', views.index, name='home'),
    path('menu/<path:menu_item_path>/', views.show_menu_item, name='menu_item'),
]

