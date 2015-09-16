import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.urlresolvers import reverse
from business.models import Restaurant, Address, Dish, DishComment
from accounts.models import CustomUser

from models import Order, OrderItem, Comment_R
from forms import OrderForm, OrderDetailForm, CommentForm, NavSearchForm
from serializers import DishSerializer,DishCommentSerializer, RestaurantSerializer
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
from OrderingSystem import settings
from django.utils.encoding import smart_str
from haystack.query import SearchQuerySet
from business.models import Restaurant

class IndexView(TemplateView):
    template = 'Customer/homepage.html'

    def get(self, request, *args, **kwargs):
        restaurant_list = Restaurant.objects.all()
        address_list = Address.objects.all()
        comment_list = Comment_R.objects.all()

        restaurant_address_rating_list = []
        for r in restaurant_list:
            oneList = {}
            oneList['r'] = r
            oneList['address'] = Address.objects.filter(restaurant = r)
            ratingList = Comment_R.objects.filter(restaurant = r)

            total = 0
            if ratingList is not None:
                for r in ratingList:
                    total = r.rating + total
            
            if len(ratingList) == 0:
                rate = 0
            else:
                rate = total / len(ratingList)

            
            rate = round(rate, 1)
            oneList["rating"] = rate
            oneList["vote"] = len(ratingList)
            restaurant_address_rating_list.append(oneList)

        # return HttpResponse(restaurant_address_rating_list[0]['addressList'][0].address)
        return render(request, self.template, {'NavSearchForm':NavSearchForm,'restaurant_list': restaurant_list, 'address_list': address_list, 'comment_list': comment_list, 'list': restaurant_address_rating_list})


class RestaurantDetailView(TemplateView):
    template = 'Customer/restaurant_detail.html'

    def get(self, request, *args, **kwargs):

        try:
            restaurant = Restaurant.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            #return HttpResponse('NO restaurant found.', status=status.HTTP_404_NOT_FOUND)
            return render(request,self.template)            

        address = Address.objects.get(restaurant=restaurant)
        dishestotal = Dish.objects.filter(restaurant=restaurant)
        dishes = dishestotal.extra(
            select={'total_like': 'liked/(liked+unliked)'},
            order_by=['-total_like']
        )[:3]
        dishcount = dishestotal.count()
        comment = list(Comment_R.objects.filter(restaurant=restaurant).order_by('-time'))
        ratetotal = Comment_R.objects.filter(restaurant=restaurant)
        ratecount = ratetotal.count()
        temp = 0


        for r in ratetotal:
            temp = temp + r.rating
        if ratecount == 0:
            rate = 0
        else:
            rate = temp / ratecount

        return render(request, self.template,
                      {'NavSearchForm':NavSearchForm, 'restaurant': restaurant, 'address': address, 'dishes': dishes, 'dishcount': dishcount,
                       'comment': comment, 'comment_form': CommentForm, 'rate': round(rate,1), 'ratecount': ratecount})

    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant = Restaurant.objects.get(pk=kwargs['pk'])
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.restaurant = restaurant
            comment.time = datetime.datetime.now()
            comment.buyer =request.user
            comment.save()
            comment_form = CommentForm()

        address = Address.objects.get(restaurant=restaurant)
        dishesObject = Dish.objects.filter(restaurant=restaurant)
        dishes = dishesObject.extra(
            select={'total_like': 'liked/(liked+unliked)'},
            order_by=['-total_like']
        )[:3]
        comment = list(Comment_R.objects.filter(restaurant=restaurant).order_by('-time'))
        ratetotal = Comment_R.objects.filter(restaurant=restaurant)
        ratecount = ratetotal.count()
        temp = 0

        for r in ratetotal:
            temp = temp + r.rating
        if ratecount == 0:
            rate = 0
        else:
            rate = temp / ratecount

        return render(request, self.template,
                      {'NavSearchForm':NavSearchForm, 'restaurant': restaurant, 'address': address, 'dishes': dishes, 'dishcount': dishesObject.count(),
                       'comment': comment, 'comment_form': comment_form, 'rate': round(rate,1), 'ratecount': ratecount})

