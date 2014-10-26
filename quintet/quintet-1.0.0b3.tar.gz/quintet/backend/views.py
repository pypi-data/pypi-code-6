"""This module contains all the view functions for Quintet."""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail
from django_password_strength.widgets import PasswordStrengthInput
from ..models import (Profile, Section, Tag, Post, Page,Comment, Role,
    Contributor)
from .forms import (PostForm, PageForm, AddContributorForm,
    EditContributorForm, AddReviewerForm, CommentForm, SettingsForm,
    AddUserForm, ChangePhotoForm, PermissionForm, SectionForm)


def can_edit(user, post):
    """Return True if the user has permission to edit the post."""
    return user == post.owner


@login_required(login_url='quintet_login')
def dashboard(request):
    feed = []
    recent_posts = Post.objects.all().order_by('-date_updated')[:5]
    for post in recent_posts:
        feed.append({
            'timestamp': post.date_updated,
            'type': 'post',
            'object': post
        })

    recent_comments = Comment.objects.all().order_by('-date_created')[:5]
    for comment in recent_comments:
        feed.append({
            'timestamp': comment.date_created,
            'type': 'comment',
            'object': comment
        })

    feed.sort(key=lambda x: x['timestamp'], reverse=True)

    posts = Post.objects.all()

    return render(request, 'quintet/dashboard.html', {
        'feed': feed[:5],
        'leaderboard': None,
        'stats': {
            'drafts': posts.filter(status='D').count(),
            'ready_for_review': posts.filter(status='R').count(),
            'published': posts.filter(status='P').count(),
        },
    })


@login_required(login_url='quintet_login')
def list_posts(request, filter=None):
    if not (request.user.has_perm('quintet.add_post') or
            request.user.has_perm('quintet.change_post') or
            request.user.has_perm('quintet.delete_post') or
            request.user.has_perm('quintet.publish_post')):
        raise PermissionDenied

    post_list = Post.objects.all().order_by('-date_updated')
    page = request.GET.get('page')

    if filter == 'my_posts':
        post_list = post_list.filter(owner=request.user).exclude(status='A')
    elif filter is not None:
        post_list = post_list.filter(status=filter)

    paginator = Paginator(post_list, 25)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'quintet/post_list.html', {
        'posts': posts,
        'filter': filter,
        'ready_for_review_count': Post.objects.filter(status='R').count()
    })


@permission_required('quintet.add_post', login_url='quintet_login')
def create_post(request):
    # Create new blank post
    post = Post()
    post.owner = request.user
    post.title = "Untitled Post"
    post.save()
    author = Contributor()
    author.user = request.user
    author.post = post
    role, _ = Role.objects.get_or_create(
        slug='author',
        defaults={
            'title': 'Author',
        }
    )
    author.save()
    author.role.add(role)
    return redirect('edit_post', pk=post.pk)


@login_required(login_url='quintet_login')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not can_edit(request.user, post):
        return redirect('view_post', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.section = form.cleaned_data['section']
            post.markdown = form.cleaned_data['markdown']
            post.tags = form.cleaned_data['tags']
            post.save()
            messages.success(request, "Saved Changes.")
    else:
        form = PostForm(initial={
            'title': post.title,
            'section': post.section,
            'markdown': post.markdown,
            'tags': post.tags.all(),
        })

    add_contributor_form = AddContributorForm()
    add_contributor_form.fields['user'].queryset = User.objects.exclude(
        pk__in=[x.user.pk for x in post.contributors.all()]
    )
    add_reviewer_form = AddReviewerForm()
    add_reviewer_form.fields['user'].queryset = User.objects.exclude(
        pk__in=post.reviewers.all()
    ).exclude(pk=request.user.pk)

    return render(request, 'quintet/post.html', {
        'post': post,
        'form': form,
        'contributor_form': add_contributor_form,
        'edit_contributor_form': EditContributorForm(),
        'add_reviewer_form': add_reviewer_form,
        'comment_form': CommentForm(),
    })


@login_required(login_url='quintet_login')
def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    add_contributor_form = AddContributorForm()
    add_contributor_form.fields['user'].queryset = User.objects.exclude(
        pk__in=post.contributors.all()
    )
    add_reviewer_form = AddReviewerForm()
    add_reviewer_form.fields['user'].queryset = User.objects.exclude(
        pk__in=post.reviewers.all()
    ).exclude(pk=request.user.pk)

    return render(request, 'quintet/post_read_only.html', {
        'post': post,
        'contributor_form': add_contributor_form,
        'edit_contributor_form': EditContributorForm(),
        'add_reviewer_form': add_reviewer_form,
        'comment_form': CommentForm(),
    })


@login_required(login_url='quintet_login')
def set_post_status(request, pk, status):
    post = get_object_or_404(Post, pk=pk)

    post.status = status
    post.save()

    return redirect('edit_post', pk=pk)


@permission_required('quintet.publish_post', login_url='quintet_login')
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.status = 'P'
    post.slug = slugify(post.title)
    post.date_published = datetime.now()
    post.save()

    return redirect('edit_post', pk=pk)


@login_required(login_url='quintet_login')
def archive_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.status = 'A'
    post.save()

    messages.warning(request, 'Archived: %s' % post.title)

    return redirect('list_posts', filter='my_posts')


@permission_required('quintet.delete_post', login_url='quintet_login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.owner != request.user:
        raise PermissionDenied

    post.delete()

    messages.error(request, 'Deleted: %s' % post.title)

    return redirect('list_posts', filter='my_posts')


@login_required(login_url='quintet_login')
def add_contributor(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': "Missing POST data.",
        })

    form = AddContributorForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'error': form.errors,
        })

    contributor = Contributor()
    contributor.post = post
    contributor.user = form.cleaned_data['user']
    contributor.save()
    contributor.role.add(*form.cleaned_data['role'])

    role_pks = []
    role_titles = []
    for role in contributor.role.all():
        role_pks.append(role.pk)
        role_titles.append(role.title)

    return JsonResponse({
        'success': True,
        'pk': contributor.pk,
        'full_name': contributor.user.get_full_name(),
        'role_pks': ','.join(map(str, role_pks)),
        'role': ','.join(role_titles),
        'thumbnail': contributor.user.profile.get_thumbnail_url(),
    })


