from django.urls import path
from .views import *


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/', LoginView.as_view(), name='login'),
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('events/', EventViewSet.as_view({'get': 'list', 'post': 'create'}), name='event-list-create'),
    path('events/<int:event_id>/purchase/', TicketViewSet.as_view({'post': 'purchase'}), name='ticket-purchase'),

]
