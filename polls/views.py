from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, ingredientItem, Recipe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm, CommentForm, RecipeCreateForm
from taggit.models import Tag
from haystack.query import SearchQuerySet
from django.views.generic import ListView


def post_list(request):
    # ob_list = Post.objects.all()
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(Q(title=search_post))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'post/list.html',
        {
            'page': page,
            'posts': posts
        }
    )

# class PostListView(ListView):
#     queryset = Post.objects.all()
#     context_object_name = 'posts'
#     paginate_by = 1
#     template_name = 'post/list.html'


# def post_detail(request, year, month, day, post):
#     # post = Post.objects.all().get(slug=post)
#     post = get_object_or_404(Post, slug=post,
#                              publish__year=year,
#                              publish__month=month,
#                              publish__day=day)
#     return render(request, 'post/detail.html', {'post': post})


# def post_share(request, post_id):
#     post = get_object_or_404(
#         Post,
#         id=post_id,
#         status='published'
#     )
#     sent = False
#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(
#                 post.get_absolute_url()
#             )
#             subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
#             message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
#             send_mail(subject, message, 'admin@myblog.com', [cd['to']])
#             sent = True
#
#     form = EmailPostForm()
#     return render(
#         request,
#         'post/share.html',
#         {'post': post,
#          'form': form,
#          'sent': sent}
#     )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post.objects.filter(slug=post),
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    comment_form = CommentForm()
    return render(
        request,
        'post/detail.html',
        {'post': post,
         'comments': comments,
         'comment_form': comment_form}
    )


# def post_list(request, tag_slug=None):
#     object_list = Post.objects.all()
#     tag = None
#     if tag_slug:
#         tag = get_object_or_404(Tag, slug=tag_slug)
#         object_list = object_list.filter(tags__in=[tag])
#     paginator = Paginator(object_list, 1)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(
#         request,
#         'post/list.html',
#         {'page': page,
#          'posts': posts,
#          'tag': tag}
#     )


def products(request):
    all_ingredients = ingredientItem.objects.all()
    return render(request, 'post/products.html', {'all_ingredients': all_ingredients})


def recipe(request):
    recipes = Recipe.objects.all()
    if request.method == 'POST':
        recipe_create = RecipeCreateForm(data=request.POST)
        if recipe_create.is_valid():
            new_recipe_create = recipe_create.save(commit=False)
            new_recipe_create.author = request.user
            new_recipe_create.save()
    recipe_create = RecipeCreateForm()
    return render(request, 'post/price.html', {
        'recipes': recipes,
        'recipe_create': recipe_create
    })

    # comments = post.comments.filter(active=True)
    # if request.method == 'POST':
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.post = post
    #         new_comment.save()
    # comment_form = CommentForm()
    # return render(
    #     request,
    #     'post/detail.html',
    #     {'post': post,
    #      'comments': comments,
    #      'comment_form': comment_form}
    # )



def create_recipe(request):
    if request.method == 'POST':
        comment_form = RecipeCreateForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.save()
    comment_form = RecipeCreateForm()
    return render(
        request,
        'post/price.html',
        {'comment_form': comment_form}
    )


class RecipeDetailView(DetailView):
    model = Recipe

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'post/recipe_detail.html',
            {'object': RecipeDetailView.model}
        )


# def post_search(request):
#     form = SearchForm()
#     # cd = form.cleaned_data
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             results = SearchQuerySet().models(Post).load_all()
#                 # .filter(content=cd['query'])\
#             # count total results
#             # total_results = results.count()
#     return render(request,
#                   'post/search.html',
#                   {'form': form,})
#                    # 'cd': cd,
#                    # 'results': results,
#                    # 'total_results': total_results}

# class SearchResultsView(ListView):
#     model = Post
#     template_name = 'post/search.html'
#
#     def get_queryset(self):  # новый
#         query = self.request.GET.get('q')
#         object_list = Post.objects.filter(
#             Q(name__icontains=query) | Q(state__icontains=query)
#         )
#         return object_list
