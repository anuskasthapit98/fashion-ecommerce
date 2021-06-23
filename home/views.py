
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls.base import clear_script_prefix
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
import random


from dashboard.forms import *
from dashboard.models import *
from dashboard.mixines import NonDeletedItemMixin

from .mixins import *
from .forms import *


from django.db.models import Q
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


# Resgistration

class CustomerRegistrationView(BaseMixin, CreateView):
    template_name = 'home/auth/register.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('home:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomerCreateForm()
        return context


# products view


class ProductListView(BaseMixin, NonDeletedItemMixin, ListView):
    template_name = 'home/product/list.html'
    model = Products
    paginate_by = 9

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     kw = self.request.GET.get('t')
    #     print(kw, 999999999999)
    #     kw = kw.split(',')
    #     type = kw[0]
    #     category = kw[1]
    #     if type != '':
    #         if type == 'k':
    #             queryset = queryset.filter(
    #                 type__type="Kid", categories__name=category)
    #         elif type == 'm':
    #             queryset = queryset.filter(
    #                 type__type="Men", categories__name=category)
    #         elif type == 'w':
    #             queryset = queryset.filter(
    #                 type__type="Women", categories__name=category)
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('t')
        kw = kw.split(',')
        type = kw[0]
        category = kw[1]
        sub = kw[2]
        products = Category.objects.filter(
            category_type__type=type, parent__name=category, name=sub)
        context['object_list'] = products
        return context


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

    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj

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


# blogs

class BlogView(ListView):
    template_name = 'home/blog/blog.html'
    model = Blog
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(deleted_at__isnull=True)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'keyword' in self.request.GET:
            if self.request.GET.get('keyword') != '':
                search_item = self.request.GET.get('keyword')
                queryset = queryset.filter(Q(title__contains=search_item) |
                                           Q(tags__title__contains=search_item) |
                                           Q(description__icontains=search_item))
        return queryset


class BlogDetailView(DetailView):
    template_name = 'home/blog/detail.html'
    model = Blog
    form_class = BlogCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.exclude(
            id=self.get_object().id).order_by("-id")
        context['form'] = BlogCommentForm(initial={'blog': self.object})
        blog = self.kwargs.get('pk')
        context['comment'] = Comment.objects.filter(blog=blog).order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        blog = self.kwargs.get('pk')
        form = Blog.objects.get(pk=Blog)
        obj = Comment.objects.create(
            full_name=name, email=email, comment=comment, blog=form)

        return redirect('blog-detail', pk=blog)


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


class CouponView(TemplateView):
    def get(self, request, *args, **kwargs):
        print("pppp")
        if request.is_ajax:
            coupon_code = request.GET.get("coupon_code", None)
            print(coupon_code)
            if Coupon.objects.filter(deleted_at__isnull=True, code=coupon_code, validity_count__gte=1, valid_from__lte=timezone.now(), valid_to__gte=timezone.now()):
                # if Coupon.objects.filter(discount_type=="Flat Discount")
                return JsonResponse({"valid": True}, status=200)
            else:
                return JsonResponse({"valid": False}, status=200)
        return JsonResponse({}, status=400)


class CheckoutView(BaseMixin, CreateView):
    template_name = 'home/checkout/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('home:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.shipping_charge = 50
            form.instance.subtotal = cart_obj.subtotal
            form.instance.total = cart_obj.total + cart_obj.vat
            form.instance.code = random.randint(1, 100)
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            # coupon= form.cleaned_data.get("coupon")
            order = form.save()
            messages.success(self.request, "Your order is on the way.")

        else:

            return redirect("home:home")

        return super().form_valid(form)


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
