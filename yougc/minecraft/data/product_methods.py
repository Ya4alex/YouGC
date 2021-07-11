from datetime import datetime
import time

from .user_methods import get_user_balance
from ..models import (KonlineOnline, Authme, KonlineList, KactivityLeaderboard, SiteProduct, SiteProductCategory,
                      EmailConfirm, KactivityList, SiteProductQueue)
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_product(name):
    return SiteProduct.objects.filter(name=name).first()


def add_product_to_queue(product: SiteProduct, user: User, str_server):
    queue = SiteProductQueue(
        name=product.long_name,
        product_text=f"/ktexture give {user.username} {product}",
        product=product,
        server=str_server
    )
    queue.save()
