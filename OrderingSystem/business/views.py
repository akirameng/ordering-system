from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.db.models import Sum
import operator

from Customer.forms import OrderForm, OrderDetailForm
from Customer.models import Order, OrderItem
from models import Restaurant, Address, Dish
from forms import RestaurantForm, AddressForm, DishForm

# Create your views here.


class SignUpView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            Restaurant.objects.get(baseUser=user)
            return HttpResponseRedirect(reverse('business:RestaurantPage'))
        except ObjectDoesNotExist:
            pass

        restaurant_form = RestaurantForm(prefix='restaurant')
        address_form = AddressForm(prefix='address')

        return render(request, 'business/signup.html',
                      {'restaurant_form': restaurant_form, 'address_form': address_form})

    def post(self, request, *args, **kwargs):

        restaurant_form = RestaurantForm(request.POST, request.FILES, prefix='restaurant')
        address_form = AddressForm(request.POST, prefix='address')

        if not (restaurant_form.is_valid() and address_form.is_valid()):
            return render(request, 'business/signup.html',
                          {'restaurant_form': restaurant_form, 'address_form': address_form})

        restaurant = restaurant_form.save(commit=False)
        restaurant.baseUser = request.user
        restaurant.save()

        address = address_form.save(commit=False)
        address.restaurant = restaurant
        address.save()

        return HttpResponseRedirect(reverse('business:RestaurantPage'))


class RestaurantView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            restaurant = Restaurant.objects.get(baseUser=user)
        except ObjectDoesNotExist:
            return HttpResponse('NO restaurant found.', status=404)

        address = Address.objects.get(restaurant=restaurant)
        dishes = Dish.objects.filter(restaurant=restaurant)

        if not isinstance(dishes, list):
            dishes = list(dishes)

        return render(request, 'business/detail.html',
                      {'restaurant': restaurant, 'address': address, 'dishes': dishes, 'dish_form': DishForm()})

    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(baseUser=user)

        dish_form = DishForm(request.POST, request.FILES)

        if dish_form.is_valid():
            dish = dish_form.save(commit=False)
            dish.restaurant = restaurant
            dish.save()
            dish_form = DishForm()

        address = Address.objects.get(restaurant=restaurant)
        dishes = Dish.objects.filter(restaurant=restaurant)

        if not isinstance(dishes, list):
            dishes = list(dishes)
        return render(request, 'business/detail.html',
                      {'restaurant': restaurant, 'address': address, 'dishes': dishes, 'dish_form': dish_form})


class ReportView(TemplateView):
    def get(self, request, *args, **kwargs):
        last_week = datetime.now() - timedelta(days=7)
        last_week_orders = Order.objects.filter(restaurant=request.user.restaurant, time__gt=last_week)
        last_week_amount = []
        last_week_count = []
        last_week_order_count = {}
        for idx in range(0, 7):
            total = 0
            one_day_order = last_week_orders.filter(
                time__range=(last_week + timedelta(days=idx), last_week + timedelta(days=idx + 1)))
            for order in one_day_order:
                total += order.total_price
                for orderItem in order.orderitem.all():
                    if orderItem.Dish.name in last_week_order_count:
                        last_week_order_count[orderItem.Dish.name] += orderItem.number
                    else:
                        last_week_order_count[orderItem.Dish.name] = orderItem.number
            last_week_amount.append(total)
            last_week_count.append(one_day_order.count())

        second_last_week = last_week - timedelta(days=7)
        second_last_week_orders = Order.objects.filter(restaurant=request.user.restaurant,
                                                       time__range=(second_last_week, last_week))
        second_last_week_amount = []
        second_last_week_count = []
        second_last_week_order_count = {}
        for idx in range(0, 7):
            total = 0
            one_day_order = second_last_week_orders.filter(
                time__range=(second_last_week + timedelta(days=idx), second_last_week + timedelta(days=idx + 1)))
            for order in one_day_order:
                total += order.total_price
                for orderItem in order.orderitem.all():
                    if orderItem.Dish.name in second_last_week_order_count:
                        second_last_week_order_count[orderItem.Dish.name] += orderItem.number
                    else:
                        second_last_week_order_count[orderItem.Dish.name] = orderItem.number
            second_last_week_amount.append(total)
            second_last_week_count.append(one_day_order.count())
        day_name = []
        for idx in range(1, 8):
            day_name.append((datetime.now() + timedelta(days=idx)).strftime('%A'))

        predict_amount = [sum(ele) / len(ele) for ele in zip(*[last_week_amount, second_last_week_amount])]
        return render(request, 'business/report.html', {'predict_amount': predict_amount,
                                                        'last_week_amount': last_week_amount,
                                                        'second_last_week_amount': second_last_week_amount,
                                                        'last_week_count': last_week_count,
                                                        'second_last_week_count': second_last_week_count,
                                                        'last_week_order_count': last_week_order_count,
                                                        'second_last_week_order_count': second_last_week_order_count,
                                                        'day_name': day_name})

