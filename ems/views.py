from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Max
import datetime
import requests

# Create your views here.


@ login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def ems(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        CustomerID = []
        if request.user.is_user:
            device_id = LoginUserDetail.objects.get(
                user_name=username).device_id
            Customer_Name = LoginUserDetail.objects.get(
                device_id=device_id).customer_name
        elif request.user.is_manager:
            Customer_Name = LoginManager.objects.get(
                manager_name=username).Customer_Name
            managername = LoginManager.objects.get(
                manager_name=username).manager_name
            User_details = LoginUserDetail.objects.all()
            DeviceID = []

            for det in User_details:
                if str(det.m0anager_name) == managername:
                    DeviceID.append(det.device_id)

            EnergyOA = []
            MaxDemLoad = []
            Star = []
            Location = []
            State = []
            City = []
            Status = []
            Rating = []
            PF_Avg = []
            for j in DeviceID:
                Sta = LoginUserDetail.objects.filter(
                    device_id=j)[0].state
                Cit = LoginUserDetail.objects.filter(
                    device_id=j)[0].city
                Loc = LoginUserDetail.objects.filter(
                    device_id=j)[0].location
                Stat = Device.objects.filter(device_id=j)[0].device_status
                Rat = Device.objects.filter(device_id=j)[0].device_rating
                Efficency = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Avg('efficiency'))
                Energy_OA = round(float(Efficency['efficiency__avg']), 2)
                EnergyOA.append(Energy_OA)
                MaxDL = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Max('maximum_demand_load'))
                MaxDLoad = round(float(
                    MaxDL['maximum_demand_load__max']), 2)
                MaxDemLoad.append(MaxDLoad)
                Powerfactor_Avg = DevicesInfo.objects.filter(
                    device_id=j).aggregate(Avg('power_factor'))
                PF_Avg.append(
                    round(float(Powerfactor_Avg['power_factor__avg']), 2))
                for e in EnergyOA:
                    if e < 25:
                        Star.append(1)
                    elif 25 < e < 40:
                        Star.append(2)
                    elif 40 < e < 50:
                        Star.append(3)
                    elif 50 < e < 60:
                        Star.append(4)
                    else:
                        Star.append(5)

                Rating.append(Rat)
                State.append(Sta)
                City.append(Cit)
                Location.append(Loc)
                Status.append(Stat)

                UserDetail = zip(State, City, Location, Status,
                                 Rating, EnergyOA, MaxDemLoad, Star, DeviceID, PF_Avg)

        elif request.user.is_superuser:
            Customer_Name = 'Admin'
            Customer_Details = LoginCustomer.objects.all()
            for Cus in Customer_Details:
                CustomerID.append(Cus.customer_id)
            DeviceID = []
            for Customer_ID in CustomerID:
                Total1 = Device.objects.filter(account_id=Customer_ID).count()
                Total = Total1 + Total
                Device_ID = Device.objects.filter(account_id=Customer_ID)
                for i in range(Total1):
                    a = Device_ID[i].device_id
                    DeviceID.append(a)

            EnergyOA = []
            MaxDemLoad = []
            Star = []
            Location = []
            State = []
            City = []
            Status = []
            Rating = []
            PF_Avg = []
            for j in DeviceID:
                Sta = LoginUserDetail.objects.filter(
                    device_id=j)[0].state
                Cit = LoginUserDetail.objects.filter(
                    device_id=j)[0].city
                Loc = LoginUserDetail.objects.filter(
                    device_id=j)[0].location
                Stat = Device.objects.filter(device_id=j)[0].device_status
                Rat = Device.objects.filter(device_id=j)[0].device_rating
                Efficency = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Avg('efficiency'))
                Energy_OA = round(float(Efficency['efficiency__avg']), 2)
                EnergyOA.append(Energy_OA)
                MaxDL = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Max('maximum_demand_load'))
                MaxDLoad = round(float(
                    MaxDL['maximum_demand_load__max']), 2)
                MaxDemLoad.append(MaxDLoad)
                Powerfactor_Avg = DevicesInfo.objects.filter(
                    device_id=j).aggregate(Avg('power_factor'))
                PF_Avg.append(
                    round(float(Powerfactor_Avg['power_factor__avg']), 2))
                for e in EnergyOA:
                    if e < 25:
                        Star.append(1)
                    elif 25 < e < 40:
                        Star.append(2)
                    elif 40 < e < 50:
                        Star.append(3)
                    elif 50 < e < 60:
                        Star.append(4)
                    else:
                        Star.append(5)

                Rating.append(Rat)
                State.append(Sta)
                City.append(Cit)
                Location.append(Loc)
                Status.append(Stat)

                UserDetail = zip(State, City, Location, Status,
                                 Rating, EnergyOA, MaxDemLoad, Star, DeviceID, PF_Avg)

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name
            Customer_ID = LoginCustomer.objects.get(
                customer_name=username).customer_id
            Total = Device.objects.filter(account_id=Customer_ID).count()
            Device_ID = Device.objects.filter(account_id=Customer_ID)
            DeviceID = []
            for i in range(Total):
                a = Device_ID[i].device_id
                DeviceID.append(a)

            EnergyOA = []
            MaxDemLoad = []
            Star = []
            Location = []
            State = []
            City = []
            Status = []
            Rating = []
            PF_Avg = []
            for j in DeviceID:
                Sta = LoginUserDetail.objects.filter(
                    device_id=j)[0].state
                Cit = LoginUserDetail.objects.filter(
                    device_id=j)[0].city
                Loc = LoginUserDetail.objects.filter(
                    device_id=j)[0].location
                Stat = Device.objects.filter(device_id=j)[0].device_status
                Rat = Device.objects.filter(device_id=j)[0].device_rating
                Efficency = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Avg('efficiency'))
                Energy_OA = round(float(Efficency['efficiency__avg']), 2)
                EnergyOA.append(Energy_OA)
                MaxDL = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Max('maximum_demand_load'))
                MaxDLoad = round(float(
                    MaxDL['maximum_demand_load__max']), 2)
                MaxDemLoad.append(MaxDLoad)
                Powerfactor_Avg = DevicesInfo.objects.filter(
                    device_id=j).aggregate(Avg('power_factor'))
                PF_Avg.append(
                    round(float(Powerfactor_Avg['power_factor__avg']), 2))

                for e in EnergyOA:
                    if e < 25:
                        Star.append(1)
                    elif 25 < e < 40:
                        Star.append(2)
                    elif 40 < e < 50:
                        Star.append(3)
                    elif 50 < e < 60:
                        Star.append(4)
                    else:
                        Star.append(5)

                Rating.append(Rat)
                State.append(Sta)
                City.append(Cit)
                Location.append(Loc)
                Status.append(Stat)

                UserDetail = zip(State, City, Location, Status,
                                 Rating, EnergyOA, MaxDemLoad, Star, DeviceID, PF_Avg)

        return render(request, 'ems/dashboard.html', {'username': username, 'Customer_Name': Customer_Name, 'UserDetail': UserDetail})


