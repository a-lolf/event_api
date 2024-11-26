from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User, Event, Ticket
from .serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView


# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class MyTokenObtainPairView(TokenObtainPairView):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def create(self, request, *args, **kwargs):
        print(request.user.role)
        if request.user.role != 'ADMIN':
            return Response({'error':' Only Admins can create events'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
    

class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=True, methods=['post'])
    def purchase(self, request, event_id):
        # import ipdb; ipdb.set_trace()

        event = Event.objects.get(pk=event_id)
        role = request.user.role
        quantity = request.data.get('quantity')

        if role == 'ADMIN':
            return Response({'error': 'Admin cannot purchase'}, status=status.HTTP_400_BAD_REQUEST)
        
        if (event.total_tickets - event.tickets_sold) < int(quantity):
            return Response({'error': 'Tickets not available'}, status=status.HTTP_400_BAD_REQUEST)

        Ticket.objects.create(
            user=request.user,
            event=event,
            quantity=int(quantity)
        )
        event.tickets_sold += int(quantity)
        event.save()

        return Response({'message': 'Ticket purchased successfully!'}, status=status.HTTP_201_CREATED)