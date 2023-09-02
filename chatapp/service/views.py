# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Service
from .serializer import ServiceSerializer


class ServiceListViewSet(viewsets.ViewSet):
    queryset = Service.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")

        if category:
            self.queryset = self.queryset.filter(category=category)
        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServiceSerializer(self.queryset, many=True)
        return Response(serializer.data)
