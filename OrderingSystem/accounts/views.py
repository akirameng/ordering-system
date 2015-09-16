from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.forms.util import ErrorList
from Customer.models import *
from django.core.exceptions import ObjectDoesNotExist
import operator
from forms import UserUpdateForm
from accounts.models import CustomUser
# Create your views here.


class ProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/profile.html', {'userUpdateForm': UserUpdateForm(instance=request.user)})

    def post(self, request, *args, **kwargs):
        updateForm = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if updateForm.is_valid():
            email = updateForm.cleaned_data['email']
            users = CustomUser.objects.filter(email=email)
            if len(users) >= 1 and users[0] != request.user:
                errors = updateForm._errors.setdefault("email", ErrorList())
                errors.append(u"This email has been register with another account.")
            else:
                updateForm.save();
                updateForm = UserUpdateForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'userUpdateForm': updateForm})

class ActivityView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/activity.html')

class CustomerOrderView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            orders = Order.objects.filter(buyer=user).order_by('-time')
        except ObjectDoesNotExist:
            return HttpResponse('There is no order exist.', status=404)
        return render(request, 'accounts/orders.html', {'orders': orders})

class Detail(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            orders = Order.objects.filter(buyer=user)
            order = Order.objects.get(buyer=user, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponse('There is no order exist.', status=404)

        Oitem = OrderItem.objects.filter(Order = order)
        dish_set = set()
        count = 0
        dish_list = []
        while (count<len(Oitem)):
            dish_set.add(Oitem[count].Dish)
            oneList = {}
            oneList['r'] = Oitem[count].restaurant
            oneList['d'] = Oitem[count].Dish
            oneList['n'] =  Oitem[count].number
            dish_list.append(oneList)
            count = count + 1

        dictionary_delivery_type = {0: 'PickUp', 1: 'Home Delivery Service'}
        payment_status = {True: 'Paid', False: 'Not Paid'}

        return render(request, 'accounts/orderdetail.html', { 'dishlist':dish_list,'order': order, 'dish_set': dish_set, 'deliverytype': dictionary_delivery_type, 'orderitem': Oitem, 'paytype': payment_status})

class LoginSuccessView(TemplateView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('You have successful logged in.')

@sensitive_post_parameters()
@csrf_protect
@never_cache
def modal_login(request, template_name='registration/login.html',
                redirect_field_name=REDIRECT_FIELD_NAME,
                authentication_form=AuthenticationForm,
                current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url('accounts:loginSuccessPage')

            # Okay, security check complete. Log the user in.
            login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
