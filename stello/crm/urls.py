from django.urls import path
from . import views
app_name = 'crm'
urlpatterns = [
    # Сайт клиента
    path('order/', views.OrderView.as_view(), name='index'),
]
