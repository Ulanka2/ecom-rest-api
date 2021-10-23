from django.urls import path
from applications.accounts.views import RegistrationAPIView

urlpatterns = [
    path('', RegistrationAPIView.as_view())

]