from django.urls import path, include
from .views import (
    PNRStatusApiView,
)

urlpatterns = [
    path('<str:pnr_number>', PNRStatusApiView.as_view()),
]