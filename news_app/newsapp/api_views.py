"""Modules Imported"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import (Article,  ArticleSerializer,
                     Newsletter, NewsletterSerializer)


# List all approved articles
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_articles(request):
    """
    Article API view
    """
    articles = Article.objects.filter(approved=True)
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


# Create a new article
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_article(request):
    """
    Create Article API view
    """
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        # Assign the journalist automatically if needed
        serializer.save(journalist=request.user.journalist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all approved newsletters
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_newsletters(request):
    """
    Newsletter API view
    """
    newsletters = Newsletter.objects.filter(approved=True)
    serializer = NewsletterSerializer(newsletters, many=True)
    return Response(serializer.data)


# Create a new newsletter
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_newsletter(request):
    """
    Create Newsletter API view
    """
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(journalist=request.user.journalist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
