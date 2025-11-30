'''Imported Modules'''
import secrets
from datetime import datetime, timedelta
from hashlib import sha1
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import (
    User, Reader,
    Publisher, PublisherSerializer,
    Journalist, JournalistSerializer,
    Editor, EditorSerializer,
    Article, ArticleSerializer,
    Newsletter, NewsletterSerializer,
    Subscription, SubscriptionSerializer, ResetToken
)
from .functions.twitter_api import Tweet


def verify_username(username):
    """
    Username validation
    """
    return username


def verify_password(password):
    """
    Password validation
    """
    try:
        validate_password(password)
        return True
    except ValidationError:
        print("Issue with passowrd")
        return False


def welcome(request):
    """
    Function that displays the first view to logged user
    """
    return render(request, 'newsapp/welcome.html')


def register_user(request):
    """
    Register a new publisher in the system.

    This function handles POST requests to create a new Publisher object
    linked to a User, validates input, and returns a success message.

    Args:
        request (HttpRequest)

    Returns:
        HttpResponse
    """

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not verify_username(username):
            messages.error(request, "Invalid username.")
            return render(request, 'newsapp/register.html')

        if not verify_password(password):
            messages.error(request, "Password does not meet requirements.")
            return render(request, 'newsapp/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'newsapp/register.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        messages.success(request, "Account created. Please choose your role.")
        return redirect('news_app:choose_group')

    return render(request, 'newsapp/register.html')


@login_required
def choose_group(request):
    """
    Select a user group on the app.

    This function handles POST requests to select the group
    under which the user will be logged in

    Args:
        request (HttpRequest)

    Returns:
        HttpResponse
    """
    user = request.user

    if request.method == 'POST':
        selected_role = request.POST.get('role')

        if selected_role == 'reader':
            Reader.objects.get_or_create(user=user)
            reader_group = Group.objects.get(name='Reader')
            user.groups.add(reader_group)
            messages.success(request, "Registered as Reader.")
            return redirect('news_app:home')

        elif selected_role == 'journalist':
            journalist_group = Group.objects.get(name='Journalist')
            user.groups.add(journalist_group)
            request.session['pending_role'] = 'journalist'
            messages.info(request, "Please select a publisher to register as a Journalist.")
            return redirect('news_app:register_under_publisher')

        elif selected_role == 'editor':
            editor_group = Group.objects.get(name='Editor')
            user.groups.add(editor_group)
            user = User.objects.get(id=user.id)
            request.session['pending_role'] = 'editor'
            messages.info(request, "Please choose your publishing house to complete registration.")
            return redirect('news_app:register_under_publisher')

        elif selected_role == 'publisher':
            publisher_group = Group.objects.get(name='Publisher')
            user.groups.add(publisher_group)
            Publisher.objects.get_or_create(user=user)
            messages.success(request, "Registered as Publisher.")
            return redirect('news_app:home')
        else:
            messages.error(request, "Invalid selection.")
            return redirect('news_app:welcome')

    return render(request, 'newsapp/choose_group.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session.set_expiry(3600)
            roles = []
            if hasattr(user, 'reader'):
                roles.append('reader')
            if hasattr(user, 'journalist'):
                roles.append('journalist')
            if hasattr(user, 'editor'):
                roles.append('editor')
            if hasattr(user, 'publisher'):
                roles.append('publisher')

            request.session['roles'] = roles

            if request.headers.get("Accept") == "application/json":
                return JsonResponse({'message': 'Login successful', 'roles': roles})
            return HttpResponseRedirect(reverse('news_app:home'))

        # invalid credentials
        if request.headers.get("Accept") == "application/json":
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        return render(request, 'newsapp/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'newsapp/login.html')


def logout_user(request):
    """
    Allows user to logout and return to welcome page

    Args:
        request

    Returns:
        HttpResponse
    """
    logout(request)
    return redirect('news_app:welcome')


@login_required
def home(request):
    user = request.user
    context = {"options": []}

    if user.groups.filter(name='Publisher').exists():
        context['group'] = 'Publisher'
        context['options'] = [
            {"label": "Create Article", "url_name": "news_app:create_post"},
            {"label": "View Submissions", "url_name": "news_app:view_mine"},
            {"label": "Manage Team", "url_name": "news_app:register_under_publisher"},
        ]

    elif user.groups.filter(name='Journalist').exists():
        context['group'] = 'Journalist'
        context['options'] = [
            {"label": "Write Article", "url_name": "news_app:create_post"},
            {"label": "View All Articles", "url_name": "news_app:article_list"},
            {'label': 'View My Articles', 'url_name': 'news_app:view_mine'},
            {"label": "Join Publisher", "url_name": "news_app:register_under_publisher"},
        ]

    elif user.groups.filter(name='Editor').exists():
        context['group'] = 'Editor'
        context['options'] = [
            {"label": "View All Articles", "url_name": "news_app:article_list"},
            {'label': 'Edit/Delete Articles', 'url_name': 'news_app:view_mine'},
            {"label": "Join Publisher", "url_name": "news_app:register_under_publisher"},
        ]

    elif user.groups.filter(name='Reader').exists():
        context['group'] = 'Reader'
        context['options'] = [
            {"label": "Read All Articles", "url_name": "news_app:article_list"},
            {"label": "Subscribe", "url_name": "news_app:subscribe"},
        ]

    else:
        messages.info(request, "Please select a role to continue.")
        return redirect('news_app:choose_group')

    return render(request, 'newsapp/home.html', context)


@login_required
# @permission_required('newsapp.join_publisher', raise_exception=True)
def register_under_publisher(request):
    user = request.user
    pending_role = request.session.get('pending_role')

    # Allow access if user is already a journalist or editor
    if pending_role not in ['journalist', 'editor']:
        if hasattr(user, 'journalist'):
            request.session['pending_role'] = 'journalist'
            pending_role = 'journalist'
        elif hasattr(user, 'editor'):
            request.session['pending_role'] = 'editor'
            pending_role = 'editor'
        else:
            messages.error(request, 'You must choose a role first.')
            return redirect('news_app:choose_group')

    if request.method == 'POST':
        publisher_id = request.POST.get('publisher_id')
        publisher = get_object_or_404(Publisher, id=publisher_id)

        if pending_role == "journalist":
            journalist, created = Journalist.objects.get_or_create(user=user)
            journalist.publisher = publisher
            journalist.save()
            role = "journalist"

        elif pending_role == "editor":
            editor, created = Editor.objects.get_or_create(user=user)
            editor.publisher = publisher
            editor.save()
            role = "editor"

        messages.success(request, f"{role.title()} successfully registered under {publisher.user.username}.")
        return render(request, 'newsapp/registered_for_publisher.html', {
            'role': role,
            'publisher': publisher
        })

    publishers = Publisher.objects.all()
    return render(request, 'newsapp/register_under_publisher.html', {'publishers': publishers})


@login_required
def subscribe(request):
    user = request.user

    # Get lists for the dropdowns
    publishers = Publisher.objects.all()
    journalists = Journalist.objects.all()

    if request.method == 'POST':
        publisher_id = request.POST.get('publisher_id')
        journalist_id = request.POST.get('journalist_id')
        subscriptions = []

        # Subscribe to Publisher
        if publisher_id:
            publisher = get_object_or_404(Publisher, id=publisher_id)
            # Prevent duplicate subscription
            sub, created = Subscription.objects.get_or_create(
                user=user, type='publisher', publisher=publisher
            )
            if created:
                subscriptions.append(sub)

        # Subscribe to Journalist
        if journalist_id:
            journalist = get_object_or_404(Journalist, id=journalist_id)
            sub, created = Subscription.objects.get_or_create(
                user=user, type='journalist', journalist=journalist
            )
            if created:
                subscriptions.append(sub)

        if publisher_id or journalist_id:
            messages.success(request, "Subscribed successfully!")
            return redirect('news_app:subscribed_articles')

        else:
            messages.error(request, "Please select at least one publisher or journalist you want to subscribe to.")

    return render(request, 'newsapp/subscribe.html', {
        'journalists': journalists,
        'publishers': publishers
    })


def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    newsletters = Newsletter.objects.all().order_by('-created_at')

    return render(request, 'newsapp/article_list.html',
                  {"articles": articles,
                   "newsletters": newsletters})


# @permission_required('newsapp.can_view')
def view_mine(request):
    user = request.user

    # Journalists: only their articles
    if hasattr(user, 'journalist'):
        articles = Article.objects.filter(journalist=user.journalist)

    # Editors: only articles under their publisher
    elif hasattr(user, 'editor'):
        articles = Article.objects.filter(journalist__publisher=user.editor.publisher)

    # Publishers: only articles submitted to their house
    elif hasattr(user, 'publisher'):
        articles = Article.objects.filter(journalist__publisher=user.publisher)

    else:
        articles = Article.objects.none()

    return render(request, 'newsapp/article_list.html', {
        'articles': articles,
        'mine_view': True
    })


def subscribed_articles(request):
    """
    Show subscription success and the publishers/journalists
    the user is subscribed to.
    """

    user = request.user
    subscriptions = Subscription.objects.filter(user=user)

    # publishers = [sub.publisher for sub in subscriptions if sub.publisher]
    # journalists = [sub.journalist for sub in subscriptions if sub.journalist]

    return render(request, 'newsapp/subscribed.html', {
        'subscriptions': subscriptions
    })


def read_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    serializer = ArticleSerializer(article)
    if request.headers.get("Accept") == "application/json":
        return JsonResponse(serializer.data, safe=False)
    return render(request, 'newsapp/read_article.html', {'article': article})


def view_article(request, article_id):
    """
    Docstring for view_article

    :param request: Description
    :param article_id: Description
    """
    user = request.user
    article = get_object_or_404(Article, id=article_id)

    role = None
    if hasattr(user, 'publisher'):
        role = "publisher"
    elif hasattr(user, 'editor'):
        role = "editor"
    elif hasattr(user, 'journalist'):
        role = "journalist"

    serializer = ArticleSerializer(article)
    if request.headers.get("Accept") == "application/json":
        return JsonResponse(serializer.data, safe=False)

    return render(request, 'newsapp/article_list.html',
                  {'article': article,
                   'role': role})


# @login_required
# @permission_required('newsapp.can_create', raise_exception=True)
def create_post(request):
    user = request.user
    publishers = Publisher.objects.all()

    if not hasattr(user, 'journalist'):
        messages.error(request, "Only journalists can create posts.")
        return redirect('news_app:home')

    journalist = user.journalist

    if request.method == 'POST':
        post_type = request.POST.get('post_type')  # article or newsletter
        title = request.POST.get('title')
        content = request.POST.get('content')
        publisher_id = request.POST.get('publisher_id')
        publisher = get_object_or_404(Publisher, id=publisher_id)

        if post_type == 'article':
            post = Article.objects.create(title=title, content=content, journalist=journalist, publisher=publisher, approved=False)
            serializer = ArticleSerializer(post)
        elif post_type == 'newsletter':
            post = Newsletter.objects.create(title=title, content=content, journalist=journalist, publisher=publisher, approved=False)
            serializer = NewsletterSerializer(post)
        else:
            return JsonResponse({'error': 'Invalid post type'}, status=400)

        if request.headers.get("Accept") == "application/json":
            return JsonResponse({'message': 'Post created successfully', 'data': serializer.data}, status=201)

        messages.success(request, f'{post_type.title()} "{title}" posted under {publisher.user.username}.')

        # optional tweet
        try:
            post_tweet = f"New Post by {journalist.user.username}: {post.title}"
            tweet = Tweet()
            tweet.make_tweet({'text': post_tweet})
        except Exception:
            pass

        return redirect('news_app:home')

    return render(request, 'newsapp/create_post.html', {'publishers': publishers})


@login_required
# @permission_required('newsapp.can_update', raise_exception=True)
def update_post(request, post_id):
    post = get_object_or_404(Article, id=post_id)

    if request.user != post.journalist.user and not hasattr(request.user, 'editor'):
        messages.error(request, "You don't have permission to update this post.")
        return redirect('news_app:home')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title:
            post.title = title
        if content:
            post.content = content
        post.save()

        if hasattr(request.user, 'journalist'):
            return redirect('news_app:view_mine')

        messages.success(request, f'Article "{post.title}" updated successfully.')

        if request.headers.get("Accept") == "application/json":
            return JsonResponse({
                'message': 'Post updated',
                'data': ArticleSerializer(post).data
            })

    return render(request, 'newsapp/update_post.html', {'post': post})


# @permission_required('newsapp.can_remove')
def remove_post(request, post_id):
    # Try to get the post from Article or Newsletter
    post = Article.objects.filter(id=post_id).first()
    post_type = 'article'
    if not post:
        post = Newsletter.objects.filter(id=post_id).first()
        post_type = 'newsletter'

    if not post:
        messages.error(request, "No post found with that ID.")
        return redirect('news_app:article_list')

    if request.method == 'POST':
        # Only owner, editor, or publisher can delete
        if hasattr(request.user, 'journalist') and getattr(post, 'journalist', None) and post.journalist.user != request.user:
            if not hasattr(request.user, 'editors') and not hasattr(request.user, 'publisher'):
                messages.error(request, "You don't have permission to remove this post.")
                return redirect('news_app:home')

        post.delete()
        messages.success(request, f'{post_type.title()} removed successfully.')

        # Redirect based on role
        if hasattr(request.user, 'journalist'):
            return redirect('news_app:view_mine')
        return redirect('news_app:article_list')

    return render(request, 'newsapp/remove_post.html', {'post': post})


@login_required
def publish_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    post_type = request.POST.get('post_type')
    post_id = request.POST.get('post_id')

    # check user is a publisher
    if not hasattr(request.user, 'publisher'):
        return JsonResponse({'error': 'User is not a publisher.'}, status=403)
    publisher = request.user.publisher

    if post_type == 'article':
        article = get_object_or_404(Article, id=post_id)
        article.approved = True
        article.save()

        if request.headers.get("Accept") == "application/json":
            return JsonResponse({'message': 'Article published', 'article': ArticleSerializer(article).data})
        messages.success(request, f'Article "{article.title}" published.')
        return render(request, 'newsapp/read_article.html', {'article': article})

    elif post_type == 'newsletter':
        newsletter = get_object_or_404(Newsletter, id=post_id)
        newsletter.approved = True
        newsletter.save()
        if request.headers.get("Accept") == "application/json":
            return JsonResponse({'message': 'Newsletter published', 'newsletter': NewsletterSerializer(newsletter).data})
        messages.success(request, f'Newsletter "{newsletter.title}" published.')
        return render(request, 'newsapp/read_article.html', {'article': newsletter})

    return JsonResponse({'error': 'Invalid post type.'}, status=400)


# Password reset handling
def build_email(user, reset_link):
    subject = "Reset Password Request"
    body = (
        f"Hi {user.username},\n\n"
        f"Use the link below to reset your password:\n\n"
        f"{reset_link}\n\n"
        "If you didn't request this, ignore this email."
    )
    return EmailMessage(
        subject=subject,
        body=body,
        from_email='newsappreset@gmail.com',
        to=[user.email],
    )


def reset_url(user):
    domain = "http://127.0.0.1:8000/"
    app_path = "reset-password/update/"
    token = secrets.token_urlsafe(24)
    hashed = sha1(token.encode()).hexdigest()
    expiry_date = datetime.now() + timedelta(minutes=30)
    ResetToken.objects.create(user=user, token=hashed, expiry_date=expiry_date)
    return f"{domain}{app_path}?token={token}"


def send_password_reset_page(request):
    """
    Display form to enter email for password reset.
    """
    return render(request, 'newsapp/send_password_reset.html')


def send_password_reset(request):
    if request.method != 'POST':
        messages.error(request, "Please submit your email to reset password.")
        return redirect('news_app:send_password_reset_page')

    user_email = request.POST.get('email')
    try:
        user = get_object_or_404(User, email=user_email)
    except User.DoesNotExist:
        messages.success(request, "If that email exists, a reset link has been sent.")
        return HttpResponseRedirect(reverse('news_app:reset_password'))

    url = reset_url(user)
    email = build_email(user, url)
    email.send(fail_silently=False)
    messages.success(request, "If that email exists, a reset link has been sent.")
    return render(request, 'newsapp/email_success.html')


def token_request(request, token):
    hashed = sha1(token.encode()).hexdigest()
    try:
        user_token = ResetToken.objects.get(token=hashed, used=False)
    except ResetToken.DoesNotExist:
        user_token = None

    # if token exists but expired, show message
    if user_token and user_token.expiry_date < datetime.now():
        messages.error(request, "Token expired.")
        return redirect('news_app:send_password_reset')

    return render(request, 'newsapp/password_reset.html', {'token': token if user_token else None})


def reset_password(request):
    if request.method == 'GET':
        # Get token from query params
        token = request.GET.get('token')
        if not token:
            messages.error(request, "Invalid or missing token.")
            return redirect('news_app:login')

        # Render form with token in hidden input
        return render(request, 'newsapp/password_reset.html', {'token': token})

    # POST request: update password
    token = request.POST.get('token')
    password = request.POST.get('password')
    password_conf = request.POST.get('password_conf')

    if not token:
        messages.error(request, "Token missing. Cannot reset password.")
        return redirect('news_app:login')

    if password != password_conf:
        messages.error(request, "Passwords do not match.")
        # Redirect to same form with token in query string
        return redirect(f"{reverse('news_app:reset_password')}?token={token}")

    hashed = sha1(token.encode()).hexdigest()
    try:
        user_token = ResetToken.objects.get(token=hashed, used=False)
    except ResetToken.DoesNotExist:
        messages.error(request, "Invalid or used token.")
        return redirect('news_app:send_password_reset_page')

    if user_token.expiry_date < timezone.now():
        messages.error(request, "Token expired.")
        return redirect('news_app:send_password_reset_page')

    # Update user password
    user = user_token.user
    user.set_password(password)
    user.save()

    # Mark token as used
    user_token.used = True
    user_token.save()

    messages.success(request, "Password reset successful.")
    return redirect('news_app:login')
