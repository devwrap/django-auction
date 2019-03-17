from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', views.UserView)
router.register('item', views.ItemView)
router.register('bids', views.BidView)

urlpatterns = [
    path('', include(router.urls))
]

# for url in router.urls:
#     print(url)
