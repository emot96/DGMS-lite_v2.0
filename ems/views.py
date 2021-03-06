from login.models import Service_History
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Max
import datetime
import requests
from .filters import *

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
            Details = DevicesInfo.objects.filter(
                device_id=device_id).exclude(vry_phase_voltage=0).last()

            Details_graph = DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time')

            # , device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)
            PL = []
            Time1 = []
            Time = []

            for det in Details_graph:
                Time1.append(det.start_time .strftime('%Y-%m-%d %H:%M:%S'))
                PL.append(round(det.maximum_demand_load, 2))

            PL.reverse()

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

            sl = slice(5, -3)
            for t in TimeN:
                Time.append(t[sl])

            Time.reverse()

            Cit = LoginUserDetail.objects.get(device_id=device_id).city
            Loc = LoginUserDetail.objects.get(device_id=device_id).location
            Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
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

            gsm = DevicesInfo.objects.filter(
                device_id=device_id).last().gsm_signal

            GWDB = DevicesInfo.objects.filter(
                device_id=device_id).last().gateway_device_battery

            PS = DevicesInfo.objects.filter(
                device_id=device_id).last().gateway_power_status

            PowerStatus = 0
            if PS == 1:
                PowerStatus = 'Healthy'
            else:
                PowerStatus = 'Battery'

            return render(request, 'ems-servo/servo_dashboard_device.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Star': Star, 'diff': diff, 'LTOD': LTOD, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'temperature': temperature, 'description': description, 'icon': icon, 'Time': Time, 'PL': PL, 'username': username, 'Customer_Name': Customer_Name, 'device_id': device_id, 'Details': Details, 'Details_graph': Details_graph})

        elif request.user.is_manager:
            Customer_Name = LoginManager.objects.get(
                manager_name=username).Customer_Name
            managername = LoginManager.objects.get(
                manager_name=username).manager_name
            User_details = LoginUserDetail.objects.all()
            DeviceID = []

            for det in User_details:
                if str(det.manager_name) == managername:
                    DeviceID.append(det.device_id)
                else:
                    pass
            Total = Device.objects.filter(device_id__in=DeviceID).count()
            Capacity = Device.objects.filter(
                device_id__in=DeviceID).aggregate(Sum('device_rating'))
            Capacity = Capacity['device_rating__sum']

            Air_total = LoginEmsAsset.objects.filter(
                device_id__in=DeviceID, cooling="AIR COOLED").count()
            Oil_total = LoginEmsAsset.objects.filter(
                device_id__in=DeviceID, cooling="OIL COOLED").count()
            Air_Capacity = LoginEmsAsset.objects.filter(device_id__in=DeviceID, cooling="AIR COOLED").aggregate(
                Sum('rating_in_kva'))['rating_in_kva__sum']
            Oil_Capacity = LoginEmsAsset.objects.filter(device_id__in=DeviceID, cooling="OIL COOLED").aggregate(
                Sum('rating_in_kva'))['rating_in_kva__sum']
            EnergyOA = []
            MaxDemLoad = []
            Star = []
            Location = []
            State = []
            City = []
            Status = []
            Rating = []
            PF_Avg = []
            Cooling = []
            for j in DeviceID:
                Sta = LoginUserDetail.objects.filter(
                    device_id=j)[0].state
                Cit = LoginUserDetail.objects.filter(
                    device_id=j)[0].city
                Loc = LoginUserDetail.objects.filter(
                    device_id=j)[0].location
                Stat = Device.objects.filter(device_id=j)[0].device_status
                Rat = LoginEmsAsset.objects.get(device_id=j).rating_in_kva
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

                Cooling_type = LoginEmsAsset.objects.get(device_id=j).cooling

                Rating.append(Rat)
                State.append(Sta)
                City.append(Cit)
                Location.append(Loc)
                Status.append(Stat)
                Cooling.append(Cooling_type)

                UserDetail = zip(State, City, Location, Status,
                                 Rating, EnergyOA, MaxDemLoad, Star, DeviceID, PF_Avg, Cooling)

                status = ['fuel_level_percentage',
                          'dg_battery_voltage', 'rpm_ctrl',  'rpm']
                alert = Alerts.objects.filter(
                    device_id__in=DeviceID, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
                alert_count = len(alert)

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

            Total = LoginEmsAsset.objects.filter(
                device_id__in=DeviceID).count()
            Capacity = LoginEmsAsset.objects.filter(
                device_id__in=DeviceID).aggregate(Sum('rating_in_kva'))
            Capacity = Capacity['rating_in_kva__sum']

            Air_total = LoginEmsAsset.objects.filter(
                device_id__in=DeviceID, cooling="AIR COOLED").count()
            Oil_total = LoginEmsAsset.objects.filter(
                device_id__in=DeviceID, cooling="OIL COOLED").count()
            Air_Capacity = LoginEmsAsset.objects.filter(device_id__in=DeviceID, cooling="AIR COOLED").aggregate(
                Sum('rating_in_kva'))['rating_in_kva__sum']
            Oil_Capacity = LoginEmsAsset.objects.filter(device_id__in=DeviceID, cooling="OIL COOLED").aggregate(
                Sum('rating_in_kva'))['rating_in_kva__sum']
            EnergyOA = []
            MaxDemLoad = []
            Star = []
            Location = []
            State = []
            City = []
            Status = []
            Rating = []
            PF_Avg = []
            Cooling = []
            for j in DeviceID:
                Sta = LoginUserDetail.objects.filter(
                    device_id=j)[0].state
                Cit = LoginUserDetail.objects.filter(
                    device_id=j)[0].city
                Loc = LoginUserDetail.objects.filter(
                    device_id=j)[0].location
                Stat = Device.objects.filter(device_id=j)[0].device_status
                Rat = LoginEmsAsset.objects.get(device_id=j).rating_in_kva
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

                Cooling_type = LoginEmsAsset.objects.get(device_id=j).cooling

                Rating.append(Rat)
                State.append(Sta)
                City.append(Cit)
                Location.append(Loc)
                Status.append(Stat)
                Cooling.append(Cooling_type)

                UserDetail = zip(State, City, Location, Status,
                                 Rating, EnergyOA, MaxDemLoad, Star, DeviceID, PF_Avg, Cooling)

                status = ['fuel_level_percentage',
                          'dg_battery_voltage', 'rpm_ctrl',  'rpm']
                alert = Alerts.objects.filter(
                    device_id__in=DeviceID, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
                alert_count = len(alert)

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

                Total = Device.objects.filter(device_id__in=DeviceID).count()
                Capacity = Device.objects.filter(
                    device_id__in=DeviceID).aggregate(Sum('device_rating'))
                Capacity = Capacity['device_rating__sum']

                Air_total = LoginEmsAsset.objects.filter(
                    device_id__in=DeviceID, cooling="AIR COOLED").count()
                Oil_total = LoginEmsAsset.objects.filter(
                    device_id__in=DeviceID, cooling="OIL COOLED").count()
                Air_Capacity = LoginEmsAsset.objects.filter(device_id__in=DeviceID, cooling="AIR COOLED").aggregate(
                    Sum('rating_in_kva'))['rating_in_kva__sum']
                Oil_Capacity = LoginEmsAsset.objects.filter(device_id__in=DeviceID, cooling="OIL COOLED").aggregate(
                    Sum('rating_in_kva'))['rating_in_kva__sum']

                EnergyOA = []
                MaxDemLoad = []
                Star = []
                Location = []
                State = []
                City = []
                Status = []
                Rating = []
                PF_Avg = []
                Cooling = []
                for j in DeviceID:
                    Sta = LoginUserDetail.objects.filter(
                        device_id=j)[0].state
                    Cit = LoginUserDetail.objects.filter(
                        device_id=j)[0].city
                    Loc = LoginUserDetail.objects.filter(
                        device_id=j)[0].location
                    Stat = Device.objects.filter(device_id=j)[0].device_status
                    Rat = LoginEmsAsset.objects.get(device_id=j).rating_in_kva
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

                    Cooling_type = LoginEmsAsset.objects.get(
                        device_id=j).cooling

                    Rating.append(Rat)
                    State.append(Sta)
                    City.append(Cit)
                    Location.append(Loc)
                    Status.append(Stat)
                    Cooling.append(Cooling_type)

                    UserDetail = zip(State, City, Location, Status,
                                     Rating, EnergyOA, MaxDemLoad, Star, DeviceID, PF_Avg, Cooling)

                    status = ['fuel_level_percentage',
                              'dg_battery_voltage', 'rpm_ctrl',  'rpm']
                    alert = Alerts.objects.filter(
                        device_id__in=DeviceID, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
                    alert_count = len(alert)

        return render(request, 'ems-servo/servo_dashboard.html', {'Total': Total, 'Capacity': Capacity, 'Air_total': Air_total, 'Oil_total': Oil_total, 'Air_Capacity': Air_Capacity, 'Oil_Capacity': Oil_Capacity, 'alert_count': alert_count, 'username': username, 'Customer_Name': Customer_Name, 'UserDetail': UserDetail})


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

        Details = DevicesInfo.objects.filter(
            device_id=device_id).exclude(vry_phase_voltage=0).last()

        Details_graph = DeviceOperational.objects.filter(
            device_id=device_id).order_by('-start_time')

        # , device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)
        PL = []
        Time1 = []
        Time = []

        for det in Details_graph:
            if det.maximum_demand_load == None:
                pass
            else:
                PL.append(round(det.maximum_demand_load, 2))
                Time1.append(det.start_time .strftime('%Y-%m-%d %H:%M:%S'))

        PL.reverse()

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

        sl = slice(5, -3)
        for t in TimeN:
            Time.append(t[sl])

        Time.reverse()

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
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

        status = ['fuel_level_percentage',
                  'dg_battery_voltage', 'rpm_ctrl',  'rpm']

        alerts = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alerts)

        asset_details = LoginEmsAsset.objects.get(device_id=device_id)
        service_details = LoginEmsServiceHistory.objects.get(
            device_id=device_id)

        EDOI = LoginEmsAsset.objects.get(
            device_id=device_id).ems_date_of_installation

        gsm = DevicesInfo.objects.filter(device_id=device_id).last().gsm_signal

        GWDB = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_device_battery

        PS = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_power_status

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

    return render(request, 'ems-servo/servo_dashboard_device.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'EDOI': EDOI, 'service_details': service_details, 'asset_details': asset_details, 'alert_count': alert_count, 'Star': Star, 'diff': diff, 'LTOD': LTOD, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'temperature': temperature, 'description': description, 'icon': icon, 'Time': Time, 'PL': PL, 'username': username, 'Customer_Name': Customer_Name, 'device_id': device_id, 'Details': Details, 'Details_graph': Details_graph})


@ login_required(login_url='login')
def emsasset_detail(request, device_id):
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

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
        Stat = Device.objects.get(device_id=device_id).device_status

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

        status = ['fuel_level_percentage',
                  'dg_battery_voltage', 'rpm_ctrl',  'rpm']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        # DDOI = DGMS_Device_Info.objects.get(
        #     Device_ID=device_id).DGMS_Date_Of_Installation

        # Address = Service_History.objects.get(Device_ID=device_id).Address

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

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

        Address1 = Device.objects.get(device_id=device_id).device_location

        Details = LoginEmsAsset.objects.get(device_id=device_id)

        Service_History = LoginEmsServiceHistory.objects.get(
            device_id=device_id)  # LoginEmsAsset

        EDOI = LoginEmsAsset.objects.get(
            device_id=device_id).ems_date_of_installation

        gsm = DevicesInfo.objects.filter(device_id=device_id).last().gsm_signal

        GWDB = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_device_battery

        PS = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_power_status

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

    return render(request, 'ems-servo/servo_asset_asset-detail.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Service_History': Service_History, 'EDOI': EDOI, 'Details': Details, 'Address1': Address1, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'alert_count': alert_count, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'current_time': current_time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat})


@ login_required(login_url='login')
def emsalert(request):

    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        CustomerID = []
        if request.user.is_customer:
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

            TR = None
            Count = None
            alerts = None
            myFilter = None
            startdate = None
            enddate = None

            status = ['fuel_level_percentage',
                      'dg_battery_voltage', 'rpm_ctrl',  'rpm']

            if request.method == 'GET' and 'date' in request.GET:
                alerts = Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(request.GET, queryset=alerts)
                alerts = myFilter.qs

                enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
                startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

            elif request.method == 'GET' and 'range' in request.GET:

                if request.GET['time_range'] == 'Last 30 mins':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 hour':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 7 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 12 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 24 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 days':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 5 days':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=5)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 week':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 weeks':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 month':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 months':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=60)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 6 months':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=183)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 year':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=365)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 years':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')
                else:

                    alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                        alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    enddate = (Alerts.objects.filter(
                        device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                    startdate = (Alerts.objects.filter(
                        device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                TR = request.GET['time_range']

            else:

                alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                enddate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                startdate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

            status = ['fuel_level_percentage',
                      'dg_battery_voltage', 'rpm_ctrl',  'rpm']

            alert = Alerts.objects.filter(
                device_id__in=Device_ID, alert_open=True).exclude(
                    alert_type_name__in=status)

            Count = len(alert)

            Start_Time1 = []
            End_Time1 = []

            for a in alerts:
                Start_Time1.append(a.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                End_Time1.append(a.updated_at.strftime('%Y-%m-%d %H:%M:%S'))

            Time = zip(Start_Time1, End_Time1)

            UTC = '0000-00-00 05:30:00'
            y = UTC[:4]
            mo = UTC[5:7]
            da = UTC[8:10]
            h = UTC[11:13]
            m = UTC[14:16]
            s = UTC[17:19]
            d1 = datetime.timedelta(days=(int(
                y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

            Start_Time = []
            End_Time = []
            for s, e in Time:
                y1 = s[:4]
                mo1 = s[5:7]
                da1 = s[8:10]
                h1 = s[11:13]
                m1 = s[14:16]
                s1 = s[17:19]
                d21 = datetime.datetime(year=int(y1), month=int(mo1), day=int(
                    da1), hour=int(h1), minute=int(m1), second=int(s1))

                Start_Time.append(d1 + d21)

                y2 = e[:4]
                mo2 = e[5:7]
                da2 = e[8:10]
                h2 = e[11:13]
                m2 = e[14:16]
                s2 = e[17:19]
                d22 = datetime.datetime(year=int(y2), month=int(mo2), day=int(
                    da2), hour=int(h2), minute=int(m2), second=int(s2))

                End_Time.append(d1 + d22)

                alerts_details = zip(Start_Time, End_Time, alerts)

            return render(request, 'ems-servo/servo_alerts.html', {'alerts_details': alerts_details, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})

        elif request.user.is_superuser:
            Customer_Name = 'Admin'
            TR = None
            Count = None
            alerts = None
            myFilter = None
            status = ['fuel_level_percentage',
                      'dg_battery_voltage', 'rpm_ctrl',  'rpm']

            if request.method == 'GET' and 'date' in request.GET:
                alerts = Alerts.objects.filter().exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(request.GET, queryset=alerts)
                alerts = myFilter.qs

                enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
                startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

            elif request.method == 'GET' and 'range' in request.GET:

                if request.GET['time_range'] == 'Last 30 mins':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 hour':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 7 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 12 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 24 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 days':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 5 days':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=5)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=5)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 week':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 weeks':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 month':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 months':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=60)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=60)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 6 months':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=183)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=183)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 year':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=365)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=365)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 years':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')
                else:

                    alerts = Alerts.objects.filter().exclude(
                        alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    enddate = Alerts.objects.filter().order_by(
                        '-created_at').exclude(alert_type_name__in=status).last().created_at
                    startdate = Alerts.objects.filter().order_by(
                        '-created_at').exclude(alert_type_name__in=status).first().updated_at

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                TR = request.GET['time_range']

            else:
                status = ['fuel_level_percentage',
                          'dg_battery_voltage', 'rpm_ctrl',  'rpm']

                alerts = Alerts.objects.filter().exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                enddate = Alerts.objects.filter().order_by(
                    '-created_at').exclude(alert_type_name__in=status).last().created_at
                startdate = Alerts.objects.filter().order_by(
                    '-created_at').exclude(alert_type_name__in=status).first().updated_at

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

            alert = Alerts.objects.filter(
                alert_open=True).exclude(alert_type_name__in=status)

            Count = len(alert)

            Start_Time1 = []
            End_Time1 = []

            for a in alerts:
                Start_Time1.append(a.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                End_Time1.append(a.updated_at.strftime('%Y-%m-%d %H:%M:%S'))

            Time = zip(Start_Time1, End_Time1)

            UTC = '0000-00-00 05:30:00'
            y = UTC[:4]
            mo = UTC[5:7]
            da = UTC[8:10]
            h = UTC[11:13]
            m = UTC[14:16]
            s = UTC[17:19]
            d1 = datetime.timedelta(days=(int(
                y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

            Start_Time = []
            End_Time = []
            for s, e in Time:
                y1 = s[:4]
                mo1 = s[5:7]
                da1 = s[8:10]
                h1 = s[11:13]
                m1 = s[14:16]
                s1 = s[17:19]
                d21 = datetime.datetime(year=int(y1), month=int(mo1), day=int(
                    da1), hour=int(h1), minute=int(m1), second=int(s1))

                Start_Time.append(d1 + d21)

                y2 = e[:4]
                mo2 = e[5:7]
                da2 = e[8:10]
                h2 = e[11:13]
                m2 = e[14:16]
                s2 = e[17:19]
                d22 = datetime.datetime(year=int(y2), month=int(mo2), day=int(
                    da2), hour=int(h2), minute=int(m2), second=int(s2))

                End_Time.append(d1 + d22)

                alerts_details = zip(Start_Time, End_Time, alerts)

            return render(request, 'ems-servo/servo_alerts.html', {'alerts_details': alerts_details, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})

        if request.user.is_manager:
            Customer_Name = LoginManager.objects.get(
                manager_name=username).customer_Name
            managername = LoginManager.objects.get(
                manager_name=username).manager_Name
            User_details = LoginUserDetail.objects.all()
            Device_ID = []

            for det in User_details:
                if str(det.Manager_Name) == managername:
                    Device_ID.append(det.Device_ID)

            TR = None
            Count = None
            alerts = None
            myFilter = None
            startdate = None
            enddate = None

            status = ['fuel_level_percentage',
                      'dg_battery_voltage', 'rpm_ctrl',  'rpm']

            if request.method == 'GET' and 'date' in request.GET:
                alerts = Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(request.GET, queryset=alerts)
                alerts = myFilter.qs

                enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
                startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

            elif request.method == 'GET' and 'range' in request.GET:

                if request.GET['time_range'] == 'Last 30 mins':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 hour':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 7 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 12 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 24 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 days':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 5 days':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=5)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 week':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 weeks':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 month':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 months':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=60)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 6 months':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=183)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 year':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=365)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 years':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

                else:

                    alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                        alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    enddate = (Alerts.objects.filter(
                        device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                    startdate = (Alerts.objects.filter(
                        device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                TR = request.GET['time_range']

            else:

                alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                enddate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                startdate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

            status = ['fuel_level_percentage',
                      'dg_battery_voltage', 'rpm_ctrl',  'rpm']

            alert = Alerts.objects.filter(
                device_id__in=Device_ID, alert_open=True).exclude(
                    alert_type_name__in=status)

            Count = len(alert)

            Start_Time1 = []
            End_Time1 = []

            for a in alerts:
                Start_Time1.append(a.created_at.strftime('%Y-%m-%d %H:%M:%S'))
                End_Time1.append(a.updated_at.strftime('%Y-%m-%d %H:%M:%S'))

            Time = zip(Start_Time1, End_Time1)

            UTC = '0000-00-00 05:30:00'
            y = UTC[:4]
            mo = UTC[5:7]
            da = UTC[8:10]
            h = UTC[11:13]
            m = UTC[14:16]
            s = UTC[17:19]
            d1 = datetime.timedelta(days=(int(
                y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

            Start_Time = []
            End_Time = []
            for s, e in Time:
                y1 = s[:4]
                mo1 = s[5:7]
                da1 = s[8:10]
                h1 = s[11:13]
                m1 = s[14:16]
                s1 = s[17:19]
                d21 = datetime.datetime(year=int(y1), month=int(mo1), day=int(
                    da1), hour=int(h1), minute=int(m1), second=int(s1))

                Start_Time.append(d1 + d21)

                y2 = e[:4]
                mo2 = e[5:7]
                da2 = e[8:10]
                h2 = e[11:13]
                m2 = e[14:16]
                s2 = e[17:19]
                d22 = datetime.datetime(year=int(y2), month=int(mo2), day=int(
                    da2), hour=int(h2), minute=int(m2), second=int(s2))

                End_Time.append(d1 + d22)

                alerts_details = zip(Start_Time, End_Time, alerts)

            return render(request, 'ems-servo/servo_alerts.html', {'alerts_details': alerts_details, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})


@ login_required(login_url='login')
def emsservice_history(request, device_id):
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

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
        Stat = Device.objects.get(device_id=device_id).device_status

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

        status = ['fuel_level_percentage',
                  'dg_battery_voltage', 'rpm_ctrl',  'rpm']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

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

        Address1 = Device.objects.get(device_id=device_id).device_location

        Details = LoginEmsServiceHistory.objects.get(device_id=device_id)

        Asset_Details = LoginEmsAsset.objects.get(device_id=device_id)

        EDOI = LoginEmsAsset.objects.get(
            device_id=device_id).ems_date_of_installation

        Contract = LoginEmsServiceHistory.objects.get(
            device_id=device_id).service_contract

        gsm = DevicesInfo.objects.filter(device_id=device_id).last().gsm_signal

        GWDB = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_device_battery

        PS = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_power_status

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

    return render(request, 'ems-servo/servo_asset_service-history.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Contract': Contract, 'EDOI': EDOI, 'Asset_Details': Asset_Details, 'Details': Details, 'Address1': Address1, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'alert_count': alert_count, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id})


@ login_required(login_url='login')
def emsLoadKPI(request, device_id):
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

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
        Stat = Device.objects.get(device_id=device_id).device_status
        Date = datetime.datetime.now()
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

        TR = None
        Count = None
        Details = None
        myFilter = None
        if request.method == 'GET' and 'date' in request.GET:
            Details = DevicesInfo.objects.filter(
                device_id=device_id).exclude(vll_average=0).order_by('-device_time')

            myFilter = KPIFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 hour':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 hours':

                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 7 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 12 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 24 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 days':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 5 days':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 week':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 weeks':

                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 month':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 months':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 6 months':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 year':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 years':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            TR = request.GET['time_range']

        else:
            Details = DevicesInfo.objects.filter(
                device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(vll_average=0).order_by('-device_time')

            myFilter = KPIFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        WT = []
        EO = []
        CA = []
        CR = []
        CY = []
        CB = []
        Time = []
        Time1 = []

        for det in Details:
            Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
            # WT.append(round(det.energy_output_kw_total, 2))
            EO.append(round(det.energy_output_kva, 2))
            CA.append(round(det.current_average, 2))
            CR.append(round(det.current_r_phase, 2))
            CY.append(round(det.current_y_phase, 2))
            CB.append(round(det.current_b_phase, 2))

        # WT.reverse()
        EO.reverse()
        CA.reverse()
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

        if Count < 1500:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -3)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        elif Count < 2880:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -3)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        elif Count < 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -3)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        elif Count >= 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        # status = ['power_factor', 'gateway_device_battery', 'fuel_level_percentage', 'gsm_signal', 'energy_output_kw_total', 'dg_battery_voltage', 'room_temperature', 'frequency',
        #           'rpm_ctrl', 'current_b_phase', 'vll_average', 'energy_output_kva', 'current_r_phase', 'rpm', 'current_y_phase', ]

        # alerts = Alerts.objects.filter(
        #     device_id=device_id).exclude(alert_type_name__in=status).order_by('-created_at')

        status = ['fuel_level_percentage',
                  'dg_battery_voltage', 'rpm_ctrl',  'rpm']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

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

        EDOI = LoginEmsAsset.objects.get(
            device_id=device_id).ems_date_of_installation

        Name = "Load Side KPI"

        gsm = DevicesInfo.objects.filter(device_id=device_id).last().gsm_signal

        GWDB = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_device_battery

        PS = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_power_status

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

        return render(request, 'ems-servo/servo_kpi_load-side.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'EDOI': EDOI, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'alert_count': alert_count, 'WT': WT, 'EO': EO, 'Time': Time, 'TR': TR, 'myFilter': myFilter, 'CA': CA, 'CR': CR, 'CY': CY, 'CB': CB, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def emsEnergyPara(request, device_id):
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

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
        Stat = Device.objects.get(device_id=device_id).device_status
        Date = datetime.datetime.now()
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

        TR = None
        Count = None
        Details = None
        myFilter = None
        if request.method == 'GET' and 'date' in request.GET:
            Details = DevicesInfo.objects.filter(
                device_id=device_id).exclude(vll_average=0).order_by('-device_time')

            myFilter = KPIFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 hour':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 hours':

                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 7 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 12 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 24 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 days':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 5 days':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 week':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 weeks':

                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 month':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 months':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 6 months':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 year':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 years':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).exclude(vll_average=0).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            TR = request.GET['time_range']

        else:
            Details = DevicesInfo.objects.filter(
                device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(vll_average=0).order_by('-device_time')

            myFilter = KPIFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        VLL = []
        VLN = []
        PF = []
        Time1 = []
        Time = []

        for det in Details:
            Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
            VLN.append(round(det.vln_average, 2))
            VLL.append(round(det.vll_average, 2))
            PF.append(round(det.power_factor, 2))

        VLN.reverse()
        VLL.reverse()
        PF.reverse()

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

        if Count < 1500:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
            for t in TimeN:
                Time.append(t[sl2]+"-"+t[sl1]+"/"+t[sl3])

            Time.reverse()

        elif Count < 2880:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
            for t in TimeN:
                Time.append(t[sl2]+"-"+t[sl1]+"/"+t[sl3])

            Time.reverse()

        elif Count < 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -3)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        elif Count >= 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        # status = ['power_factor', 'energy_output_kw_total', 'dg_battery_voltage', 'room_temperature', 'frequency',
        #           'rpm_ctrl', 'current_b_phase', 'vll_average', 'energy_output_kva', 'current_r_phase', 'rpm', 'current_y_phase', ]

        # alerts = Alerts.objects.filter(
        #     device_id=device_id).exclude(alert_type_name__in=status).order_by('-created_at')

        status = ['fuel_level_percentage',
                  'dg_battery_voltage', 'rpm_ctrl',  'rpm']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

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

        EDOI = LoginEmsAsset.objects.get(
            device_id=device_id).ems_date_of_installation

        Name = "Energy Parameter KPI"

        gsm = DevicesInfo.objects.filter(device_id=device_id).last().gsm_signal

        GWDB = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_device_battery

        PS = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_power_status

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

        return render(request, 'ems-servo/servo_kpi_energy-parameters.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'EDOI': EDOI, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'PF': PF, 'VLN': VLN, 'VLL': VLL,  'alert_count': alert_count, 'Time': Time,  'TR': TR, 'myFilter': myFilter,  'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def emsDeviceInfoKPI(request, device_id):
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

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
        Stat = Device.objects.get(device_id=device_id).device_status
        Date = datetime.datetime.now()
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

        TR = None
        Count = None
        Details = None
        myFilter = None
        if request.method == 'GET' and 'date' in request.GET:
            Details = DevicesInfo.objects.filter(
                device_id=device_id).order_by('-device_time')

            myFilter = KPIFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 hour':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 hours':

                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 7 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 12 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 24 hours':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 days':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 5 days':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 week':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 weeks':

                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 month':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 months':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 6 months':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 year':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 years':
                Details = DevicesInfo.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).order_by('-device_time')

                myFilter = KPIFilter(request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            TR = request.GET['time_range']

        else:
            Details = DevicesInfo.objects.filter(
                device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-device_time')

            myFilter = KPIFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        GSM = []
        GB = []
        Time = []
        Time1 = []
        PS1 = []
        BV1 = []

        for det in Details:
            Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
            GSM.append(round(det.gsm_signal, 2))
            GB.append(round(det.gateway_device_battery, 2))
            PS1.append(det.gateway_power_status)
            BV1.append(det.gateway_device_battery)

        GSM.reverse()
        GB.reverse()
        PS1.reverse()
        BV1.reverse()

        if len(PS1) == 0:
            PS = 'NA'
        else:
            PS = PS1[-1]

        if len(BV1) == 0:
            BatteryVoltage = 0
        else:
            BatteryVoltage = BV1[-1]

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

        if len(GSM) == 0:
            GSMSignal = 0
        else:
            GSMSignal = GSM[-1]

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

        if Count < 1500:
            sl = slice(11, -3)
            for t in TimeN:
                Time.append(t[sl])

            Time.reverse()

        elif Count < 2880:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -3)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        elif Count < 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -3)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

            Time.reverse()

        elif Count >= 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        # status = ['power_factor', 'gateway_device_battery', 'fuel_level_percentage', 'gsm_signal', 'energy_output_kw_total', 'dg_battery_voltage', 'room_temperature', 'frequency',
        #           'rpm_ctrl', 'current_b_phase', 'vll_average', 'energy_output_kva', 'current_r_phase', 'rpm', 'current_y_phase', ]

        # alerts = Alerts.objects.filter(
        #     device_id=device_id).exclude(alert_type_name__in=status).order_by('-created_at')

        status = ['fuel_level_percentage',
                  'dg_battery_voltage', 'rpm_ctrl',  'rpm']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

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

        EDOI = LoginEmsAsset.objects.get(
            device_id=device_id).ems_date_of_installation

        Name = "Device Info KPI"

        gsm = DevicesInfo.objects.filter(device_id=device_id).last().gsm_signal

        GWDB = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_device_battery

        PS = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_power_status

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

        return render(request, 'ems-servo/servo_kpi_device-info.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'EDOI': EDOI, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'GSMSignal': GSMSignal, 'PowerStatus': PowerStatus, 'BatteryVoltage': BatteryVoltage, 'GSM': GSM, 'GB': GB, 'alert_count': alert_count, 'Time': Time, 'myFilter': myFilter, 'TR': TR, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def emsdevice_alert(request, device_id):
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

        elif request.user.is_customer:
            Customer_Name = LoginCustomer.objects.get(
                customer_name=username).customer_name

        Cit = LoginUserDetail.objects.get(device_id=device_id).city
        Loc = LoginUserDetail.objects.get(device_id=device_id).location
        Rat = LoginEmsAsset.objects.get(device_id=device_id).rating_in_kva
        Stat = Device.objects.get(device_id=device_id).device_status

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

        TR = None
        Count = None
        alerts = None
        myFilter = None
        startdate = None
        enddate = None

        status = ['fuel_level_percentage',
                  'dg_battery_voltage', 'rpm_ctrl',  'rpm']

        if request.method == 'GET' and 'date' in request.GET:
            alerts = Alerts.objects.filter(
                device_id=device_id).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

            myFilter = DeviceAlertFilter(request.GET, queryset=alerts)
            alerts = myFilter.qs

            enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
            startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

        elif request.method == 'GET' and 'range' in request.GET:

            status = ['fuel_level_percentage',
                      'dg_battery_voltage', 'rpm_ctrl',  'rpm']

            if request.GET['time_range'] == 'Last 30 mins':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now().strftime(
                    '%d-%m-%Y')).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now().strftime(
                    '%d-%m-%Y')).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')
            else:

                alerts = Alerts.objects.filter(
                    device_id=device_id).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                startdate = (Alerts.objects.filter(
                    device_id=device_id).order_by('-created_at').exclude(alert_type_name__in=status).first().updated_at).strftime('%d-%m-%Y')
                enddate = (Alerts.objects.filter(
                    device_id=device_id).order_by('-created_at').exclude(alert_type_name__in=status).last().created_at).strftime('%d-%m-%Y')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

            TR = request.GET['time_range']

        else:
            status = ['fuel_level_percentage',
                      'dg_battery_voltage', 'rpm_ctrl',  'rpm']

            alerts = Alerts.objects.filter(
                device_id=device_id).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

            startdate = (Alerts.objects.filter(
                device_id=device_id).order_by('-created_at').exclude(alert_type_name__in=status).first().updated_at).strftime('%d-%m-%Y')
            enddate = (Alerts.objects.filter(
                device_id=device_id).order_by('-created_at').exclude(alert_type_name__in=status).last().created_at).strftime('%d-%m-%Y')

            myFilter = DeviceAlertFilter(
                request.GET, queryset=alerts)
            alerts = myFilter.qs

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        Start_Time1 = []
        End_Time1 = []

        for a in alerts:
            Start_Time1.append(a.created_at.strftime('%Y-%m-%d %H:%M:%S'))
            End_Time1.append(a.updated_at.strftime('%Y-%m-%d %H:%M:%S'))

        Time = zip(Start_Time1, End_Time1)

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

        Start_Time = []
        End_Time = []
        for s, e in Time:
            y1 = s[:4]
            mo1 = s[5:7]
            da1 = s[8:10]
            h1 = s[11:13]
            m1 = s[14:16]
            s1 = s[17:19]
            d21 = datetime.datetime(year=int(y1), month=int(mo1), day=int(
                da1), hour=int(h1), minute=int(m1), second=int(s1))

            Start_Time.append(d1 + d21)

            y2 = e[:4]
            mo2 = e[5:7]
            da2 = e[8:10]
            h2 = e[11:13]
            m2 = e[14:16]
            s2 = e[17:19]
            d22 = datetime.datetime(year=int(y2), month=int(mo2), day=int(
                da2), hour=int(h2), minute=int(m2), second=int(s2))

            End_Time.append(d1 + d22)

            alerts_details = zip(Start_Time, End_Time, alerts)

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

        EDOI = LoginEmsAsset.objects.get(
            device_id=device_id).ems_date_of_installation

        # http://openweathermap.org/img/w/{{icon}}.png

        gsm = DevicesInfo.objects.filter(device_id=device_id).last().gsm_signal

        GWDB = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_device_battery

        PS = DevicesInfo.objects.filter(
            device_id=device_id).last().gateway_power_status

        PowerStatus = 0
        if PS == 1:
            PowerStatus = 'Healthy'
        else:
            PowerStatus = 'Battery'

        return render(request, 'ems-servo/servo_alert_device.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'EDOI': EDOI, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'alerts_details': alerts_details, 'alert_count': alert_count,  'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff,  'current_time': current_time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, })
