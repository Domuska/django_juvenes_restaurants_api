from rest_framework import generics
from menus.serializers import TodoSerializer
from menus.models import Menus


class Menu(generics.ListCreateAPIView):
    queryset = Menus.objects.all()
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        print("saving a new menu item")
        serializer.save()
