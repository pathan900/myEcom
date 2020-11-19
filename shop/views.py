from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

MERCHANT_KEY = 'bKMfNxPPf_QdZppa'


# Create your views here.
def index(request):
    allProducts = []
    prodCtg = Product.objects.values('category', 'id')
    catgs = {item['category'] for item in prodCtg}
    for catg in catgs:
        prod = Product.objects.filter(category=catg)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProducts.append([prod, range(1, nSlides), nSlides])

    params = {'allProducts': allProducts}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProducts = []
    prodCtg = Product.objects.values('category', 'id')
    catgs = {item['category'] for item in prodCtg}
    for catg in catgs:
        prodtemp = Product.objects.filter(category=catg)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProducts.append([prod, range(1, nSlides), nSlides])

    params = {'allProducts': allProducts, 'msg': ''}
    if len(allProducts) == 0 or len(query) < 3:
        params = {'msg': 'Item Not Found......! Please enter a relevant item.'}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/shopAbout.html')


def contact(request):
    thanks = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        country = request.POST.get('country', '')
        subject = request.POST.get('subject', '')
        dsc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, country=country, subject=subject, dsc=dsc)
        contact.save()
        thanks = True
    return render(request, 'shop/contactus.html', {'thanks': thanks})


def tracker(request):
    if request.method == "POST":
        name = request.POST.get('name', " ")
        orderid = request.POST.get('orderid', " ")
        try:
            order = Order.objects.filter(name=name, order_id=orderid)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')


def product(request, myid):
    product = Product.objects.filter(id=myid)

    return render(request, 'shop/product.html', {'product': product[0]})


def mycart(request):
    return render(request, 'my/mycart.html')


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        amount = request.POST.get('amount', '')
        address = request.POST.get('address', '')
        mobile = request.POST.get('mobile', '')
        landmark = request.POST.get('landmark', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(items_json=items_json, name=name, address=address, mobile=mobile, landmark=landmark, city=city,
                      state=state, zip_code=zip_code, amount=amount, email=email)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="Your Order Has Been Successfully Placed.")
        update.save()
        thanks = True
        id = order.order_id
        # request paytm to transfer the amount to your account after payment by user
        #param_dict = {'MID': 'MizQwb47156271309021',
                      #'ORDER_ID': str(order.order_id),
                      #'TXN_AMOUNT': str(amount),
                      #'CUST_ID': email,
                      #'INDUSTRY_TYPE_ID': 'Retail',
                      #'WEBSITE': 'WEBSTAGING',
                      #'CHANNEL_ID': 'WEB',
                      #'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
                      #}
        #param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        #return render(request, 'shop/paytm.html', {'param_dict': param_dict})
        return render(request, 'shop/checkout.html', {'thanks': thanks, 'id': id})
    return render(request, 'shop/checkout.html')


#@csrf_exempt
#def handlerequest(request):
    #return HttpResponse('done')
    #pass
