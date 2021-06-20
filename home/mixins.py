from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from dashboard.models import Contact, CartProduct, Cart


class BaseMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contact'] = Contact.objects.all()
        # accessing cart
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_product = CartProduct.objects.filter(cart=cart_id)
            cart = Cart.objects.get(id=cart_id)
            subtotal = cart.subtotal
        else:
            cart_product = None
            subtotal = 0
        context['cart_products'] = cart_product
        context['subtotal'] = subtotal
        # context['subtotal'] = cart_product.subtotal
        return context

class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/customer/login/?next=/my-cart/")
        return super().dispatch(request, *args, **kwargs)
    
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
