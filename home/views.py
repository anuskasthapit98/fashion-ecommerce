import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls.base import clear_script_prefix
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.contrib import messages
from django.views.generic.edit import FormView


from dashboard.forms import MessageForm
from dashboard.models import *
from dashboard.mixines import *

from .mixins import *

# Create your views here.


class HomeTemplateView(BaseMixin, TemplateView):
    template_name = 'home/base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(deleted_at__isnull=True)
        context['service'] = service.objects.filter(deleted_at__isnull=True)
        context['brand'] = Brands.objects.filter(deleted_at__isnull=True)
        context['trend_products'] = Products.objects.filter(
            deleted_at__isnull=True).order_by('-view_count')
        context['brand'] = Brands.objects.filter(deleted_at__isnull=True)

        return context

# products view


class ProductListView(BaseMixin, NonDeletedItemMixin, ListView):
    template_name = 'home/product/list.html'
    model = Products


class ProductDetailView(BaseMixin, DetailView):
    template_name = 'home/product/detail.html'
    model = Products
    context_object_name = 'product_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_id = self.kwargs.get('pk')
        obj = Products.objects.get(pk=p_id)
        category = obj.categories
        context['similar_product'] = Products.objects.filter(
            categories__name=category).exclude(pk=p_id)
        return context

# about


class AboutListView(BaseMixin, NonDeletedItemMixin, ListView):
    model = Abouts
    template_name = 'home/about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = Abouts.objects.filter(deleted_at__isnull=True)
        context['testimonial'] = Testimonials.objects.filter(
            deleted_at__isnull=True)
        context['service'] = service.objects.filter(deleted_at__isnull=True)
        context['blog'] = Blog.objects.filter(deleted_at__isnull=True)
        context['brand'] = Brands.objects.filter(deleted_at__isnull=True)

        return context

# contact


class ContactView(BaseMixin, CreateView):
    template_name = 'home/contact/contact.html'
    form_class = MessageForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.filter(deleted_at__isnull=True)
        form = MessageForm(self.request.POST or None)
        context['form'] = MessageForm()

        return context

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        obj = Message.objects.create(
            first_name=first_name, last_name=last_name, email=email, phone=phone, message=message)
        return redirect('contact')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        if "@" not in email:
            return render(self.request, self.template_name,
                          {
                              'error': 'Invalid email',
                              'form': form
                          })
        else:
            pass
        return super().form_valid(form)

# newsletter


class SubscriptionView(View):
    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('email')
        if Subscription.objects.filter(email=email).exists():
            messages.warning(request, "Wow, Already Subscribed.")
        else:
            obj = Subscription.objects.create(email=email)
            messages.success(
                request, f'Thank you for Subscription {email}')
            subject = "Thank you for joining Us"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            html_template = get_template(
                "home/newsletter/newsletter.html").render()
            plain_text = get_template(
                "home/newsletter/newsletter.txt").render()
            message = EmailMultiAlternatives(
                subject, plain_text, from_email, to_email)

            message.attach_alternative(html_template, "text/html")
            message.send()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# cart funtionality view


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        quantity = 1
        size = None
        if 'quantity' in request.GET:
            quantity = int(request.GET.get('quantity'))
        if 'size' in request.GET:
            size = request.GET.get('size')

        print(quantity, size)
        # getting product id
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Products.objects.get(id=product_id)
        # check if cart exists of not
        cart_id = self.request.session.get('cart_id', None)
        # if cart exists
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            # checking for product existance
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)
            # if product already exists
            if this_product_in_cart:
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += quantity
                cartproduct.size = size
                cartproduct.subtotal += (quantity * product_obj.selling_price)
                cartproduct.save()
                cart_obj.subtotal += (quantity * product_obj.selling_price)
                if product_obj.vat_amt:
                    cart_obj.vat += (quantity * product_obj.vat_amt)
                cart_obj.total = cart_obj.subtotal + cart_obj.vat
                cart_obj.save()
                messages.success(self.request, "Item added to cart")
            # if product doesnot exists
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=quantity,
                    subtotal=(quantity * product_obj.selling_price), size=size)
                cart_obj.subtotal += (quantity * product_obj.selling_price)
                if product_obj.vat_amt:
                    cart_obj.vat += (quantity * product_obj.vat_amt)
                cart_obj.total = cart_obj.subtotal + cart_obj.vat
                cart_obj.save()
                messages.success(self.request, "Item added to cart")

        # if cart does not exists
        else:
            cart_obj = Cart.objects.create(total=0, subtotal=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=quantity,
                subtotal=(quantity * product_obj.selling_price), size=size)
            cart_obj.subtotal += (quantity * product_obj.selling_price)
            if product_obj.vat_amt:
                cart_obj.vat += (quantity * product_obj.vat_amt)
            cart_obj.total = cart_obj.subtotal + cart_obj.vat
            cart_obj.save()
            messages.success(self.request, "Item added to cart")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs.get('p_id')
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == 'remove':
            cart_obj.subtotal -= (cp_obj.subtotal)
            cart_obj.vat -= (cp_obj.quantity*cp_obj.product.vat_amt)
            cart_obj.total = cart_obj.subtotal + cart_obj.vat
            cart_obj.save()
            cp_obj.delete()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class MyCartView(BaseMixin, TemplateView):
    template_name = 'home/cart/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


# coupen validation form
class CoupenValidation(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse({"error": "Cannot access this page"}, status=404)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        print('form validation called')
        print(code, 999999999999999999999999)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
