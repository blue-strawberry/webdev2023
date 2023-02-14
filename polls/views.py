from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from teach import settings
# from cart.cart import Cart
from .models import Post, Recipe, Category, Product
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm, RecipeCreateForm, LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


@login_required
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
            'posts': posts,
            'section': 'post_list'
        }
    )


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


def products(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(
            Category,
            slug=category_slug
        )
    return render(
        request,
        'post/products.html',
        {'category': category,
         'categories': categories,
         'products': products}
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True
    )
    return render(
        request,
        'post/card_detail.html',
        {'product': product}
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'post/card_detail.html', {'product': product,
                                                     'cart_product_form': cart_product_form})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(
        Product,
        id=product_id
    )
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

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


def recipe_detail(request, id, title):
    recipe = get_object_or_404(
        Recipe,
        id=id,
        title=title
    )
    return render(
        request,
        'post/recipe_detail.html',
        {'recipe': recipe}
    )


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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(
                        request,
                        'post/list.html'
                    )
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(
        request,
        'post/login.html',
        {'form': form}
    )

# def product_detail(request, id, productName):
#     product = get_object_or_404(ingredientItem,
#                                 id=id,
#                                 slug=productName,)
#     cart_product_form = CartAddProductForm()
#     return render(request, 'post/products.html', {
#         'product': product,
#         'cart_product_form': cart_product_form}
#     )
