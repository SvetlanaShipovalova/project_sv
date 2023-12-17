
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from myProject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info, name="info"),
    path('', views.show_index, name="home"),
    path('showCustomer/<int:id_user>/addOrder/', views.create_order, name = "create_order"),
    path('showCustomer/<int:id_user>/', views.show_customer),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy("home")), name="logout"),
    path('user_logout', views.logout_user, name="logout_user"),
    path("providerView/<int:id_user>/",views.show_CustomerFromProvider,name = "Customers"),
    path("providerView/<int:id_user>/<int:order_id>/deleteOrder", views.delete_order, name="delete_order"),


    path('ajax/validate_username', views.validate_username, name='validate_username'),
    path('ajax/validate_email', views.validate_email, name='validate_email'),
    path('ajax/check_order_number/<int:id_customer>/', views.check_numberOrder, name='check_order_number'),

]
