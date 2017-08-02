import datetime
from django.template.loader import get_template
from django.shortcuts import render, redirect
import simplejson
from .models import *
from django.conf import settings
import re
import requests
from django.http import HttpResponse
from account.models import User
from django.views.generic.base import TemplateView


def get_dates():
    date = datetime.datetime.today()
    count = 5
    data_array = []
    if not date.strftime('%A') == 'Saturday' and not date.strftime('%A') == 'Sunday':
        data_array = [date]
    while count > 0:
        date += datetime.timedelta(days=1)
        if date.strftime('%A') == 'Saturday' or date.strftime('%A') == 'Sunday':
            continue
        else:
            data_array.append(date)
            count -= 1
    start_date = data_array[0]
    end_date = data_array[len(data_array) - 1]
    dates = Date.objects.filter(data__range=(start_date, end_date)).order_by('data')
    return dates



def get_geo_point(address):
    address = re.sub(r'ул\.', '', address).split(',')
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s+%s+%s&key=%s' % (address[2].strip(),
                                                                                                    address[1].strip(),
                                                                                                    address[0].strip(),
                                                                                                    settings.GOOGLE_MAPS_API_KEY))
    data = r.json()
    lat = data['results'][0]['geometry']['viewport']['southwest']['lat']
    lng = data['results'][0]['geometry']['viewport']['southwest']['lng']
    return lat, lng


def user_profile(request):
    if request.method == 'POST' and request.is_ajax():
        email = request.POST.get('email', None)
        try:
            user = Place.objects.get(email=email)
        except:
            Place.objects.create(email=email)
            user = Place.objects.get(email=email)
        date = datetime.datetime.today()
        count = 5
        data_array = []
        if not date.strftime('%A') == 'Saturday' and not date.strftime('%A') == 'Sunday':
            data_array = [date]
        while count > 0:
            date += datetime.timedelta(days=1)
            if date.strftime('%A') == 'Saturday' or date.strftime('%A') == 'Sunday':
                continue
            else:
                data_array.append(date)
                count -= 1
        start_date = data_array[0]
        end_date = data_array[len(data_array) - 1]
        dates = Date.objects.filter(data__range=(start_date, end_date)).order_by('data')
        v_garbage = VGarbage.objects.all().order_by('ordering')
        for day in data_array:
            try:
                Date.objects.get(data=day)
            except:
                Date.objects.create(data=day)
        interval = TimeInterval.objects.all()
        tpl = get_template('trasher/order_1.html')
        answer_html = tpl.render({'user': user, 'dates': dates, 'interval': interval, 'v_garbage': v_garbage})
        json_string = simplejson.dumps({
            'data': answer_html,
        })
        return HttpResponse(json_string, content_type='application/json')
    else:
        return redirect('/')


def add_date_time(request):
    if request.method == "POST" and request.is_ajax():
        email = request.POST.get('email', None)
        time_interval = request.POST.get('time_interval', None)
        date = request.POST.get('date', None)
        v_garbage = VGarbage.objects.get(ordering=request.POST.get('v_garbage', None))

        user = Place.objects.get(email=email)
        try:
            date_time = Date.objects.get(data=date).id
            if TimeInterval.objects.filter(ordering=time_interval, date_time=date_time).exists():
                json_string = simplejson.dumps({
                    'status': False,
                })
                return HttpResponse(json_string, content_type='application/json')
        except:
            pass
        if user.address:
            time = TimeInterval.objects.get(ordering=time_interval)
            data_object = Date.objects.get(data=date)
            time.date_time.add(data_object)
            user.date = data_object
            user.v_garbage = v_garbage
            user.save()
            time.save()
            tpl = get_template('trasher/order_success.html')
            answer_html = tpl.render({'user': user})
            json_string = simplejson.dumps({
                'status': True,
                'data': answer_html
            })
            return HttpResponse(json_string, content_type='application/json')
        else:
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            phone = request.POST.get('phone', None)
            address = request.POST.get('address', None)
            lat, lng = get_geo_point(address)
            user.address = address
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.latitude = lat
            user.longitude = lng
            time = TimeInterval.objects.get(ordering=time_interval)
            data_object = Date.objects.get(data=date)
            time.date_time.add(data_object)
            user.date = data_object
            user.v_garbage = v_garbage
            user.save()
            time.save()
            tpl = get_template('trasher/order_success.html')
            answer_html = tpl.render({'user': user})
            json_string = simplejson.dumps({
                'status': True,
                'data': answer_html
            })
            return HttpResponse(json_string, content_type='application/json')

    else:
        return redirect('/')


class AdminTrash(TemplateView):
    template_name = 'trasher/account.html'

    def get_context_data(self, **kwargs):
        context = super(AdminTrash, self).get_context_data(**kwargs)
        context['dates'] = get_dates()
        return context


class AddMarker(TemplateView):
    template_name = 'trasher/account_with_marker.html'

    def get_context_data(self, **kwargs):
        context = super(AddMarker, self).get_context_data(**kwargs)
        context['users'] = Place.objects.all()
        return context


def add_marker(request):
    if request.method == 'POST':
        date_item = request.POST.get('selectbasic', None)
        print(date_item)
        try:
            date = Date.objects.get(data=date_item)
            users = Place.objects.filter(date=date.id)
        except:
            users = Place.objects.all()
        v_trash = 0
        route_array = []
        for user in users:
            v_trash += user.v_garbage.garbage
            user_array = [user.latitude, user.longitude]
            route_array.append(user_array)
        return render(request, 'trasher/account_with_marker.html', {'users': users, 'trash': v_trash,
                                                                    'dates': get_dates(), 'routes': route_array,
                                                                    'length': (len(route_array) - 1)})


