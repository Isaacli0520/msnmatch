from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from .models import Item
from .forms import ItemForm

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
def category_items(request, category):
    return render(request, 'market_category.html')

@login_required
def get_category_items(request):
    return JsonResponse({
        "items":[model_to_dict(item) for item in Item.objects.filter(category = request.GET.get('category'))]
    }, encoder=CustomEncoder)

@login_required
def get_all_items(request):
    return JsonResponse({
        "items":[model_to_dict(item) for item in Item.objects.all()]
    }, encoder=CustomEncoder)

@login_required
def get_my_items(request):
    items = Item.objects.filter(user=request.user)
    return JsonResponse({
        "items":[model_to_dict(item) for item in items]
    }, encoder=CustomEncoder)


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
    return JsonResponse({"success":False})


class CustomEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            try:
                return obj.url
            except ValueError:
                return ''
        return super(CustomEncoder, self).default(obj)