"""Modules Imported"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from .models import Article, ArticleSerializer, Newsletter, NewsletterSerializer


def create_resource_response(serializer, resource_name, request):
    """
    Helper function to add HATEOAS-style link to the created resource
    """
    data = serializer.data
    data['url'] = request.build_absolute_uri(
        reverse(f'news_app:api_{resource_name}_detail', args=[serializer.instance.id])
    )
    return data


# ---------------------- ARTICLES ----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_articles(request):
    """
    Retrieve all approved articles
    """
    articles = Article.objects.filter(approved=True)
    serializer = ArticleSerializer(articles, many=True)
    return Response({
        "count": articles.count(),
        "articles": serializer.data,
        "links": {
            "self": request.build_absolute_uri(),
            "create": request.build_absolute_uri(reverse('news_app:api_create_article'))
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_article(request):
    """
    Create a new article and associate it with the current journalist & publisher
    """
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            journalist=request.user.journalist,
            publisher=request.user.journalist.publisher
        )
        return Response(
            create_resource_response(serializer, 'article', request),
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Optional: single article view for HATEOAS links
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_article_detail(request, pk):
    """
    Retrieve a single article by ID
    """
    try:
        article = Article.objects.get(pk=pk, approved=True)
    except Article.DoesNotExist:
        return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ArticleSerializer(article)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------- NEWSLETTERS ----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_newsletters(request):
    """
    Retrieve all approved newsletters
    """
    newsletters = Newsletter.objects.filter(approved=True)
    serializer = NewsletterSerializer(newsletters, many=True)
    return Response({
        "count": newsletters.count(),
        "newsletters": serializer.data,
        "links": {
            "self": request.build_absolute_uri(),
            "create": request.build_absolute_uri(reverse('news_app:api_create_newsletter'))
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_newsletter(request):
    """
    Create a new newsletter and associate it with the current journalist & publisher
    """
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            journalist=request.user.journalist,
            publisher=request.user.journalist.publisher
        )
        return Response(
            create_resource_response(serializer, 'newsletter', request),
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Optional: single newsletter view for HATEOAS links
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_newsletter_detail(request, pk):
    """
    Retrieve a single newsletter by ID
    """
    try:
        newsletter = Newsletter.objects.get(pk=pk, approved=True)
    except Newsletter.DoesNotExist:
        return Response({"error": "Newsletter not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsletterSerializer(newsletter)
    return Response(serializer.data, status=status.HTTP_200_OK)
