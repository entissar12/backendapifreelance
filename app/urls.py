from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'resettoken', TokenViewSet)