class DishListView(TemplateView):
    template = 'Customer/dishlist.html'

    def get(self, request, *args, **kwargs):
        restaurant = Restaurant.objects.get(pk=kwargs['pk'])
        dishes = Dish.objects.filter(restaurant=restaurant).extra(
            select={'total_like': 'liked/(liked+unliked)'},
            order_by=['-total_like']
        )

        ratetotal = Comment_R.objects.filter(restaurant=restaurant)
        ratecount = ratetotal.count()
        temp = 0
        
        entries = Dish.objects.filter(restaurant=restaurant, dishcategory='ent')
        entries_quantity = len(entries)
        mains = Dish.objects.filter(restaurant=restaurant, dishcategory='mai')
        mains_quantity = len(mains)
        desserts = Dish.objects.filter(restaurant=restaurant, dishcategory='des')
        desserts_quantity = len(desserts)
        drinks = Dish.objects.filter(restaurant=restaurant, dishcategory='drk')
        drinks_quantity = len(drinks)
        for r in ratetotal:
            temp = temp + r.rating
        if ratecount == 0:
            rate = 0
        else:
            rate = temp / ratecount

        return render(request, self.template,
                      {'NavSearchForm':NavSearchForm, 'restaurant': restaurant, 'dishes': dishes, 'rate': round(rate,1), 'ratecount': ratecount, 'entries_quantity':entries_quantity, 'mains_quantity':mains_quantity, 'desserts_quantity':desserts_quantity, 'drinks_quantity':drinks_quantity})
        # response.delete_cookie('dishes')
        # return response


class RestaurantAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            return Response(RestaurantSerializer(Restaurant.objects.get(id=pk)).data)
        except ObjectDoesNotExist:
            raise  Http404

class DetailDish(APIView):
    def get_object(self, dish_id):

        try:
            return Dish.objects.get(pk=dish_id)
        except Dish.DoesNotExist:
            raise Http404

    def get(self, request, dish_id, formate=None):

        dish = self.get_object(dish_id)
        serializer = DishSerializer(dish)
        comment=DishComment.objects.filter(dish=dish)
        serializer2=DishCommentSerializer(comment,many=True)
        result=list()
        result.append(serializer.data)
        result.append(serializer2.data)
        return Response(result)        

class DetailDishLike(APIView):
    def get_object(self, dish_id):

        try:
            return Dish.objects.filter(pk=dish_id)
        except Dish.DoesNotExist:
            raise Http404

    def get(self, request, dish_id, formate=None):

        dish = self.get_object(dish_id)
        dish.update(liked=F('liked')+1)
        
        serializer = DishSerializer(Dish.objects.get(pk=dish_id))
        return Response(serializer.data)

class DetailDishUnlike(APIView):
    def get_object(self, dish_id):

        try:
            return Dish.objects.filter(pk=dish_id)
        except Dish.DoesNotExist:
            raise Http404

    def get(self, request, dish_id, formate=None):

        dish = self.get_object(dish_id)
        dish.update(unliked=F('unliked')+1)
        
        serializer = DishSerializer(Dish.objects.get(pk=dish_id))
        return Response(serializer.data)

