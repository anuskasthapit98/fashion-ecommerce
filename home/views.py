from django.conf import settings
from django.conf import settings as conf_settings
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.urls.base import clear_script_prefix
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.db.models import F
import random
from django.views.generic import *
from dashboard.forms import *
from dashboard.models import *
from dashboard.mixines import *
from dashboard.mixines import *
from .forms import *
from .mixins import *
from .forms import *


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
        print(self.request.user)
        return context


# Resgistration

class CustomerRegistrationView(BaseMixin, CreateView):
    template_name = 'home/auth/register.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('home:login')

    def form_valid(self, form):
        form.instance.is_customer = True
        user = form.save()
        password = form.cleaned_data.get('password')
        user.set_password(password)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home:home")


class CustomerLoginView(BaseMixin, FormView):
    template_name = "home/auth/login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("home:home")

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

    def form_valid(self, form):
        username = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = authenticate(username=username, password=pword)

        if user is not None:
            login(self.request, user)
            customer = Customer.objects.get(username=self.request.user)
            cart_id = self.request.session.get('cart_id', None)
            if cart_id:
                if customer.cart_items is None:
                    customer.cart_items = cart_id
                    customer.save(update_fields=['cart_items'])
                else:
                    session_cart_product = CartProduct.objects.filter(
                        cart__id=cart_id)
                    print(session_cart_product, "session cart product")
                    for product in session_cart_product:
                        print(product.product, "session product")
                        pro_id = product.product.id
                        print(pro_id, "id showing")
                        cart_obj = Cart.objects.get(id=customer.cart_items)
                        product_obj = Products.objects.get(id=pro_id)
                        # checking for product existance
                        this_product_in_cart = cart_obj.cartproduct_set.filter(
                            product=product_obj)
                        # if product already exists
                        if this_product_in_cart:
                            cartproduct = this_product_in_cart.last()
                            cartproduct.quantity += product.quantity
                            cartproduct.size = product.size
                            cartproduct.subtotal += (product.quantity *
                                                     product_obj.selling_price)
                            cartproduct.save()
                            cart_obj.subtotal += (product.quantity *
                                                  product_obj.selling_price)
                            if product_obj.vat_amt:
                                cart_obj.vat += (product.quantity *
                                                 product_obj.vat_amt)
                            cart_obj.total = cart_obj.subtotal + cart_obj.vat
                            cart_obj.save()

                        # if product doesnot exists
                        else:
                            cartproduct = CartProduct.objects.create(
                                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=product.quantity,
                                subtotal=(product.quantity * product_obj.selling_price), size=product.size)
                            cart_obj.subtotal += (product.quantity *
                                                  product_obj.selling_price)
                            if product_obj.vat_amt:
                                cart_obj.vat += (product.quantity *
                                                 product_obj.vat_amt)
                            cart_obj.total = cart_obj.subtotal + cart_obj.vat
                            cart_obj.save()

        else:
            return redirect(self.success_url)

        return super().form_valid(form)