@login_required(login_url='login')
def emsDashboard(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        CustomerID = []
        if request.user.is_user:
            device_id = LoginUserDetail.objects.get(
                user_name=username).device_id
            Customer_Name = LoginUserDetail.objects.get(
                device_id=device_id).customer_name
        elif request.user.is_manager:
            Customer_Name = LoginManager.objects.get(
                manager_name=username).Customer_Name
            managername = LoginManager.objects.get(
                manager_name=username).manager_name
        elif request.user.is_superuser:
            Customer_Name = 'Admin'
            Customer_Details = LoginCustomer.objects.all()
            for Cus in Customer_Details:
                CustomerID.append(Cus.customer_id)

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name
            Customer_ID = LoginCustomer.objects.get(
                customer_name=username).customer_id

        Details = DevicesInfo.objects.filter(device_id=device_id).last()

        Details_graph = DevicesInfo.objects.filter(
            device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-device_time')

        CR = []
        CY = []
        CB = []
        Time1 = []
        Time = []

        for det in Details_graph:
            Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
            CR.append(det.current_r_phase)
            CY.append(det.current_y_phase)
            CB.append(det.current_b_phase)

        CR.reverse()
        CY.reverse()
        CB.reverse()

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

        TimeN = []

        for t in Time1:
            y = t[:4]
            mo = t[5:7]
            da = t[8:10]
            h = t[11:13]
            m = t[14:16]
            s = t[17:19]
            d2 = datetime.datetime(year=int(y), month=int(mo), day=int(
                da), hour=int(h), minute=int(m), second=int(s))
            d = d1 + d2
            TimeN.append(str(d))

        sl = slice(11, -3)
        for t in TimeN:
            Time.append(t[sl])

        Time.reverse()

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = Device.objects.get(device_id=device_id).device_rating
        Stat = Device.objects.get(device_id=device_id).device_status

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

        LTOD1 = DevicesInfo.objects.filter(
            device_id=device_id).last().device_time.strftime('%Y-%m-%d %H:%M:%S')

        y1 = LTOD1[:4]
        mo1 = LTOD1[5:7]
        da1 = LTOD1[8:10]
        h1 = LTOD1[11:13]
        m1 = LTOD1[14:16]
        s1 = LTOD1[17:19]
        d21 = datetime.datetime(year=int(y1), month=int(mo1), day=int(
            da1), hour=int(h1), minute=int(m1), second=int(s1))

        LTOD = d1 + d21

        if Stat == 'ON':
            now = datetime.datetime.now()
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            format = '%Y-%m-%d %H:%M:%S'
            Current_T = datetime.datetime.strptime(current_time, format)
            Start_time = DeviceOperational.objects.filter(
                device_id=device_id).last().start_time
            diff = Current_T - Start_time
        else:
            now = datetime.datetime.now()
            current_time = now.strftime('%Y-%m-%d %H:%M:%S')
            format = '%Y-%m-%d %H:%M:%S'
            Current_T = datetime.datetime.strptime(current_time, format)
            Start_time = DeviceOperational.objects.filter(
                device_id=device_id).last().start_time
            End_time = DeviceOperational.objects.filter(
                device_id=device_id).last().end_time
            diff = Current_T - End_time

        Efficency = DeviceOperational.objects.filter(
            device_id=device_id).aggregate(Avg('efficiency'))

        Energy_OA = round(float(Efficency['efficiency__avg']), 2)

        if Energy_OA < 25:
            Star = 1
        elif 25 < Energy_OA < 40:
            Star = 2
        elif 40 < Energy_OA < 50:
            Star = 3
        elif 50 < Energy_OA < 60:
            Star = 4
        else:
            Star = 5

    return render(request, 'ems/emsDashboard.html', {'Star': Star, 'diff': diff, 'LTOD': LTOD, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'temperature': temperature, 'description': description, 'icon': icon, 'Time': Time, 'CR': CR, 'CY': CY, 'CB': CB, 'username': username, 'Customer_Name': Customer_Name, 'device_id': device_id, 'Details': Details, 'Details_graph': Details_graph})
