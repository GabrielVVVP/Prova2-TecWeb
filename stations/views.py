from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from django.urls import reverse
from .models import Station, Parameter, User
from .serializers import StationSerializer, ParameterSerializer, UserSerializer
import requests
import geocoder
import json
import re

 
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
 
def check(email):
    if(re.search(regex, email)):
        return True
 
    else:
        return False

def login(request):
    if request.method == 'GET':
        # Pegar Token
        API_ENDPOINT = "http://54.88.109.168/gabrielvvvp/token"
        r = requests.get(url = API_ENDPOINT)
        token = str(json.loads(r.text)['token'])
        # Request da Imagem
        API_ENDPOINT2 = " http://54.88.109.168/gabrielvvvp/image"
        r2 = requests.post(url = API_ENDPOINT2, data = json.dumps({"token": token}))
        imgendpoint = str(json.loads(r2.text)['image_uri'])
        # Endereço da Imagem
        address = " http://54.88.109.168"+imgendpoint
        print(address)
        return render(request, 'stations/index.html', {'selo': address})
    else:
        username = request.POST.get('username')
        if (User.objects.all().filter(name=username).exists()):
            password_full = User.objects.all().filter(name=username).first().password
            pass_receive = request.POST.get('password')  
            if (pass_receive==str(password_full)):
                return redirect(reverse('menu', kwargs={"user_id": User.objects.all().filter(name=username).first().id}))
            else:
                return render(request, 'stations/index.html')
        else:
            return render(request, 'stations/index.html')    