class CustomerForgotPasswordView(FormView):
    template_name = 'home/auth/reset-password.html'
    form_class = CustomerPasswordResetForm
    success_url = reverse_lazy('home:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        password = get_random_string(8)
        user.set_password(password)
        user.save(update_fields=['password'])

        text_content = 'Your password has been changed. {} '.format(password)
        send_mail(
            'Password Reset | Ekocart',
            text_content,
            conf_settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(self.request, "Password reset code is sent")
        return super().form_valid(form)


# password change view
class CustomerPasswordsChangeView(PasswordChangeView):
    template_name = 'home/auth/password-change.html'
    form_class = CustomerChangePasswordForm
    success_url = reverse_lazy('home:login')

    def get_form(self):
        form = super().get_form()
        form.set_user(self.request.user)
        return form


class CustomerProfileView(TemplateView):
    template_name = 'home/auth/customer-profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(is_customer=True).exists():
            pass
        else:
            return redirect("/customer/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context


class CustomerOrderDetailView(DetailView):
    template_name = 'home/auth/order-detail.html'
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(is_customer=True).exists():
            # order_id = self.kwargs["pk"]
            # order = Order.objects.get(id=order_id)
            # if request.user.customer != order.cart.customer:
            #     return redirect("home:customerprofile")
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


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


class ProductQuickView(View):
    def get(self, request, *args, **kwargs):
        print("get method called")
        if request.is_ajax:
            product_id = request.GET.get("product_id", None)
            product_obj = Products.objects.get(id=product_id)
            product = {
                'id': product_obj.id, 'name': product_obj.name, 'marked_price': product_obj.marked_price,
                'selling_price': product_obj.selling_price, 'description': product_obj.description,
                'status': product_obj.status
            }
            data = {
                'product': product

            }

        return JsonResponse(product)

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
        print(product_id, "add to cart")
        # get product
        product_obj = Products.objects.get(id=product_id)
        # check if cart exists of not
        cart_id = None
        if request.user.is_authenticated and Customer.objects.filter(is_customer=True).exists():
            customer = Customer.objects.get(username=request.user)
            cart_id = customer.cart_items
        else:
            cart_id = self.request.session.get('cart_id', None)
        # if cart exists
        if cart_id is not None:
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
            if request.user.is_authenticated and Customer.objects.filter(is_customer=True).exists():
                customer = Customer.objects.get(username=request.user)
                customer.cart_items = cart_obj.id
                customer.save(update_fields=['cart_items'])

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
        cart_id = None
        if self.request.user.is_authenticated and self.request.user.is_staff == False:
            customer = Customer.objects.get(username=self.request.user)
            cart_id = customer.cart_items
        else:
            cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class CouponView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            coupon_code = request.GET.get("coupon_code", None)
            if Coupon.objects.filter(deleted_at__isnull=True, code=coupon_code, validity_count__gte=1, valid_from__lte=timezone.now(), valid_to__gte=timezone.now()):
                code = self.request.session.get('code')
                if code:
                    pass
                else:
                    request.session['code'] = coupon_code
                return JsonResponse({"valid": True}, status=200)
                # if Coupon.objects.filter(is_used)

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
            form.instance.subtotal = cart_obj.subtotal
            form.instance.total = cart_obj.total
            form.instance.code = f'#Ekocart{cart_id}'
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            code = self.request.session.get('code')
            if code != '' and code != None:
                coupon_obj = Coupon.objects.get(code=code)
                if coupon_obj:
                    form.instance.coupon = Coupon.objects.get(code=code)
                    order.total -= coupon_obj.discount_amt
                    order.save(update_fields=['coupon', 'total'])
            messages.success(self.request, "Your order is on the way.")
        else:
            return redirect("home:home")

        return super().form_valid(form)

# wishlist


class WishlistView(View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs['pro_id']
        product_obj = Products.objects.filter(id=product_id)
        wishlist_id = self.request.session.get('wishlist_id', None)
        if wishlist_id:
            wishlist_obj = Wishlist.objects.get(id=wishlist_id)
            print(wishlist_id, 99999999999999999)
            if True:
                pass
            else:
                wishlist_obj = Wishlist.objects.create()
                wishlist_obj.products.set(product_obj)
                print('new', '1111111111')
                messages.success(self.request, 'Item added to wishlist')
            wishlist_obj = Wishlist.objects.get(id=wishlist_id)
            print('Old wishlist')
            messages.success(self.request, 'Item is added to wishlist')
        else:
            wishlist_obj = Wishlist.objects.create()
            wishlist_obj.products.set(product_obj)
            self.request.session['wishlist_id'] = wishlist_obj.id
            print('New wishlist')
            messages.success(self.request, 'Item is added to wishlist')
            # wishlist = Wishlist.objects.create(products=product_obj)
            # messages.success(self.request, 'Item is added to wishlist')

        return redirect('home:home')


class MyWishListView(BaseMixin, TemplateView):
    template_name = 'home/wishlist/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_id = self.request.session.get("wishlist_id", None)
        print(wishlist_id, 77777777777777777)
        if wishlist_id:
            wishlist = Wishlist.objects.get(id=wishlist_id)
            print(wishlist.products, 88888888888888)
        else:
            wishlist = None
        context['wishlist'] = wishlist
        return context
