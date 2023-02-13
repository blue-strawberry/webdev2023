from django.urls import path, register_converter, re_path
from . import views, converters
from .feeds import LatestPostsFeed

app_name = 'polls'
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('',
         views.post_list,
         name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
            views.post_detail,
            name='post_detail'),
    # path('search/',views.SearchResultsView.as_view, name='search'),
    # path('search/', views.post_search, name='post_search'),
    # path('<int:post_id>/share/',
    #      views.post_share,
    #      name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path("products", views.products, name="products"),
    path("recipe", views.recipe, name="recipe"),
    path('recipe/create', views.create_recipe, name="recipes-create"),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name="recipes-detail"),
]
