from django.urls import path
from .views import *

app_name = 'dashboard'
urlpatterns = [

    # login
    path('login/', LoginView.as_view(), name="login"),
    # logout
    path('logout/', LogoutView.as_view(), name="logout"),
    # password reset
    path('recoverpassword/<int:pk>',
         PasswordResetView.as_view(), name="reset-password"),
    path('password-forgot/', ForgotPasswordView.as_view(), name='forgot-password'),
    # password change
    path('changepassword/', PasswordsChangeView.as_view(), name="change-password"),

    # user list
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/list/', UsersListView.as_view(), name="users"),
    path('userdisable/<int:pk>/',
         UserToggleStatusView.as_view(), name='user-disable'),
    # dashboard view
    path('dashboard/', AdminDashboardView.as_view(), name="dashboard"),

    # Category
    path('dashboard/related/category/',
         TypeRelatedCategoryView.as_view(), name='type-related-category'),
    path('dashboard/category/', CategoryListView.as_view(), name="categories"),
    path('dashboard/category/create/',
         CategoryCreateView.as_view(), name="category-create"),
    path('dashboard/category/<int:pk>/update/',
         CategoryUpdateView.as_view(), name="category-update"),
    path('dashboard/category/<int:pk>/delete/',
         CategoryDeleteView.as_view(), name="category-delete"),

    # image create
    path('dashboard/product/image/create/',
         ProductImageCreateView.as_view(), name='product-image-create'),

    # product urls here
    path('dashboard/product/specific-list/',
         SpecificProductList.as_view(), name='specific-products'),
    path('dashboard/product/list/',
         ProductListView.as_view(), name='products'),
    path('dashboard/product/create/',
         ProductCreateView.as_view(), name='product-create'),
    path('dashboard/product/<slug:slug>/update/',
         ProductUpdateView.as_view(), name='product-update'),

    path('dashboard/product/<slug:slug>/delete/',
         ProductDeleteView.as_view(), name='product-delete'),

    # brand urls
    path('dashboard/brand/list/', BrandListView.as_view(), name='brands'),
    path('dashboard/brand/create/', BrandCreateView.as_view(), name='brand-create'),
    path('dashboard/brand/<int:pk>/update/',
         BrandUpdateView.as_view(), name='brand-update'),
    path('dashboard/brand/<int:pk>/delete/',
         BrandDeleteView.as_view(), name='brand-delete'),


    # size urls
    path('dashboard/size/list/', SizeListView.as_view(), name='sizes'),
    path('dashboard/size/create/', SizeCreateView.as_view(), name='size-create'),
    path('dashboard/size/<int:pk>/update/',
         SizeUpdateView.as_view(), name='size-update'),
    path('dashboard/size/<int:pk>/delete/',
         SizeDeleteView.as_view(), name='size-delete'),

    # customer urls
    path('dashboard/customer/list/',
         CustomerListView.as_view(), name='customers'),
    path('dashboard/customer/create/',
         CustomerCreateView.as_view(), name='customer-create'),
    path('dashboard/customer/<int:pk>/update/',
         CustomerUpdateView.as_view(), name='customer-update'),
    path('dashboard/customer/<int:pk>/delete/',
         CustomerDeleteView.as_view(), name='customer-delete'),

    # testimonials
    path('dashboard/testimonials/',
         TestimonialListView.as_view(), name='testimonials'),
    path('dashboard/testimonials/create/',
         TestimonialCreateView.as_view(), name='testimonial-create'),
    path('dashboard/testimonials/<int:pk>/update/',
         TestimonialUpdateView.as_view(), name='testimonial-update'),
    path('dashboard/testimonials/<int:pk>/delete/',
         TestimonialDeleteView.as_view(), name='testimonial-delete'),


    # tags urls
    path('dashboard/tags/list/', TagListView.as_view(), name='tags'),
    path('dashboard/tags/create/', TagCreateView.as_view(), name='tag-create'),
    path('dashboard/tags/<int:pk>/update/',
         TagUpdateView.as_view(), name='tag-update'),
    path('dashboard/tags/<int:pk>/delete/',
         TagDeleteView.as_view(), name='tag-delete'),


    # blogs
    path('dashboard/blogs/',
         BlogListView.as_view(), name='blogs'),
    path('dashboard/blogs/create/',
         BlogCreateView.as_view(), name='blogs-create'),
    path('dashboard/blogs/<int:pk>/update/',
         BlogUpdateView.as_view(), name='blogs-update'),
    path('dashboard/blogs/<int:pk>/delete/',
         BlogDeleteView.as_view(), name='blogs-delete'),

    # blogs comment
    path('dashboard/blog/comments/',
         BlogCommentListView.as_view(), name='blog-comments'),
    path('dashboard/blog/comments/create/',
         BlogCommentCreateView.as_view(), name='blog-comment-create'),
    path('dashboard/blog/comments/<int:pk>/update/',
         BlogCommentUpdateView.as_view(), name='blog-comment-update'),
    path('dashboard/blog/comments/<int:pk>/delete/',
         BlogCommentDeleteView.as_view(), name='blog-comment-delete'),


    # contact urls
    path('dashboard/contact/list/', ContactListView.as_view(), name='contacts'),
    path('dashboard/contact/create/',
         ContactCreateView.as_view(), name='contact-create'),
    path('dashboard/contact/<int:pk>/update/',
         ContactUpdateView.as_view(), name='contact-update'),
    path('dashboard/contact/<int:pk>/delete/',
         ContactDeleteView.as_view(), name='contact-delete'),

    # service urls
    path('dashboard/service/list/', ServiceListView.as_view(), name='services'),
    path('dashboard/service/create/',
         ServiceCreateView.as_view(), name='service-create'),
    path('dashboard/service/<int:pk>/update/',
         ServiceUpdateView.as_view(), name='service-update'),
    path('dashboard/service/<int:pk>/delete/',
         ServiceDeleteView.as_view(), name='service-delete'),


    # message urls
    path('dashboard/message/list/', MessageListView.as_view(), name='messages'),
    path('dashboard/message/create/',
         MessageCreateView.as_view(), name='message-create'),
    path('dashboard/message/<int:pk>/update/',
         MessageUpdateView.as_view(), name='message-update'),
    path('dashboard/message/<int:pk>/delete/',
         MessageDeleteView.as_view(), name='message-delete'),

    # color urls
    path('dashboard/color/list/', ColorListView.as_view(), name='colors'),
    path('dashboard/color/create/', ColorCreateView.as_view(), name='color-create'),
    path('dashboard/color/<int:pk>/update/',
         ColorUpdateView.as_view(), name='color-update'),
    path('dashboard/color/<int:pk>/delete/',
         ColorDeleteView.as_view(), name='color-delete'),

    # about urls

    path('dashboard/about/list/', AboutListView.as_view(), name='abouts'),
    path('dashboard/about/create/', AboutCreateView.as_view(), name='about-create'),
    path('dashboard/about/<int:pk>/update/',
         AboutUpdateView.as_view(), name='about-update'),
    path('dashboard/about/<int:pk>/delete/',
         AboutDeleteView.as_view(), name='about-delete'),


    # newsletter urls
    path('dashboard/newsletter/list/',
         NewsletterListView.as_view(), name='newsletters'),
    path('dashboard/newsletter/<int:pk>/delete/',
         NewsletterDeleteView.as_view(), name='newsletter-delete'),
]
