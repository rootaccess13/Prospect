from django.shortcuts import render
from . import serializers
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets
# import csrf_exempt
from django.views.decorators.csrf import csrf_exempt


class CreateReview(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.ReviewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