@login_required(login_url='quintet_login')
def edit_contributor(request, pk, contributor_pk):
    contributor = get_object_or_404(Contributor, pk=contributor_pk)

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': "Missing POST data.",
        })

    form = EditContributorForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'error': form.errors,
        })

    contributor.role = form.cleaned_data['role']
    contributor.save()

    return JsonResponse({
        'success': True,
        'pk': contributor.pk,
        'full_name': contributor.user.get_full_name(),
        'role_pks': [role.pk for role in contributor.role.all()],
        'role': [role.title for role in contributor.role.all()],
    })


@login_required(login_url='quintet_login')
def remove_contributor(request, pk, contributor_pk):
    contributor = get_object_or_404(Contributor, pk=contributor_pk)
    removed_pk = contributor.pk
    contributor.delete()

    return JsonResponse({
        'success': True,
        'pk': removed_pk,
    })


@login_required(login_url='quintet_login')
def add_reviewer(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': "Missing POST data.",
        })

    form = AddReviewerForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'error': form.errors,
        })

    reviewer = form.cleaned_data['user']
    post.reviewers.add(reviewer)

    absolute_url = "%s://%s%s" % (
        request.scheme,
        request.get_host(),
        reverse('quintet.backend.views.view_post', kwargs={'pk': post.pk}),
    )

    send_mail(
        'You have been asked to review: %s' % post.title,
        """
%s would like you to review their post:

%s
%s
        """ % (post.owner.first_name, post.title, absolute_url),
        'Quintet <quintet@%s>' % request.get_host(),
        [reviewer.email],
        fail_silently=True
    )

    return JsonResponse({
        'success': True,
        'pk': reviewer.pk,
        'full_name': reviewer.get_full_name(),
        'thumbnail': reviewer.profile.get_thumbnail_url(),
    })


@login_required(login_url='quintet_login')
def remove_reviewer(request, pk, reviewer_pk=None):
    post = get_object_or_404(Post, pk=pk)
    reviewer = get_object_or_404(User, pk=reviewer_pk)

    post.reviewers.remove(reviewer)

    return JsonResponse({
        'success': True,
        'user': reviewer.pk,
        'post': post.pk,
    })


@login_required(login_url='quintet_login')
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.approved_by.add(request.user)

    return JsonResponse({
        'success': True,
        'user': {
            'pk': request.user.pk,
            'full_name': request.user.get_full_name(),
            'thumbnail': request.user.profile.get_thumbnail_url(),
        },
        'post': post.pk,
    })


@login_required(login_url='quintet_login')
def unapprove_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.approved_by.remove(request.user)

    return JsonResponse({
        'success': True,
        'user': {
            'pk': request.user.pk,
        },
        'post': post.pk,
    })


@login_required(login_url='quintet_login')
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': "Missing POST data.",
        })

    form = CommentForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })

    comment = Comment()
    comment.post = post
    comment.user = request.user
    comment.comment = form.cleaned_data['comment']
    comment.reply_to = None
    comment.excerpt = form.cleaned_data['excerpt']
    comment.save()

    return JsonResponse({
        'success': True,
        'comment': {
            'pk': comment.pk,
            'user': comment.user.get_full_name(),
            'comment': comment.comment,
            'reply_to': comment.reply_to,
            'excerpt': comment.excerpt,
        },
    })


