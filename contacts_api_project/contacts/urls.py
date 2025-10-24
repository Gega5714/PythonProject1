from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

router = DefaultRouter()
# Register the viewset at the root of this included URLconf so the final
# paths become /contacts/ (list/create) and /contacts/{pk}/ (detail).
router.register(r'', ContactViewSet, basename='contact')

urlpatterns = router.urls