class FilterView(APIView):
    def get_object(self):
        try:
            return Restaurant.objects.all()
        except Restaurant.DoesNotExist:
            raise Http404

    def post(self,request, *args, **kwargs):
        restaurant=self.get_object()
        address_list = Address.objects.all()
        comment_list = Comment_R.objects.all()
        # if request.data.get("category","")!="":
        #     restaurant=Restaurant.objects.filter(category=request.data.get("category",""))
        #     if request.data.get("Provide_Delivery",)=='true':
        #         restaurant=Restaurant.objects.filter(category=request.data.get("category",""),Provide_Delivery=request.data.get("Provide_Delivery",))
        #         if request.data.get("Children_Friendly",)=='true':
        #             restaurant=Restaurant.objects.filter(category=request.data.get("category",""),Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",))
        #             if request.data.get("Wifi",)=='true':
        #                 restaurant=Restaurant.objects.filter(category=request.data.get("category",""),Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",),Wifi=request.data.get("Wifi",))
        #                 if request.data.get("Vegan",)=='true':
        #                     restaurant=Restaurant.objects.filter(category=request.data.get("category",""),Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",),Wifi=request.data.get("Wifi",),Vegan=request.data.get("Vegan",))
        #                     if request.data.get("GlutenFree",)=='true':
        #                         Restaurant.objects.filter(category=request.data.get("category",""),Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",),Wifi=request.data.get("Wifi",),Vegan=request.data.get("Vegan",),Gluten_Free=request.data.get("GlutenFree",))
        # else:
        #     restaurant=self.get_object()
        #     if request.data.get("Provide_Delivery",)=='true':
        #         restaurant=Restaurant.objects.filter(Provide_Delivery=request.data.get("Provide_Delivery",))
        #         if request.data.get("Children_Friendly",)=='true':
        #             restaurant=Restaurant.objects.filter(Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",))
        #             if request.data.get("Wifi",)=='true':
        #                 restaurant=Restaurant.objects.filter(Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",),Wifi=request.data.get("Wifi",))
        #                 if request.data.get("Vegan",)=='true':
        #                     restaurant=Restaurant.objects.filter(Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",),Wifi=request.data.get("Wifi",),Vegan=request.data.get("Vegan",))
        #                     if request.data.get("GlutenFree",)=='true':
        #                         Restaurant.objects.filter(Provide_Delivery=request.data.get("Provide_Delivery",),Children_Friendly=request.data.get("Children_Friendly",),Wifi=request.data.get("Wifi",),Vegan=request.data.get("Vegan",),Gluten_Free=request.data.get("GlutenFree",))
        
        if request.data.get("category","")!="":
            restaurant=restaurant.filter(category=request.data.get("category",""))
        if request.data.get("Children_Friendly",)=='true':
            restaurant=restaurant.filter(Children_Friendly=request.data.get("Children_Friendly",""))
        if request.data.get("Wifi",)=='true':
            restaurant=restaurant.filter(Wifi=request.data.get("Wifi",""))
        if request.data.get("Vegan",)=='true':
            restaurant=restaurant.filter(Vegan=request.data.get("Vegan",""))
        if request.data.get("GlutenFree",)=='true':
            restaurant=restaurant.filter(Gluten_Free=request.data.get("GlutenFree",""))
        if request.data.get("Provide_Delivery",)=='true':
            restaurant=restaurant.filter(Gluten_Free=request.data.get("Provide_Delivery",""))





        restaurant_address_rating_list = []
        for r in restaurant:
            oneList = {}
            oneList['name'] = r.name
            oneList['id'] =r.pk
            if r.image:
                oneList['image'] = r.image.url
            oneList['phone'] = r.phone
            oneList['category'] = r.get_category_display()
            oneList['opentime'] = r.opentime
            oneList['closetime'] = r.closetime
            addressObject =Address.objects.filter(restaurant = r)[0]
            oneList['address'] = addressObject.address
            oneList['city'] = addressObject.city
            oneList['state'] = addressObject.state
            oneList['zipcode'] = addressObject.zipcode
            oneList['latitude'] = addressObject.latitude
            oneList['longitude'] = addressObject.longitude
            ratingList = Comment_R.objects.filter(restaurant = r)

            total = 0
            if ratingList :
                for r in ratingList:
                    total = r.rating + total
            
            if len(ratingList) == 0:
                rate = 0
            else:
                rate = total / len(ratingList)

            
            rate = round(rate, 1)
            oneList["rating"] = rate
            oneList["vote"] = len(ratingList)
            restaurant_address_rating_list.append(oneList)

        return Response(restaurant_address_rating_list)
        #return Response(request.data['category'])

        




# class RestaurantView(TemplateView):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'Customer/restaurant.html')


