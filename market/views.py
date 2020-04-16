from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q, F
from .models import Item
from .forms import ItemForm, ItemEditForm
from msnmatch import settings
import datetime

@login_required
def market(request):
    return render(request, 'market.html')

@login_required
def market_item(request, item_pk):
    return render(request, 'market_item.html')

@login_required
def my_items(request):
    return render(request, 'market_my_items.html')

@login_required
def get_item(request):
    item = Item.objects.filter(pk=request.GET.get('item_pk')).first()
    if not item:
        return JsonResponse({
            "success":False,
        })
    else:
        return JsonResponse({
            "item":item_json(item),
            "success":True,
        })

@login_required
def get_category_items(request):
    sorted_items = sorted(Item.objects.filter(sold=False, category = request.GET.get('category')), key=lambda c:c.updated,reverse=True)
    return JsonResponse({
        "items":[item_json(item) for item in sorted_items]
    }, encoder=CustomEncoder)

@login_required
def get_all_items(request):
    sorted_items = sorted(Item.objects.filter(sold=False), key=lambda c:c.updated, reverse=True)
    return JsonResponse({
        "items":[item_json(item) for item in sorted_items]
    })

@login_required
def get_my_items(request):
    sorted_items = sorted(Item.objects.filter(user=request.user, sold=False), key=lambda c:c.updated, reverse=True)
    sold_sorted_items = sorted(Item.objects.filter(user=request.user, sold=True), key=lambda c:c.updated, reverse=True)
    return JsonResponse({
        "items":[item_json(item) for item in sorted_items],
        "sold_items":[item_json(item) for item in sold_sorted_items]
    })
    # return JsonResponse({
    #     "items":items
    # }, encoder=CustomEncoder)


@login_required
def item_search_result(request):
    query = request.GET.get("query")
    category = request.GET.get("category")
    if query:
        query = query.strip().lower()
    if not query and not category:
        tmp_item_queryset = Item.objects.filter(sold=False)
        retrieved_items = sorted(tmp_item_queryset, key=lambda c: c.updated.timestamp(), reverse=True)
    elif not query and category:
        tmp_item_queryset = Item.objects.filter(sold=False, category=category)
        retrieved_items = sorted(tmp_item_queryset, key=lambda c: c.updated.timestamp(), reverse=True)
    elif query and not category:
        tmp_item_queryset = Item.objects.filter(sold=False).annotate(
                similarity_name=TrigramSimilarity('name',query),
                similarity_description=TrigramSimilarity('description',query)).filter(Q(similarity_name__gt=0.3) | Q(similarity_description__gt=0.15))
        retrieved_items = sorted(tmp_item_queryset, key=lambda c: (-c.similarity_name,-c.similarity_description))
    else:
        tmp_item_queryset = Item.objects.filter(sold=False, category=category).annotate(
                similarity_name=TrigramSimilarity('name',query),
                similarity_description=TrigramSimilarity('description',query)).filter(Q(similarity_name__gt=0.3) | Q(similarity_description__gt=0.15))
        retrieved_items = sorted(tmp_item_queryset, key=lambda c: (-c.similarity_name,-c.similarity_description))
    retrieved_items = [item_json(item) for item in retrieved_items]

    return JsonResponse({
        "items": retrieved_items,
    })

@login_required
def create_item(request):
    if request.method == "POST":
        post = request.POST.copy()
        post["user"] = request.user.pk
        item_form = ItemForm(post, request.FILES)
        if item_form.is_valid():
            print("Form cleaned data", item_form.cleaned_data)
            item_form.save()
            return JsonResponse({"success":True})
        else:
            print("Market Create Item Error:", item_form.errors)
    return JsonResponse({"sucess":False, "message":"Get request not supported"})

@login_required
def edit_item(request):
    if request.method == "POST":
        post = request.POST.copy()
        item = Item.objects.filter(pk=post["id"]).first()
        if not item:
            return JsonResponse({"success":False, "message":"Item does not exist"})
        if item.user != request.user:
            return JsonResponse({"success":False, "message":"This item is not yours"})
        item_form = ItemEditForm(post, request.FILES, instance=item)
        if item_form.is_valid():
            print("Form cleaned data", item_form.cleaned_data)
            item_form.save()
            return JsonResponse({"success":True})
        else:
            print("Market Create Item Error:", item_form.errors)
            return JsonResponse({"success":False, "message":"Form data not valid"})
    return JsonResponse({"success":False, "message":"Get request not supported"})

@login_required
def delete_item(request):
    if request.method == "POST":
        post = request.POST.copy()
        item = Item.objects.filter(pk=post["id"]).first()
        if not item:
            return JsonResponse({"sucess":False, "message":"Item does not exist"})
        if item.user != request.user:
            return JsonResponse({"sucess":False, "message":"This item is not yours"})
        item.delete()
        return JsonResponse({"success":True})
    return JsonResponse({"sucess":False, "message":"Get request not supported"})

@login_required
def sell_item(request):
    if request.method == "POST":
        post = request.POST.copy()
        item = Item.objects.filter(pk=post["id"]).first()
        if not item:
            return JsonResponse({"sucess":False, "message":"Item does not exist"})
        if item.user != request.user:
            return JsonResponse({"sucess":False, "message":"This item is not yours"})
        item.sold = True
        item.save()
        return JsonResponse({"success":True})
    return JsonResponse({"sucess":False, "message":"Get request not supported"})

def item_json(item):
    if item.image:
        image = item.image.url
    else:
        image = settings.STATIC_URL + "css/images/brand.jpg"
    return {
        "name":item.name,
        "price":item.price,
        "condition":item.condition,
        "id":item.pk,
        "description":item.description,
        "category":item.category,
        "delivery":item.delivery,
        "pickup":item.pickup,
        "image":image,
        "sold":item.sold,
        "user":item.user.pk,
        "email":item.user.email,
        "wechat":item.user.profile.wechat if item.user.profile.wechat else "",
        "updated": item.updated.timestamp(),
        "seller_name":item.user.first_name + " " + item.user.last_name
    }

class CustomEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            try:
                return obj.url
            except ValueError:
                return ''
        return super(CustomEncoder, self).default(obj)