@login_required(login_url='quintet_login')
def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    removed_pk = comment.pk
    comment.delete()

    return JsonResponse({
        'success': True,
        'pk': removed_pk,
    })


@login_required(login_url='quintet_login')
def list_pages(request):
    if not (request.user.has_perm('quintet.add_page') or
            request.user.has_perm('quintet.change_page') or
            request.user.has_perm('quintet.delete_page') or
            request.user.has_perm('quintet.publish_page')):
        raise PermissionDenied

    page_list = Page.objects.all().order_by('-date_updated')
    page = request.GET.get('page')

    paginator = Paginator(page_list, 25)

    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'quintet/page_list.html', {
        'pages': pages,
    })


@permission_required('quintet.add_page', login_url='quintet_login')
def create_page(request):
    # Create new blank page
    page = Page()
    page.title = "Untitled Page"
    page.save()

    return redirect('edit_page', pk=page.pk)


@login_required(login_url='quintet_login')
def edit_page(request, pk):
    page = get_object_or_404(Page, pk=pk)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page.title = form.cleaned_data['title']
            page.markdown = form.cleaned_data['markdown']
            page.save()
            messages.success(request, "Saved Changes.")
    else:
        form = PageForm(initial={
            'title': page.title,
            'markdown': page.markdown,
        })

    return render(request, 'quintet/page.html', {
        'page': page,
        'form': form,
    })


@login_required(login_url='quintet_login')
def set_page_status(request, pk, status):
    page = get_object_or_404(Page, pk=pk)

    page.status = status
    page.save()

    return redirect('edit_page', pk=pk)


@permission_required('quintet.publish_page', login_url='quintet_login')
def publish_page(request, pk):
    page = get_object_or_404(Page, pk=pk)

    page.status = 'P'
    page.slug = slugify(page.title)
    page.date_published = datetime.now()
    page.save()

    return redirect('edit_page', pk=pk)


@login_required(login_url='quintet_login')
def archive_page(request, pk):
    page = get_object_or_404(Page, pk=pk)

    page.status = 'A'
    page.save()

    messages.warning(request, 'Archived: %s' % page.title)

    return redirect('list_pages')


@permission_required('quintet.delete_page', login_url='quintet_login')
def delete_page(request, pk):
    page = get_object_or_404(Page, pk=pk)

    page.delete()

    messages.error(request, 'Deleted: %s' % page.title)

    return redirect('list_pages')


@login_required(login_url='quintet_login')
def edit_user(request, pk=None):
    if int(pk) == request.user.pk:
        user = request.user
    else:
        if not request.user.has_perm('auth.change_user'):
            raise PermissionDenied
        user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        settings_form = SettingsForm(request.POST)
        if settings_form.is_valid():
            user.first_name = settings_form.cleaned_data['first_name']
            user.last_name = settings_form.cleaned_data['last_name']
            user.email = settings_form.cleaned_data['email']
            user.save()
            user.profile.twitter = settings_form.cleaned_data['twitter']
            user.profile.bio = settings_form.cleaned_data['bio']
            user.profile.save()

            messages.success(request, "Saved Changes.")
    else:
        settings_form = SettingsForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'twitter': user.profile.twitter,
            'bio': user.profile.bio,
        })

    return render(request, 'quintet/settings.html', {
        'subject': user,
        'form': settings_form,
        'change_photo_form': ChangePhotoForm(),
        'page': 'general',
    })


@login_required(login_url='quintet_login')
def change_photo(request, pk=None):
    if int(pk) == request.user.pk:
        user = request.user
    else:
        if not request.user.has_perm('auth.change_user'):
            raise PermissionDenied
        user = get_object_or_404(User, pk=pk)

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': "Missing POST data.",
        })

    form = ChangePhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })

    user.profile.photo = form.cleaned_data['photo']
    user.profile.save()

    return JsonResponse({
        'success': True,
        'photo': user.profile.get_thumbnail_url(),
    })


@login_required(login_url='quintet_login')
def change_password(request, pk=None):
    if int(pk) == request.user.pk:
        user = request.user
    else:
        raise PermissionDenied

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            form = PasswordChangeForm(user)
    else:
        form = PasswordChangeForm(user)

    form.fields['new_password1'].widget = PasswordStrengthInput()

    return render(request, 'quintet/settings_password.html', {
        'subject': user,
        'form': form,
        'page': 'password',
    })