class OrderView(TemplateView):
    
    template = 'Customer/order.html'

    def get(self, request, *args, **kwargs):

        try:
            restaurant = Restaurant.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return render(request,'Customer/restaurant_detail.html')  
            # return HttpResponse('NO restaurant found.', status=status.HTTP_404_NOT_FOUND)

        if(request.COOKIES.get('dishes') is not None):

            cookie = json.loads(request.COOKIES.get('dishes'))
            json1=[]

            for one in cookie:

                try:
                    onedish =Dish.objects.get(pk=one['dish_id'],restaurant=restaurant)
                    onejson={}
                    onejson['dish_id']=one['dish_id']
                    onejson['count']=one['count']
                    onejson['name']=onedish.name
                    onejson['price']=onedish.price
                    onejson['total'] = onedish.price * int(one['count'])
                    json1.append(onejson)

                except:
                    onejson = {}
                    # json1 = []  
            
    
            #return HttpResponse(json.dumps(json1))
        else:
            json1=[]


        dishObject = []
        cookieDishNameList = []
        cookieItemObjectList = []

        for item in json1:
            dishObject.append(item['dish_id'])
            cookieDishNameList.append(item['name'])
            cookieItemObjectList = OrderItem.objects.filter(restaurant = restaurant, Dish = Dish.objects.filter(restaurant = restaurant, id__in = dishObject))


        orderItemObject = []
        recommendList = []
        for item in cookieItemObjectList:

            orderItemObject.append(item.Order.id)
        
        recommendList = OrderItem.objects.filter(Order = Order.objects.filter(id__in = set(orderItemObject)))

        dishNameRecommendList = []
        for recommendItem in recommendList:
            dish = Dish.objects.get(pk = recommendItem.Dish.id, restaurant = restaurant)
            dishNameRecommendList.append(dish.name)

        advRecommendList = []
        for d in dishNameRecommendList:
            if d not in cookieDishNameList:
                advRecommendList.append(d)
        advRecommendList1 = set(advRecommendList)

        advRecommendListObject = []
        for o in advRecommendList1:
            advRecommendListObject.append(Dish.objects.get(name = o, restaurant = restaurant))

        # return HttpResponse(advRecommendListObject)
        return render(request, self.template, {'r': restaurant, 'json1':json1, 'advRecommendListObject': advRecommendListObject})

        # return render(request, self.template, {'r': restaurant, 'food_type': dictionary_food_type})

    def post(self, request, *args, **kwargs):

        try:
            restaurant = Restaurant.objects.get(pk=kwargs['pk'])
            # cookie = COOKIES.get('dishes')

        except ObjectDoesNotExist:
            return render(request,'Customer/restaurant_detail.html') 
            # return HttpResponse('NO restaurant found.', status=status.HTTP_404_NOT_FOUND)

        dishNameList = request.POST.getlist("dishName")
        dishPriceList = request.POST.getlist("dishPrice")
        dishQuantityList = request.POST.getlist("dishQ")

        tempOrderList = []
        totalPrice = 0
        for i in range(0, len(dishNameList)):
            if(int(str(dishQuantityList[i])) > 0):
                oneDish = {}
                oneDish['dishName'] = str(dishNameList[i])
                oneDish['dishPrice'] = float(str(dishPriceList[i])[1:])
                oneDish['dishQuantity'] = int(str(dishQuantityList[i]))
                totalPrice = totalPrice + float(str(dishPriceList[i])[1:]) * int(str(dishQuantityList[i]))
                tempOrderList.append(oneDish)


        location = request.POST.get("location")

        deli_type = 1
        if(location == ""):
            deli_type = 0


        order = Order(restaurant = Restaurant.objects.get(pk=kwargs['pk']), buyer = request.user, time = datetime.datetime.now(), location = location, delivery_type = deli_type, total_price = totalPrice, discount = 0, paid = False)
        order.save()

        for item in tempOrderList:
            orderItem = OrderItem(Order = order, Dish = Dish.objects.get(name = item['dishName']), restaurant = Restaurant.objects.get(pk=kwargs['pk']), number = item['dishQuantity'])
            orderItem.save()

        response =  HttpResponseRedirect('/%d/complete' %restaurant.pk)
        response.delete_cookie('dishes')
        return response
   




