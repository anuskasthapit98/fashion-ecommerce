from django.shortcuts import render
from django.http import HttpResponseRedirect
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


from dashboard.forms import *
from dashboard.models import *
from dashboard.mixines import *

from .mixins import *

from dashboard.mixines import NonDeletedItemMixin
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
    
    
#Resgistration 

class CustomerRegistrationView(CreateView):
    template_name = 'home/auth/register.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('home:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomerCreateForm()

        return context

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('first_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        obj = Customer.objects.create(
            first_name=first_name, last_name=last_name, email=email, mobile=mobile, password = password, confirm_password = confirm_password )
        return redirect('home:home')

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


#blogs

class BlogView(ListView):
    template_name= 'home/blog/blog.html'
    model = Blog
    paginate_by = 3
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
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
        quantity = request.POST.get('quantity')
        size = request.POST.get('size')
        print(quantity, size, 88888888888888888888)

        # getting product id
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Products.objects.get(id=product_id)
        # check if cart exists of not
        cart_id = self.request.session.get('cart_id')
        # if cart exists
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            # checking for product existance
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)
            # if product already exists
            if this_product_in_cart:
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.subtotal += product_obj.selling_price
                if product_obj.vat_amt:
                    cart_obj.vat += product_obj.vat_amt
                cart_obj.total = cart_obj.subtotal + cart_obj.vat
                cart_obj.save()
                messages.success(self.request, "Item added to cart")
            # if product doesnot exists
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1,
                    subtotal=product_obj.selling_price, size='-')
                cart_obj.subtotal += product_obj.selling_price
                if product_obj.vat_amt:
                    cart_obj.vat += product_obj.vat_amt
                cart_obj.total = cart_obj.subtotal + cart_obj.vat
                cart_obj.save()
                messages.success(self.request, "Item added to cart")

        # if cart does not exists
        else:
            cart_obj = Cart.objects.create(total=0, subtotal=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1,
                subtotal=product_obj.selling_price, size='-')
            cart_obj.subtotal += product_obj.selling_price
            if product_obj.vat_amt:
                cart_obj.vat += product_obj.vat_amt
            cart_obj.total = cart_obj.subtotal + cart_obj.vat
            cart_obj.save()
            messages.success(self.request, "Item added to cart")
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