def signin(request):
    if request.method == 'GET':
        return render(request, 'stations/signin.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if (User.objects.all().filter(name=username).exists()==False):
            if (User.objects.all().filter(email=email).exists()==False):
                if check(email) == True:
                    if len(password)>4:
                        station = User(name=username,email=email,password=password,favorites="")
                        station.save()
                        return redirect('index')
                    else:
                        return render(request, 'stations/signin.html')      
                else:
                    return render(request, 'stations/signin.html')    
            else:
                return render(request, 'stations/signin.html')    
        else:
            return render(request, 'stations/signin.html')        

def menu(request,user_id):
    if request.method == 'POST':
        statname = request.POST.get('station-name')
        if (Station.objects.all().filter(name=statname).exists()==False)and(statname!=""):
            g = geocoder.ip('me')
            geolocat = str(g.latlng[0])+","+str(g.latlng[1])
            station = Station(name=statname,location=geolocat)
            station.save()
        return redirect(reverse('menu', kwargs={"user_id": user_id}))
    else:
        all_stations = Station.objects.all()
        all_params = Parameter.objects.all()
        return render(request, 'stations/menu.html', {'stations': all_stations, 'parameters':all_params, 'user_id':user_id})

def create_parameter(request,user_id,station):
    if request.method == 'POST':
        paramname = request.POST.get('parameter-name')
        if (paramname!=""):
            check_station = Station.objects.all().filter(name=station).first()
            parameter = Parameter(name=paramname,station=check_station,readings="")
            parameter.save()
        return redirect(reverse('menu', kwargs={"user_id": user_id}))    

def check_data(request,user_id,station,name,type_chart='line'):
    if request.method == 'GET':
        check_station = Station.objects.all().filter(name=station).first()
        check_parameter = Parameter.objects.all().filter(name=name,station=check_station).first()
        values = check_parameter.readings
        dates = check_parameter.dates
        if (values != ""):
            values_list = [float(item) for item in values.split(",")]
        else:
            values_list = [""]    
        if (dates != ""):
            dates_list = dates.split(",")
        else:
            dates_list = [""]  
        return render(request, 'stations/data.html', {'station': check_station, 'parameter':check_parameter, 'values':values_list, 'dates':dates_list, 'type':type_chart, 'user_id':user_id})
    else:
        return redirect(reverse('menu', kwargs={"user_id": user_id}))

def check_location(request,user_id,station,name):
    check_station = Station.objects.all().filter(name=station).first()
    check_parameter = Parameter.objects.all().filter(name=name,station=check_station).first()
    coordinates = check_parameter.location
    f = open('stations/k.json', "r")
    api_key = json.loads(f.read())["key"]
    return render(request, 'stations/location.html', {'station': check_station, 'parameter': check_parameter,'coordinates':coordinates, 'key':api_key, 'user_id':user_id})

def subscribe(request,user_id,station,name):
    if request.method == 'GET':
        check_station = Station.objects.all().filter(name=station).first()
        check_parameter = Parameter.objects.all().filter(name=name,station=check_station).first()
        return render(request, 'stations/subscribe.html', {'station': check_station, 'parameter': check_parameter, 'user_id':user_id})  
    else:
        check_station = Station.objects.all().filter(name=station).first()
        check_parameter = Parameter.objects.all().filter(name=name,station=check_station).first()
        threshold = request.POST.get('Threshold')
        thisuser = User.objects.all().filter(id=user_id).first()
        print(thisuser.favorites)
        try:
            threshold = float(threshold)
            if thisuser.favorites=="":
                new_info = str(check_parameter.id)+":"+str(threshold)
                thisuser.favorites = thisuser.favorites+new_info
            else:
                newi = 0    
                lista = thisuser.favorites.split(",")
                for param in range(len(lista)):
                    par_id = lista[param].split(":")
                    if int(par_id[0])==int(check_parameter.id):
                        new_info = str(check_parameter.id)+":"+str(threshold)
                        lista[param] = new_info
                        newi +=1      
                separator = ','
                separator.join(lista)
                lista = separator.join(lista)
                thisuser.favorites = lista  
                if newi==0:
                    new_info = ","+str(check_parameter.id)+":"+str(threshold)
                    thisuser.favorites = thisuser.favorites+new_info
            thisuser.save()    
        except:
            pass
        return redirect(reverse('menu', kwargs={"user_id": user_id}))   

def send_message(api_key,api_dom,api_send,user_mail,subject,param,thres,valor,site):
    from_origin = 'Aries Micro-Estações <{}>'.format(api_send)
    return requests.post(
        api_dom,
        auth=("api", api_key),
        data={"from": from_origin,
              "to": [user_mail],
              "subject": subject,
              "template": "alert",
			  "v:parametro": param,
              "v:threshold": thres,
              "v:valor": valor,
              "v:site": site
              })      

def delete_station(request,user_id,station_id):
    del_entry = Station.objects.all().filter(id=station_id).first()
    del_entry.delete()
    return redirect(reverse('menu', kwargs={"user_id": user_id}))

def delete_parameter(request,user_id,parameter_id):
    del_entry = Parameter.objects.all().filter(id=parameter_id).first()
    del_entry.delete()
    return redirect(reverse('menu', kwargs={"user_id": user_id}))   

@api_view(['GET', 'POST'])
def api_station(request, station_id=0):
    if station_id==0:
        try:
            stations = Station.objects.all()
        except Station.DoesNotExist:
            raise Http404()
        serialized_station = StationSerializer(stations, many=True)    
    else:
        try: 
            station = Station.objects.get(id=station_id)
        except Station.DoesNotExist:
            raise Http404()    
        serialized_station = StationSerializer(station)     
    if request.method == 'POST':
        new_station_data = request.data
        new_station = Station(name=new_station_data['name'],date=new_station_data['date'])
        new_station.save()
        stations = Station.objects.all()    
        serialized_station = StationSerializer(stations, many=True)
    return Response(serialized_station.data)

@api_view(['GET', 'POST'])
def api_parameter(request, parameter_id=0):
    if parameter_id==0:
        try:
            parameters = Parameter.objects.all()
        except Parameter.DoesNotExist:
            raise Http404()
        serialized_parameter = ParameterSerializer(parameters, many=True) 
    else:    
        try:
            parameter = Parameter.objects.get(id=parameter_id)
        except Parameter.DoesNotExist:
            raise Http404()
        serialized_parameter = ParameterSerializer(parameter)
    if request.method == 'POST':
        new_parameter_data = request.data
        if (type(new_parameter_data['station']) == int):
            default_station = Station.objects.all().filter(id=new_parameter_data['station']).first()
        else:
            default_station = Station.objects.all().filter(id=1).first()
        new_parameter = Parameter(station=default_station,name=new_parameter_data['name'],readings="",dates="")
        new_parameter.save()
        parameters = Parameter.objects.all()    
        serialized_parameter = ParameterSerializer(parameters, many=True)    
    return Response(serialized_parameter.data)

@api_view(['GET'])
def api_users(request, user_id=0):
    if user_id==0:
        try:
            users = User.objects.all()
        except User.DoesNotExist:
            raise Http404()
        serialized_user = UserSerializer(users, many=True) 
    else:    
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404()
        serialized_user = UserSerializer(user)
    return Response(serialized_user.data)    

@api_view(['GET', 'POST'])
def api_values(request, parameter_id):
    if request.method == 'POST':
        if (type(parameter_id)==int):
            new_data = request.data
            default_parameter = Parameter.objects.all().filter(id=parameter_id).first()
            if default_parameter.readings != "":
                default_parameter.readings = default_parameter.readings+","+new_data['readings']
            else:
                default_parameter.readings = new_data['readings']
            if default_parameter.dates != "":         
                default_parameter.dates = default_parameter.dates+","+new_data['dates']
            else:    
                default_parameter.dates = new_data['dates']
            default_parameter.location = new_data['location'] 
            default_parameter.save()
            
            #Sending emails
            allusers = User.objects.all()
            for user in allusers:
                lista = user.favorites.split(",")
                for param in lista:
                    par_id = param.split(":")
                    if int(par_id[0])==parameter_id: 
                        if float(new_data['readings'])>float(par_id[1]):
                            f = open('stations/k.json', "r")
                            readjson = json.loads(f.read())
                            api_key = readjson["mailgunkey"]
                            api_dom = readjson["mailgundom"]
                            api_send = readjson["mailgunsend"]
                            user_mail = user.email
                            user_id = user.id
                            station_mail = Station.objects.all().filter(id=default_parameter.station.id).first()
                            subjects = "Alert! {} has exceeded defined Threshold!".format(default_parameter.name)
                            site = "https://safe-spire-18268.herokuapp.com/menu/{}/data/{}/{}".format(user_id,station_mail.name,default_parameter.name)
                            send_message(api_key,api_dom,api_send,user_mail,subjects,default_parameter.name,par_id[1],new_data['readings'],site)

            serialized_parameter = ParameterSerializer(default_parameter)
        else:
            try:
                parameters = Parameter.objects.all()
            except Parameter.DoesNotExist:
                raise Http404()
            serialized_parameter = ParameterSerializer(parameters, many=True)         
    return Response(serialized_parameter.data)  