class EditRestaurantView(TemplateView):
    def get(self, request, *args, **kwargs):
        restaurant = Restaurant.objects.get(baseUser=request.user)
        address = Address.objects.get(restaurant=restaurant)

        restaurant_form = RestaurantForm(instance=restaurant, prefix='restaurant')
        address_form = AddressForm(instance=address, prefix='address')

        return render(request, 'business/edit_restaurant_page.html',
                      {'restaurant_form': restaurant_form, 'address_form': address_form})

    def post(self, request, *args, **kwargs):
        restaurant_form = RestaurantForm(request.POST, request.FILES, prefix='restaurant')
        address_form = AddressForm(request.POST, prefix='address')

        if not (restaurant_form.is_valid() and address_form.is_valid()):
            return render(request, 'business/edit_restaurant_page.html',
                          {'restaurant_form': restaurant_form, 'address_form': address_form})

        restaurant = Restaurant.objects.get(baseUser=request.user)
        address = Address.objects.get(restaurant=restaurant)

        RestaurantForm(request.POST, request.FILES, prefix='restaurant', instance=restaurant).save()
        AddressForm(request.POST, prefix='address', instance=address).save()

        return HttpResponseRedirect(reverse('business:RestaurantPage'))


class DishView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(baseUser=user)
        try:
            dish = Dish.objects.get(restaurant=restaurant, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponse('Dish does not exist.', status=404)

        dish_form = DishForm(instance=dish)

        return render(request, 'business/dish_detail.html', {'dish_form': dish_form, 'dish': dish})

    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(baseUser=user)
        try:
            dish = Dish.objects.get(restaurant=restaurant, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponse('Dish does not exist.', status=404)
        dish_form = DishForm(request.POST, request.FILES)
        if dish_form.is_valid():
            DishForm(request.POST, request.FILES, instance=dish).save()

        return HttpResponseRedirect(reverse('business:RestaurantPage'))


class OrderView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(baseUser=user)
        try:
            order = Order.objects.get(restaurant=restaurant, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponse('Order does not exist.', status=404)

        Oitem = OrderItem.objects.filter(Order = order)
        dish_set = set()
        count = 0
        while (count<len(Oitem)):
           dish_set.add(Oitem[count].Dish)
           count = count + 1
        order_form = OrderDetailForm(instance=order)
        dictionary_delivery_type = {0: 'PickUp', 1: 'Home Delivery Service'}
        payment_status = {True: 'Paid', False: 'Not Paid'}

        return render(request, 'business/order_detail.html', {'order_form': order_form, 'order': order, 'dish_set': dish_set, 'deliverytype': dictionary_delivery_type, 'orderitem': Oitem, 'paytype': payment_status})

    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(baseUser=user)
        try:
            order = Order.objects.get(restaurant=restaurant, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponse('Order does not exist.', status=404)
        order_form = OrderDetailForm(request.POST)
        if order_form.is_valid():
            print order.status
            OrderDetailForm(request.POST, instance=order).save()

        return HttpResponseRedirect(reverse('business:OrderListPage'))


class OrderListView(TemplateView):
    def get(self, request, *args, **kwargs):

        user = request.user
        try:
            restaurant = Restaurant.objects.get(baseUser=user)
        except ObjectDoesNotExist:
            return HttpResponse('NO restaurant found.', status=404)

        orders = Order.objects.filter(restaurant=restaurant)
        progorders = Order.objects.filter(restaurant=restaurant, status='prog').order_by('-time')
        progorders = progorders[:8]
        finorders = Order.objects.filter(restaurant=restaurant, status='fin').order_by('-time')
        finorders = finorders[:4]
        canorders = Order.objects.filter(restaurant=restaurant, status='can').order_by('-time')
        canorders = canorders[:4]

        if not isinstance(orders, list):
            orders = list(orders)
        return render(request, 'business/order.html',
                      {'canorders': canorders, 'progorders': progorders, 'finorders': finorders, 'orders': orders,
                       'order_form': OrderForm()})

    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(baseUser=user)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.restaurant = restaurant
            order.save()
            order_form = OrderForm()
        orders = Order.objects.filter(restaurant=restaurant)
        progorders = Order.objects.filter(restaurant=restaurant, status='prog')
        progorders = progorders[:4]
        finorders = Order.objects.filter(restaurant=restaurant, status='fin')
        finorders = finorders[:4]
        canorders = Order.objects.filter(restaurant=restaurant, status='can')
        canorders = canorders[:4]
        return render(request, 'business/order.html',
                      {'canorders': canorders, 'progorders': progorders, 'finorders': finorders, 'orders': orders,
                       'order_form': order_form})


class InprocessOrderView(TemplateView):
    def get(self, request, *args, **kwargs):

        user = request.user
        try:
            restaurant = Restaurant.objects.get(baseUser=user)
        except ObjectDoesNotExist:
            return HttpResponse('NO restaurant found.', status=404)

        orders = Order.objects.filter(restaurant=restaurant)
        progorders = Order.objects.filter(restaurant=restaurant, status='prog').order_by('-time')
        if not isinstance(orders, list):
            orders = list(orders)
        return render(request, 'business/inprocessorder.html', {'progorders': progorders, 'orders': orders})


class CompleteOrderView(TemplateView):
    def get(self, request, *args, **kwargs):

        user = request.user
        try:
            restaurant = Restaurant.objects.get(baseUser=user)
        except ObjectDoesNotExist:
            return HttpResponse('NO restaurant found.', status=404)

        orders = Order.objects.filter(restaurant=restaurant)
        finorders = Order.objects.filter(restaurant=restaurant, status='fin').order_by('-time')
        if not isinstance(orders, list):
            orders = list(orders)
        return render(request, 'business/completeorder.html', {'finorders': finorders, 'orders': orders})


class CanceledOrderView(TemplateView):
    def get(self, request, *args, **kwargs):

        user = request.user
        try:
            restaurant = Restaurant.objects.get(baseUser=user)
        except ObjectDoesNotExist:
            return HttpResponse('NO restaurant found.', status=404)

        orders = Order.objects.filter(restaurant=restaurant)
        canorders = Order.objects.filter(restaurant=restaurant, status='can').order_by('-time')
        print type(canorders)
        if not isinstance(orders, list):
            orders = list(orders)
        return render(request, 'business/cancelorder.html', {'canorders': canorders, 'orders': orders})


class BuyerView(TemplateView):

    def get(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(baseUser=user)
        try:
            order = Order.objects.get(restaurant=restaurant, pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return HttpResponse('Order does not exist.', status=404)

        orders = Order.objects.filter(restaurant=restaurant, buyer = order.buyer)

        return render(request, 'business/buyerprofile.html', { 'orders': orders, 'order': order})


