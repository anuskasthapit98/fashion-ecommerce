from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, response
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import View
from django.contrib import messages

from dashboard.forms import MessageForm
from dashboard.models import *

# Create your views here.



# home
class HomeTemplateView(TemplateView):
    template_name = 'home/base/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = service.objects.filter(deleted_at__isnull=True)
        return context


# contact

class ContactView(CreateView):
    template_name = 'home/contact/contact.html'
    form_class = MessageForm
    success_url = reverse_lazy('contact')
  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.filter(deleted_at__isnull=True)
        form = MessageForm(self.request.POST or None)
        # context['form'] = MessageForm()

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

# class NewsletterView(View):
#     def post(self, request, *args, **kwargs):
#         email = self.request.POST.get('email')
#         if Subscription.objects.filter(email=email).exists():
#             messages.warning(request, 'Wow, you have already subscribed')
#         else:
#             obj = Subscription.objects.create(email=email)
#             messages.success(request, f'Thank you for subsciption {email}')
#             subject = "Thank you for joining us"
#             from_email = settings.EMAIL_HOST_USER
#             to_email = [email]
#             html_template = get_template("home/newsletter/newsletter.html").render()
#             plain_text = get_template("home/newsletter/newsletter.txt").render()
#             message = EmailMultiAlternatives(subject.plain_text, from_email, to_email)
#             message.attach_alternative(html_template,"text/html")
#             message.send()
#         return response.HttpResponseRedirect(request.META.get('HTTP_REFER'))