class CompleteOrderView(TemplateView):

    template = 'Customer/completeOrder.html'

    def get(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return render(request,'Customer/restaurant_detail.html') 
            # return HttpResponse('NO restaurant found.', status=status.HTTP_404_NOT_FOUND)
        
        order = Order.objects.filter(restaurant = restaurant, buyer = request.user)

        order_items = OrderItem.objects.filter(Order=order)

        
        if(len(order) != 0):
            return render(request, self.template, {'r': restaurant, 'newOrder': order[len(order)-1],'order': order, 'order_items':order_items})

        else:
            order = []
            order_items = []
            return render(request, self.template, {'r': restaurant, 'newOrder': order ,'order': order, 'order_items':order_items})



class CookieView(TemplateView):
    template_name = ""
    @csrf_exempt
    def dispatch(self,request, *args, **kwargs):
        return super(CookieView,self).dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
       
        count = smart_str(request.POST.get("count") )
        dish_id =smart_str(request.POST["id"]);
        response = HttpResponse("yes")
        max_age =365 * 24 * 60 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        
        if request.COOKIES.get('dishes'):
            j = request.COOKIES['dishes']
            json1 =json.loads(j)
            data =[]
            flag = False
            for one in json1:
                if one['dish_id'] ==dish_id:
                    one['count']=count
                    data.append(one)
                    flag = True 
                else:
                    data.append(one)

            if not flag:
                item = {}
                item['dish_id']=dish_id
                item['count']=count
                data.append(item)

            response.set_cookie('dishes', json.dumps(data), max_age= max_age, expires=expires)
            
        else:
            json1 ={}
            json1['dish_id']=dish_id
            json1['count']=count
            response.set_cookie('dishes', json.dumps([json1,]), max_age= max_age, expires=expires)
        return response;

class search(TemplateView):

    def get(self, request, *args, **kwargs):
        search_form = NavSearchForm()
        try:
            query = request.GET['search_text'].strip()
            results = SearchQuerySet().models(Restaurant).filter(name=query)
            dish_list = []
            dishresults = SearchQuerySet().models(Dish).filter(name=query)

            for item in dishresults:
                oneList = {}
                dish= Dish.objects.get(pk = item.id)
                oneList['r'] = Restaurant.objects.get(pk=dish.restaurant.id)
                oneList['d'] = dish
                dish_list.append(oneList)
        except ObjectDoesNotExist:
            return HttpResponse('Error', status=404)

        return render(request, 'Customer/search_list.html', {'dishlist':dish_list,'dishresults':dishresults,'results': results})

    def post(self, request, *args, **kwargs):
        search_form = NavSearchForm()
        try:
            query = request.POST['query'].strip()
            results = SearchQuerySet().models(Restaurant).filter(name=query)
            restaurant_address_rating_list = []
            dish_list = []
            dishresults = SearchQuerySet().models(Dish).filter(name=query)

            for item in dishresults:
                oneList = {}
                dish= Dish.objects.get(pk = item.id)
                oneList['r'] = Restaurant.objects.get(pk=dish.restaurant.id)
                oneList['d'] = dish
                dish_list.append(oneList)

            for item in results:

                oneList = {}
                oneList['r'] = Restaurant.objects.get(pk=item.id)

                oneList['address'] = Address.objects.filter(restaurant = oneList['r'])
                ratingList = Comment_R.objects.filter(restaurant = oneList['r'])

                total = 0
                if ratingList is not None:
                    for r in ratingList:
                        total = r.rating + total

                if len(ratingList) == 0:
                    rate = 0
                else:
                    rate = total / len(ratingList)


                rate = round(rate, 1)
                oneList["rating"] = rate
                oneList["vote"] = len(ratingList)
                restaurant_address_rating_list.append(oneList)

        except ObjectDoesNotExist:
            return HttpResponse('Error', status=404)
        return render(request, 'Customer/search_result.html', {'dishcount':len(dishresults),'dishlist':dish_list,'dishresults':dishresults, 'count':len(results),'results': results,'NavSearchForm':NavSearchForm,'list': restaurant_address_rating_list})



