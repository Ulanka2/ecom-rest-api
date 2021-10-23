from django.urls import path
from applications.orders.views import OrderView, DetailOrderView

urlpatterns = [
    path('', OrderView.as_view()),
    path('<int:pk>/detail/', DetailOrderView.as_view()),
    # path('<int:id>/update',  TaskUpdateGenericView.as_view()),
    # path('<int:id>/destroy',  TaskDestroyGenericView.as_view()),

]