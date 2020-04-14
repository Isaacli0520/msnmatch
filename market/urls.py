from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path('',views.market, name='market'),
    path('items/',views.my_items, name='my_items'),
    path('<category>/',views.category_items, name='category_items'),
    path('item/<int:item_pk>/',views.market_item, name='market_item'),
    # path('create/',views.create, name='create'),
    # path('send/',views.comments_send, name='comments_send'),
    # path('filter/',views.comments_filter, name='comments_filter'),

	# path('<int:slide_pk>/',views.comments, name='comments'),

    path('api/create_item/', views.create_item, name="create_item"),
    path('api/delete_item/', views.delete_item, name="delete_item"),
    path('api/sell_item/', views.sell_item, name="sell_item"),
    path('api/edit_item/', views.edit_item, name="edit_item"),
    path('api/get_my_items/', views.get_my_items, name="get_my_items"),
    path('api/get_category_items/', views.get_category_items, name="get_category_items"),
    path('api/get_all_items/', views.get_all_items, name="get_all_items"),
    path('api/item_search_result/', views.item_search_result, name="item_search_result"),
    # path('api/delete_slide/', views.delete_slide, name="delete_slide"),
    # path('api/get_slide/', views.get_slide, name="get_slide"),
    # path('api/get_slides/', views.get_slides, name="get_slides"),
    # path('api/get_active_slide/', views.get_active_slide, name="get_active_slide"),
]