@permission_required('quintet.set_perms', login_url='quintet_login')
def edit_permissions(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            user.user_permissions.clear()

            if form.cleaned_data['add_post']:
                perm = Permission.objects.get(codename='add_post')
                user.user_permissions.add(perm)

            if form.cleaned_data['change_post']:
                perm = Permission.objects.get(codename='change_post')
                user.user_permissions.add(perm)

            if form.cleaned_data['delete_post']:
                perm = Permission.objects.get(codename='delete_post')
                user.user_permissions.add(perm)

            if form.cleaned_data['publish_post']:
                perm = Permission.objects.get(codename='publish_post')
                user.user_permissions.add(perm)

            if form.cleaned_data['add_page']:
                perm = Permission.objects.get(codename='add_page')
                user.user_permissions.add(perm)

            if form.cleaned_data['change_page']:
                perm = Permission.objects.get(codename='change_page')
                user.user_permissions.add(perm)

            if form.cleaned_data['delete_page']:
                perm = Permission.objects.get(codename='delete_page')
                user.user_permissions.add(perm)

            if form.cleaned_data['publish_page']:
                perm = Permission.objects.get(codename='publish_page')
                user.user_permissions.add(perm)

            if form.cleaned_data['add_section']:
                perm = Permission.objects.get(codename='add_section')
                user.user_permissions.add(perm)

            if form.cleaned_data['delete_section']:
                perm = Permission.objects.get(codename='delete_section')
                user.user_permissions.add(perm)

            if form.cleaned_data['add_user']:
                perm = Permission.objects.get(codename='add_user')
                user.user_permissions.add(perm)

            if form.cleaned_data['change_user']:
                perm = Permission.objects.get(codename='change_user')
                user.user_permissions.add(perm)

            if form.cleaned_data['delete_user']:
                perm = Permission.objects.get(codename='delete_user')
                user.user_permissions.add(perm)

            if form.cleaned_data['set_perms']:
                perm = Permission.objects.get(codename='set_perms')
                user.user_permissions.add(perm)

            messages.success(request, "Saved Changes.")
    else:
        form = PermissionForm(initial={
            'add_post': user.has_perm('quintet.add_post'),
            'change_post': user.has_perm('quintet.change_post'),
            'delete_post': user.has_perm('quintet.delete_post'),
            'publish_post': user.has_perm('quintet.publish_post'),
            'add_page': user.has_perm('quintet.add_page'),
            'change_page': user.has_perm('quintet.change_page'),
            'delete_page': user.has_perm('quintet.delete_page'),
            'publish_page': user.has_perm('quintet.publish_page'),
            'add_section': user.has_perm('quintet.add_section'),
            'delete_section': user.has_perm('quintet.delete_section'),
            'add_user': user.has_perm('auth.add_user'),
            'change_user': user.has_perm('auth.change_user'),
            'delete_user': user.has_perm('auth.delete_user'),
            'set_perms': user.has_perm('quintet.set_perms'),
        })

    return render(request, 'quintet/settings_permissions.html', {
        'subject': user,
        'form': form,
        'page': 'permissions',
    })


@login_required(login_url='quintet_login')
def list_users(request):
    if not (request.user.has_perm('auth.add_user') or
            request.user.has_perm('auth.change_user') or
            request.user.has_perm('auth.delete_user')):
        raise PermissionDenied
    return render(request, 'quintet/user_list.html', {
        'users': User.objects.all(),
    })


@permission_required('auth.add_user', login_url='quintet_login')
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save(request)

            messages.success(request, "New user created.")
            return redirect('quintet.backend.views.list_users')
    else:
        form = AddUserForm()

    return render(request, 'quintet/add_user.html', {
        'form': form,
    })


@login_required(login_url='quintet_login')
def delete_user(request, pk):
    if int(pk) == request.user.pk:
        user = request.user
    else:
        user = get_object_or_404(User, pk=pk)
        if not request.user.has_perm('auth.delete_user') or user.is_superuser:
            raise PermissionDenied

    if 'confirm' in request.GET:
        user.delete()
        messages.warning(request, "User account deleted.")
        return redirect('list_users')

    return render(request, 'quintet/settings_delete.html', {
        'subject': user,
        'page': 'delete',
    })


@login_required(login_url='quintet_login')
def list_sections(request):
    if not (request.user.has_perm('quintet.add_section') or
            request.user.has_perm('quintet.delete_section')):
        raise PermissionDenied

    return render(request, 'quintet/section_list.html', {
        'sections': Section.objects.all(),
        'section_form': SectionForm(),
    })


@permission_required('quintet.delete_section', login_url='quintet_login')
def delete_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    section.delete()

    messages.error(request, "%s section deleted." % section)
    return redirect('list_sections')


@permission_required('quintet.add_section', login_url='quintet_login')
def add_section(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': "Missing POST data.",
        })

    form = SectionForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })

    section = Section()
    section.name = form.cleaned_data['section']
    section.slug = slugify(section.name)
    section.save()

    return JsonResponse({
        'success': True,
        'section': {
            'pk': section.pk,
            'name': section.name,
            'slug': section.slug,
        },
    })
