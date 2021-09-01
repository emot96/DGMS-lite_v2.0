from django.core.checks.messages import CRITICAL, ERROR
from django.db.models.aggregates import Max
from django.db.models.fields import DecimalField
from django.db.models.lookups import In
from django.db.models.manager import Manager
from django.forms.widgets import PasswordInput
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Avg, Sum, Max
import datetime
from .forms import *
from django import http
from .filters import *
from django.core.files.storage import FileSystemStorage
import json
import urllib.request
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from .serializers import *
# Create your views here.


@api_view(['GET'])
def automation(request):

    details = Automation.objects.all()
    serializer = AutomationSerializer(details, many=True)

    return Response(serializer.data)


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'dgms/index.html')


def login(request):
    return render(request, 'dgms/login.html')


def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("dashboard")
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    # else:
        # return render(request, 'dashboard.html')


@login_required(login_url='login')
def dashboard(request):
    username = None
    email = None
    usertype = None
    temperature = None
    description = None
    icon = None
    CustomerID = []
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_user:
            device_id = User_Detail.objects.get(
                User_Name=username).Device_ID
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
            Cit = User_Detail.objects.get(Device_ID=device_id).City
            Loc = User_Detail.objects.get(Device_ID=device_id).Location
            Rat = Device.objects.get(device_id=device_id).device_rating
            Stat = Device.objects.get(device_id=device_id).device_status
            Date = datetime.datetime.now()
            try:
                Fuel2 = round(DevicesInfo.objects.filter(
                     device_id=device_id).exclude(fuel_level_litre=0).last().fuel_level_litre, 2)
            except:
                  Fuel2 = 0
           
            Tank_Size = Asset.objects.get(
                Device_ID=device_id).Diesel_Tank_Size
            Fuel_Per = round((Fuel2/Tank_Size)*100, 2)
            Run = DevicesInfo.objects.filter(device_id=device_id).exclude(
                dg_runtime_seconds=0).last()
            if Run != None:
                Run = Run.dg_runtime_seconds
            else:
                
                Run = DevicesInfo.objects.filter(device_id=device_id).exclude(
                    runtime_second_ctrl=0).last()
                if Run != None:
                    Run = Run.runtime_second_ctrl
             
          
            PreRH = Before_DGMA_INSTALLATION.objects.get(
                Device_ID=device_id).Previous_Run_Hour
            Run = Run + int(PreRH)
            seconds = Run
            # seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            hh = "%d:%02d:%02d" % (hour, minutes, seconds)

            UG = round(DevicesInfo.objects.filter(device_id=device_id).exclude(
                unit_generated_kwh=0).last().unit_generated_kwh, 2)
            PreUG = Before_DGMA_INSTALLATION.objects.get(
                Device_ID=device_id).Units_Generated
            UG = UG + float(PreUG)

            CarbonFootPrint = DeviceOperational.objects.filter(
                device_id=device_id).aggregate(Sum('carbon_footprint'))
            Carbon_Foot_Print = round(
                float(CarbonFootPrint['carbon_footprint__sum']), 2)

            BV = DevicesInfo.objects.filter(device_id=device_id).exclude(
                dg_battery_voltage=0).last().dg_battery_voltage

            FuelConsumed = DeviceOperational.objects.filter(
                device_id=device_id).aggregate(Sum('fuel_consumed'))
            Fuel_Consumed = float(FuelConsumed['fuel_consumed__sum'])
            AvgFC = round(Fuel_Consumed/(Run*0.000277778), 2)

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

            MaxDL = DeviceOperational.objects.filter(
                device_id=device_id).aggregate(Max('maximum_demand_load'))
            MaxDLoad = round(float(MaxDL['maximum_demand_load__max']), 2)

            DeviceC = DeviceCounterView.objects.filter(
                device_id=device_id)[0].counter

            RT = round(DevicesInfo.objects.filter(device_id=device_id).exclude(
                room_temperature=0).last().room_temperature, 2)

            if Stat == 'ON':
                now = datetime.datetime.now()
                current_time = now.strftime('%Y-%m-%d %H:%M:%S')
                format = '%Y-%m-%d %H:%M:%S'
                Current_T = datetime.datetime.strptime(
                    current_time, format)
                Start_time = DeviceOperational.objects.filter(
                    device_id=device_id).last().start_time
                diff = Current_T - Start_time
            else:
                now = datetime.datetime.now()
                current_time = now.strftime('%Y-%m-%d %H:%M:%S')
                format = '%Y-%m-%d %H:%M:%S'
                Current_T = datetime.datetime.strptime(
                    current_time, format)
                Start_time = DeviceOperational.objects.filter(
                    device_id=device_id).last().start_time
                End_time = DeviceOperational.objects.filter(
                    device_id=device_id).last().end_time
                diff = Current_T - End_time

            Fuel_Level = DevicesInfo.objects.filter(
                device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-device_time')

            Fuel1 = []
            Time1 = []
            Time2 = []
            Time = []
            Level = []
            for Fuel in Fuel_Level:
                Fuel1.append(Fuel.fuel_level_litre)
                Time2.append(Fuel.device_time.strftime(
                    '%Y-%m-%d %H:%M:%S'))

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

            for t in Time2:
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

            Fuel1.reverse()
            Time.reverse()

            alerts = Alerts.objects.filter(
                device_id=device_id, alert_open=True).order_by('-created_at')

            alert_count = len(alerts)

            DDOI = DGMS_Device_Info.objects.get(
                Device_ID=device_id).DGMS_Date_Of_Installation

            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
            r = requests.get(url.format(Cit)).json()
            temperature = round((float(r['main']['temp'])-32)*0.555, 2)
            description = r['weather'][0]['description']
            icon = r['weather'][0]['icon']

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

            asset_info = Asset.objects.get(Device_ID=device_id)

            service_info = Service_History.objects.get(Device_ID=device_id)

            DTNS = (Service_History.objects.get(
                Device_ID=device_id).Next_Service_Date) - (datetime.date.today())

            return render(request, 'dgms/dgms_dashboard_device.html', {'DTNS': DTNS, 'service_info': service_info, 'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'temperature': temperature, 'description': description, 'icon': icon, 'Fuel2': Fuel2, 'DDOI': DDOI, 'alert_count': alert_count, 'Fuel1': Fuel1, 'Time': Time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Fuel2': Fuel2, 'Tank_Size': Tank_Size, 'Fuel_Per': Fuel_Per, 'hh': hh, 'UG': UG, 'Carbon_Foot_Print': Carbon_Foot_Print, 'BV': BV, 'AvgFC': AvgFC, 'Energy_OA': Energy_OA, 'MaxDLoad': MaxDLoad, 'DeviceC': DeviceC, 'asset_info': asset_info, 'Star': Star, 'RT': RT, 'diff': diff, 'Level': Level, 'Fuel1': Fuel1, 'Time': Time})

        elif request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name
            Customer_ID = Customer.objects.get(
                Customer_Name=Customer_Name).Customer_ID
            managername = Manager.objects.get(
                Manager_Name=username).Manager_Name
            User_details = User_Detail.objects.all()
            DeviceID = []

            for det in User_details:
                if str(det.Manager_Name) == managername:
                    DeviceID.append(det.Device_ID)

            Device_ID = Device.objects.filter(device_id__in=DeviceID)

            myFilter = DashboardFilter(
                request.GET, queryset=Device_ID, request=request)
            Device_ID = myFilter.qs

            DeviceID = []
            for i in Device_ID:
                DeviceID.append(i.device_id)

            Total = 0
            Live = 0
            Offline = 0
            InUse = 0
            Capacity = 0

            Total = Device.objects.filter(device_id__in=DeviceID).count()
            Live = Device.objects.filter(
                device_id__in=DeviceID, device_status='ON').count()
            Offline = Device.objects.filter(
                device_id__in=DeviceID, device_status='OFF').count()
            Capacity = Device.objects.filter(
                device_id__in=DeviceID).aggregate(Sum('device_rating'))
            Capacity = Capacity['device_rating__sum']
            InUse = Device.objects.filter(
                device_id__in=DeviceID, device_status='ON').aggregate(Sum('device_rating'))
            InUse = InUse['device_rating__sum']
            if InUse == None:
                InUse = 0

            Fuel__Consumed = 0
            Fuel__Cost = 0
            Carbon_Foot__Print = 0
            Location = []
            State = []
            City = []
            Status = []
            Rating = []
            PreRH = []
            RunHour = []
            UnitGen = []
            FuelCon = []
            CarbonFP = []
            FuelC = []
            CPU = []
            EnergyOA = []
            MaxDemLoad = []
            Star = []
            Diesel = []
            Energy = []
            for j in DeviceID:
                FuelConsumed = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Sum('fuel_consumed'))
                FuelCost = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Sum('fuel_cost'))
                CarbonFootPrint = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Sum('carbon_footprint'))
                PreFuelCon = Before_DGMA_INSTALLATION.objects.get(
                    Device_ID=j).Previous_Fuel_Consumed
                Fuel_Consumed = float(
                    FuelConsumed['fuel_consumed__sum']) + float(PreFuelCon)
                FuelCon.append(round(Fuel_Consumed, 2))
                Fuel__Consumed = Fuel_Consumed + Fuel__Consumed
                Fuel_Cost = float(FuelCost['fuel_cost__sum'])
                FuelC.append(round(Fuel_Cost))
                Fuel__Cost = Fuel_Cost + Fuel__Cost
                Carbon_Foot_Print = float(
                    CarbonFootPrint['carbon_footprint__sum'])
                CarbonFP.append(round(Carbon_Foot_Print, 2))
                Carbon_Foot__Print = Carbon_Foot_Print + Carbon_Foot__Print
                Fuel__Consumed = round(Fuel__Consumed, 2)
                Fuel__Cost = round(Fuel__Cost, 2)
                Carbon_Foot__Print = round(Carbon_Foot__Print, 2)
                Sta = User_Detail.objects.filter(
                    Device_ID=j)[0].State
                Cit = User_Detail.objects.filter(
                    Device_ID=j)[0].City
                Loc = User_Detail.objects.filter(
                    Device_ID=j)[0].Location
                Stat = Device.objects.filter(device_id=j)[0].device_status
                Rat = Asset.objects.get(Device_ID=j).Rating_In_KVA
                Run = DevicesInfo.objects.filter(device_id=j).exclude(
                    dg_runtime_seconds=0).last()
                RunHour1 = []
                if Run != None:
                    Run = Run.dg_runtime_seconds
                    RunHour1.append(Run)
                RunH = DevicesInfo.objects.filter(device_id=j).exclude(
                    runtime_second_ctrl=0).last()
                if RunH != None:
                    RunH = RunH.runtime_second_ctrl
                    RunHour1.append(RunH)
                PreRH = []
                PreRH.append(int(Before_DGMA_INSTALLATION.objects.get(
                    Device_ID=j).Previous_Run_Hour))
                RunHour2 = zip(RunHour1, PreRH)
                for rh, prh in RunHour2:
                    seconds = rh + prh
                    # seconds = seconds % (24 * 3600)
                    hour = seconds // 3600
                    seconds %= 3600
                    minutes = seconds // 60
                    seconds %= 60
                    hh = "%d:%02d:%02d" % (hour, minutes, seconds)
                    RunHour.append(hh)

                UG = DevicesInfo.objects.filter(device_id=j).exclude(
                    unit_generated_kwh=0).last()
                PreUG = Before_DGMA_INSTALLATION.objects.get(
                    Device_ID=j).Units_Generated
                UG = round(UG.unit_generated_kwh, 2) + float(PreUG)
                UnitGen.append(UG)
                Cost_Per_Unit = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Avg('per_unit_cost'))
                Cost_Per_U = float(Cost_Per_Unit['per_unit_cost__avg'])
                Cost_Per_U = round(Cost_Per_U, 2)
                CPU.append(Cost_Per_U)
                Efficency = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Avg('efficiency'))
                Energy_OA = round(float(Efficency['efficiency__avg']), 2)
                EnergyOA.append(Energy_OA)
                MaxDL = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Max('maximum_demand_load'))
                MaxDLoad = round(float(
                    MaxDL['maximum_demand_load__max']), 2)
                MaxDemLoad.append(MaxDLoad)

                if Energy_OA < 25:
                    Star.append(1)
                elif 25 < Energy_OA < 40:
                    Star.append(2)
                elif 40 < Energy_OA < 50:
                    Star.append(3)
                elif 50 < Energy_OA < 60:
                    Star.append(4)
                else:
                    Star.append(5)

                Rating.append(Rat)
                State.append(Sta)
                City.append(Cit)
                Location.append(Loc)
                Status.append(Stat)

                for c in City:
                    EnergyPrice = Price.objects.get(
                        Location=c).Energy_Price
                    DieselPrice = Price.objects.get(
                        Location=c).Diesel_Price
                    Diesel.append(DieselPrice)
                    Energy.append(EnergyPrice)

            UserDetail = zip(State, City, Location, Status, Rating, UnitGen, FuelCon, CarbonFP,
                             FuelC, CPU, EnergyOA, MaxDemLoad, Star, Diesel, Energy, RunHour, DeviceID)

            status = ['power_factor']

            alert = Alerts.objects.filter(
                device_id__in=DeviceID, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
            alert_count = len(alert)

            return render(request, 'dgms/dgms_dashboard.html', {'myFilter': myFilter, 'alert_count': alert_count, 'username': username, 'Customer_Name': Customer_Name, 'Total': Total, 'Live': Live, 'Offline': Offline, 'Capacity': Capacity, 'InUse': InUse, 'Fuel__Consumed': Fuel__Consumed, 'Fuel__Cost': Fuel__Cost, 'Carbon_Foot__Print': Carbon_Foot__Print, 'UserDetail': UserDetail})

        elif request.user.is_superuser:
            Customer_Name = 'Admin'
            Customer_Details = Customer.objects.all()
            for Cus in Customer_Details:
                CustomerID.append(Cus.Customer_ID)
            Total = 0
            Live = 0
            Offline = 0
            InUse = 0
            Capacity = 0
            DeviceID = []
            for Customer_ID in CustomerID:
                Total1 = Device.objects.filter(account_id=Customer_ID).count()
                Total = Total1 + Total
                Live1 = Device.objects.filter(
                    account_id=Customer_ID, device_status='ON').count()
                Live = Live1 + Live
                Offline1 = Device.objects.filter(
                    account_id=Customer_ID, device_status='OFF').count()
                Offline = Offline1 + Offline
                Capacity1 = Device.objects.filter(
                    account_id=Customer_ID).aggregate(Sum('device_rating'))
                Capacity1 = float(Capacity1['device_rating__sum'])
                Capacity = Capacity1 + Capacity
                InUse1 = Device.objects.filter(
                    account_id=Customer_ID, device_status='ON').aggregate(Sum('device_rating'))
                InUse1 = InUse1['device_rating__sum']
                if InUse1 == None:
                    InUse1 = 0
                InUse = InUse1 + InUse
                Device_ID = Device.objects.filter(account_id=Customer_ID)
                for i in range(Total1):
                    a = Device_ID[i].device_id
                    DeviceID.append(a)

                Fuel__Consumed = 0
                Fuel__Cost = 0
                Carbon_Foot__Print = 0
                Location = []
                State = []
                City = []
                Status = []
                Rating = []
                PreRH = []
                RunHour = []
                UnitGen = []
                FuelCon = []
                CarbonFP = []
                FuelC = []
                CPU = []
                EnergyOA = []
                MaxDemLoad = []
                Star = []
                Diesel = []
                Energy = []
                for j in DeviceID:
                    FuelConsumed = DeviceOperational.objects.filter(
                        device_id=j).aggregate(Sum('fuel_consumed'))
                    FuelCost = DeviceOperational.objects.filter(
                        device_id=j).aggregate(Sum('fuel_cost'))
                    CarbonFootPrint = DeviceOperational.objects.filter(
                        device_id=j).aggregate(Sum('carbon_footprint'))
                    PreFuelCon = Before_DGMA_INSTALLATION.objects.get(
                        Device_ID=j).Previous_Fuel_Consumed
                    Fuel_Consumed = float(
                        FuelConsumed['fuel_consumed__sum']) + float(PreFuelCon)
                    FuelCon.append(round(Fuel_Consumed, 2))
                    Fuel__Consumed = Fuel_Consumed + Fuel__Consumed
                    Fuel_Cost = float(FuelCost['fuel_cost__sum'])
                    FuelC.append(round(Fuel_Cost))
                    Fuel__Cost = Fuel_Cost + Fuel__Cost
                    Carbon_Foot_Print = float(
                        CarbonFootPrint['carbon_footprint__sum'])
                    CarbonFP.append(round(Carbon_Foot_Print, 2))
                    Carbon_Foot__Print = Carbon_Foot_Print + Carbon_Foot__Print
                    Fuel__Consumed = round(Fuel__Consumed, 2)
                    Fuel__Cost = round(Fuel__Cost, 2)
                    Carbon_Foot__Print = round(Carbon_Foot__Print, 2)
                    Sta = User_Detail.objects.filter(
                        Device_ID=j)[0].State
                    Cit = User_Detail.objects.filter(
                        Device_ID=j)[0].City
                    Loc = User_Detail.objects.filter(
                        Device_ID=j)[0].Location
                    Stat = Device.objects.filter(device_id=j)[0].device_status
                    Rat = Device.objects.filter(device_id=j)[0].device_rating
                    Run = DevicesInfo.objects.filter(device_id=j).exclude(
                        dg_runtime_seconds=0).last()
                    RunHour1 = []
                    if Run != None:
                        Run = Run.dg_runtime_seconds
                        RunHour1.append(Run)
                    RunH = DevicesInfo.objects.filter(device_id=j).exclude(
                        runtime_second_ctrl=0).last()
                    if RunH != None:
                        RunH = RunH.runtime_second_ctrl
                        RunHour1.append(RunH)

                    PreRH.append(int(Before_DGMA_INSTALLATION.objects.get(
                        Device_ID=j).Previous_Run_Hour))
                    RunHour2 = zip(RunHour1, PreRH)
                    for rh, prh in RunHour2:
                        seconds = rh + prh
                        # seconds = seconds % (24 * 3600)
                        hour = seconds // 3600
                        seconds %= 3600
                        minutes = seconds // 60
                        seconds %= 60
                        hh = "%d:%02d:%02d" % (hour, minutes, seconds)
                        RunHour.append(hh)

                    UG = DevicesInfo.objects.filter(device_id=j).exclude(
                        unit_generated_kwh=0).last()
                    PreUG = Before_DGMA_INSTALLATION.objects.get(
                        Device_ID=j).Units_Generated
                    UG = round(UG.unit_generated_kwh, 2) + float(PreUG)
                    UnitGen.append(UG)
                    Cost_Per_Unit = DeviceOperational.objects.filter(
                        device_id=j).aggregate(Avg('per_unit_cost'))
                    Cost_Per_U = float(Cost_Per_Unit['per_unit_cost__avg'])
                    Cost_Per_U = round(Cost_Per_U, 2)
                    CPU.append(Cost_Per_U)
                    Efficency = DeviceOperational.objects.filter(
                        device_id=j).aggregate(Avg('efficiency'))
                    Energy_OA = round(float(Efficency['efficiency__avg']), 2)
                    EnergyOA.append(Energy_OA)
                    MaxDL = DeviceOperational.objects.filter(
                        device_id=j).aggregate(Max('maximum_demand_load'))
                    MaxDLoad = round(float(
                        MaxDL['maximum_demand_load__max']), 2)
                    MaxDemLoad.append(MaxDLoad)
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

                    for c in City:
                        EnergyPrice = Price.objects.get(
                            Location=c).Energy_Price
                        DieselPrice = Price.objects.get(
                            Location=c).Diesel_Price
                        Diesel.append(DieselPrice)
                        Energy.append(EnergyPrice)

                UserDetail = zip(State, City, Location,
                                 Status, Rating, UnitGen, FuelCon, CarbonFP, FuelC, CPU, EnergyOA, MaxDemLoad, Star, Diesel, Energy, RunHour, DeviceID)

                status = ['power_factor']

                alert = Alerts.objects.filter(
                    alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
                alert_count = len(alert)

            return render(request, 'dgms/dashboard1.html', {'alert_count': alert_count, 'username': username, 'Customer_Name': Customer_Name, 'Total': Total, 'Live': Live, 'Offline': Offline, 'Capacity': Capacity, 'InUse': InUse, 'Fuel__Consumed': Fuel__Consumed, 'Fuel__Cost': Fuel__Cost, 'Carbon_Foot__Print': Carbon_Foot__Print, 'UserDetail': UserDetail})

        elif request.user.is_customer:

            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
            Customer_ID = Customer.objects.get(
                Customer_Name=username).Customer_ID
            Total = Device.objects.filter(account_id=Customer_ID).count()
            Live = Device.objects.filter(
                account_id=Customer_ID, device_status='ON').count()
            Offline = Device.objects.filter(
                account_id=Customer_ID, device_status='OFF').count()
            Capacity = Device.objects.filter(
                account_id=Customer_ID).aggregate(Sum('device_rating'))
            Capacity = Capacity['device_rating__sum']
            InUse = Device.objects.filter(
                account_id=Customer_ID, device_status='ON').aggregate(Sum('device_rating'))
            InUse = InUse['device_rating__sum']
            if InUse == None:
                InUse = 0
            Device_ID = Device.objects.filter(account_id=Customer_ID)

            myFilter = DashboardFilter(
                request.GET, queryset=Device_ID, request=request)
            Device_ID = myFilter.qs

            DeviceID = []
            for i in Device_ID:
                DeviceID.append(i.device_id)

            Fuel__Consumed = 0
            Fuel__Cost = 0
            Carbon_Foot__Print = 0
            Location = []
            State = []
            City = []
            Status = []
            Rating = []
            PreRH = []
            RunHour = []
            UnitGen = []
            FuelCon = []
            CarbonFP = []
            FuelC = []
            CPU = []
            EnergyOA = []
            MaxDemLoad = []
            Star = []
            Diesel = []
            Energy = []
            for j in DeviceID:
                FuelConsumed = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Sum('fuel_consumed'))
                FuelCost = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Sum('fuel_cost'))
                CarbonFootPrint = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Sum('carbon_footprint'))
                PreFuelCon = Before_DGMA_INSTALLATION.objects.get(
                    Device_ID=j).Previous_Fuel_Consumed
                Fuel_Consumed = float(
                    FuelConsumed['fuel_consumed__sum']) + float(PreFuelCon)
                FuelCon.append(round(Fuel_Consumed, 2))
                Fuel__Consumed = Fuel_Consumed + Fuel__Consumed
                Fuel_Cost = float(FuelCost['fuel_cost__sum'])
                FuelC.append(round(Fuel_Cost))
                Fuel__Cost = Fuel_Cost + Fuel__Cost
                Carbon_Foot_Print = float(
                    CarbonFootPrint['carbon_footprint__sum'])
                CarbonFP.append(round(Carbon_Foot_Print, 2))
                Carbon_Foot__Print = Carbon_Foot_Print + Carbon_Foot__Print
                Fuel__Consumed = round(Fuel__Consumed, 2)
                Fuel__Cost = round(Fuel__Cost, 2)
                Carbon_Foot__Print = round(Carbon_Foot__Print, 2)
                Sta = User_Detail.objects.filter(
                    Device_ID=j)[0].State
                Cit = User_Detail.objects.filter(
                    Device_ID=j)[0].City
                Loc = User_Detail.objects.filter(
                    Device_ID=j)[0].Location
                Stat = Device.objects.filter(device_id=j)[0].device_status
                Rat = Asset.objects.get(Device_ID=j).Rating_In_KVA
                Run = DevicesInfo.objects.filter(device_id=j).exclude(
                    dg_runtime_seconds=0).last()
                RunHour1 = []
                if Run != None:
                    Run = Run.dg_runtime_seconds
                    RunHour1.append(Run)
                RunH = DevicesInfo.objects.filter(device_id=j).exclude(
                    runtime_second_ctrl=0).last()
                if RunH != None:
                    RunH = RunH.runtime_second_ctrl
                    RunHour1.append(RunH)
                PreRH = []
                PreRH.append(int(Before_DGMA_INSTALLATION.objects.get(
                    Device_ID=j).Previous_Run_Hour))
                RunHour2 = zip(RunHour1, PreRH)
                for rh, prh in RunHour2:
                    seconds = rh + prh
                    # seconds = seconds % (24 * 3600)
                    hour = seconds // 3600
                    seconds %= 3600
                    minutes = seconds // 60
                    seconds %= 60
                    hh = "%d:%02d:%02d" % (hour, minutes, seconds)
                    RunHour.append(hh)

                UG = DevicesInfo.objects.filter(device_id=j).exclude(
                    unit_generated_kwh=0).last()
                PreUG = Before_DGMA_INSTALLATION.objects.get(
                    Device_ID=j).Units_Generated
                UG = round(UG.unit_generated_kwh, 2) + float(PreUG)
                UnitGen.append(UG)
                Cost_Per_Unit = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Avg('per_unit_cost'))
                Cost_Per_U = float(Cost_Per_Unit['per_unit_cost__avg'])
                Cost_Per_U = round(Cost_Per_U, 2)
                CPU.append(Cost_Per_U)
                Efficency = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Avg('efficiency'))
                Energy_OA = round(float(Efficency['efficiency__avg']), 2)
                EnergyOA.append(Energy_OA)
                MaxDL = DeviceOperational.objects.filter(
                    device_id=j).aggregate(Max('maximum_demand_load'))
                MaxDLoad = round(float(
                    MaxDL['maximum_demand_load__max']), 2)
                MaxDemLoad.append(MaxDLoad)

                if Energy_OA < 25:
                    Star.append(1)
                elif 25 < Energy_OA < 40:
                    Star.append(2)
                elif 40 < Energy_OA < 50:
                    Star.append(3)
                elif 50 < Energy_OA < 60:
                    Star.append(4)
                else:
                    Star.append(5)

                Rating.append(Rat)
                State.append(Sta)
                City.append(Cit)
                Location.append(Loc)
                Status.append(Stat)

                for c in City:
                    EnergyPrice = Price.objects.get(
                        Location=c).Energy_Price
                    DieselPrice = Price.objects.get(
                        Location=c).Diesel_Price
                    Diesel.append(DieselPrice)
                    Energy.append(EnergyPrice)

            UserDetail = zip(State, City, Location,
                             Status, Rating, UnitGen, FuelCon, CarbonFP, FuelC, CPU, EnergyOA, MaxDemLoad, Star, Diesel, Energy, RunHour, DeviceID)

            status = ['power_factor']

            alert = Alerts.objects.filter(
                device_id__in=Device_ID, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
            alert_count = len(alert)

        return render(request, 'dgms/dgms_dashboard.html', {'myFilter': myFilter, 'alert_count': alert_count, 'username': username, 'Customer_Name': Customer_Name, 'Total': Total, 'Live': Live, 'Offline': Offline, 'Capacity': Capacity, 'InUse': InUse, 'Fuel__Consumed': Fuel__Consumed, 'Fuel__Cost': Fuel__Cost, 'Carbon_Foot__Print': Carbon_Foot__Print, 'UserDetail': UserDetail})


@ login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@ login_required(login_url='login')
def asset(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

        Address = Service_History.objects.get(Device_ID=device_id).Address

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

        asset_info = Asset.objects.get(Device_ID=device_id)

    return render(request, 'dgms/dgms_asset_detail.html', {'GWDB': GWDB, 'PowerStatus': PowerStatus, 'asset_info': asset_info, 'gsm': gsm, 'Address1': Address1, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'Address': Address, 'DDOI': DDOI, 'alert_count': alert_count, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'current_time': current_time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat})


@ login_required(login_url='login')
def alert(request):

    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        CustomerID = []
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
            Customer_ID = Customer.objects.get(
                Customer_Name=username).Customer_ID
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

            status = ['power_factor']

            if request.method == 'GET' and 'date' in request.GET:
                alerts = Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts, request=request)
                alerts = myFilter.qs

                enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
                startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

            elif request.method == 'GET' and 'range' in request.GET:

                if request.GET['time_range'] == 'Last 30 mins':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 hour':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 7 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 12 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 24 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 days':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 5 days':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=5)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 week':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 weeks':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 month':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 months':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=60)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 6 months':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=183)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 year':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=365)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 years':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

                else:
                    alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                        alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    enddate = (Alerts.objects.filter(device_id__in=Device_ID).exclude(
                        alert_type_name__in=status).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                    startdate = (Alerts.objects.filter(device_id__in=Device_ID).exclude(
                        alert_type_name__in=status).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                TR = request.GET['time_range']

            else:

                alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                enddate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                startdate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts, request=request)
                alerts = myFilter.qs

            status = ['power_factor']

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

            return render(request, 'dgms/dgms_alert.html', {'alerts_details': alerts_details, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})

        elif request.user.is_superuser:
            Customer_Name = 'Admin'
            TR = None
            Count = None
            alerts = None
            myFilter = None
            status = ['power_factor']

            if request.method == 'GET' and 'date' in request.GET:
                alerts = Alerts.objects.filter().exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts, request=request)
                alerts = myFilter.qs

                enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
                startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

            elif request.method == 'GET' and 'range' in request.GET:

                if request.GET['time_range'] == 'Last 30 mins':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 hour':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 7 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 12 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 24 hours':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 days':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 5 days':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=5)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=5)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 week':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 weeks':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 month':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 months':
                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=60)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=60)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 6 months':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=183)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=183)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 year':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=365)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=365)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 years':

                    alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                    ) - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

                TR = request.GET['time_range']

            else:
                status = ['power_factor']

                alerts = Alerts.objects.filter().exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                enddate = Alerts.objects.filter().order_by(
                    '-created_at').exclude(alert_type_name__in=status).last().created_at
                startdate = Alerts.objects.filter().order_by(
                    '-created_at').exclude(alert_type_name__in=status).first().updated_at

            myFilter = AlertFilter(
                request.GET, queryset=alerts, request=request)
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

            return render(request, 'dgms/dgms_alert.html', {'alerts_details': alerts_details, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})

        elif request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name
            managername = Manager.objects.get(
                Manager_Name=username).Manager_Name
            User_details = User_Detail.objects.all()
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

            status = ['power_factor']

            if request.method == 'GET' and 'date' in request.GET:
                alerts = Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts, request=request)
                alerts = myFilter.qs

                enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
                startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

            elif request.method == 'GET' and 'range' in request.GET:

                if request.GET['time_range'] == 'Last 30 mins':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 hour':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 7 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 12 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 24 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 days':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 5 days':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=5)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 week':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 weeks':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 month':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 months':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=60)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 6 months':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=183)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 year':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=365)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 years':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts, request=request)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

                TR = request.GET['time_range']

            else:

                alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                    alert_type_name__in=status).order_by('-alert_open', '-created_at')

                enddate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                startdate = (Alerts.objects.filter(
                    device_id__in=Device_ID).exclude(alert_type_name__in=status).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts, request=request)
                alerts = myFilter.qs

            status = ['power_factor']

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

            return render(request, 'dgms/dgms_alert.html', {'alerts_details': alerts_details, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})


@ login_required(login_url='login')
def servicehistory(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        # SP = Service_History.objects.get(
        #     Device_ID=device_id).Service_Provider
        # SC = Service_History.objects.get(
        #     Device_ID=device_id).Contact
        # Address = Service_History.objects.get(Device_ID=device_id).Address
        # Con = Service_History.objects.get(Device_ID=device_id).Contact
        # LSD = Service_History.objects.get(
        #     Device_ID=device_id).Last_Service_Date
        # Activity = Service_History.objects.get(
        #     Device_ID=device_id).Activity
        # Remark = Service_History.objects.get(Device_ID=device_id).Remark
        # Activity1 = Service_History.objects.get(
        #     Device_ID=device_id).Activity1
        # Remark1 = Service_History.objects.get(Device_ID=device_id).Remark1
        # NSD = Service_History.objects.get(
        #     Device_ID=device_id).Next_Service_Date

        service_info = Service_History.objects.get(Device_ID=device_id)

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size

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

        try:
            pdf_loc = service_info.Service_Document.url
        except:
            pdf_loc = "None"

        asset = Asset.objects.get(Device_ID=device_id)

    return render(request, 'dgms/dgms_service_history.html', {'asset': asset, 'pdf_loc': pdf_loc, 'service_info': service_info, 'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Address1': Address1, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'Tank_Size': Tank_Size, 'alert_count': alert_count, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id})


@ login_required(login_url='login')
def dgmsDashboard(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
        Stat = Device.objects.get(device_id=device_id).device_status
        Date = datetime.datetime.now()
        try:
            Fuel2 = round(DevicesInfo.objects.filter(
                device_id=device_id).exclude(fuel_level_litre=0).last().fuel_level_litre, 2)

        except:
            Fuel2 = 0

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Fuel_Per = round((Fuel2/Tank_Size)*100, 2)
        Run = DevicesInfo.objects.filter(device_id=device_id).exclude(
            dg_runtime_seconds=0).last()
        if Run != None:
            Run = Run.dg_runtime_seconds
        else:
            Run = DevicesInfo.objects.filter(device_id=device_id).exclude(
                runtime_second_ctrl=0).last()
            if Run != None:
                Run = Run.runtime_second_ctrl

        PreRH = Before_DGMA_INSTALLATION.objects.get(
            Device_ID=device_id).Previous_Run_Hour
        Run = Run + int(PreRH)
        seconds = Run
        # seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        hh = "%d:%02d:%02d" % (hour, minutes, seconds)

        UG = round(DevicesInfo.objects.filter(device_id=device_id).exclude(
            unit_generated_kwh=0).last().unit_generated_kwh, 2)
        PreUG = Before_DGMA_INSTALLATION.objects.get(
            Device_ID=device_id).Units_Generated
        UG = UG + float(PreUG)

        CarbonFootPrint = DeviceOperational.objects.filter(
            device_id=device_id).aggregate(Sum('carbon_footprint'))
        Carbon_Foot_Print = round(
            float(CarbonFootPrint['carbon_footprint__sum']), 2)

        BV = DevicesInfo.objects.filter(device_id=device_id).exclude(
            dg_battery_voltage=0).last().dg_battery_voltage

        FuelConsumed = DeviceOperational.objects.filter(
            device_id=device_id).aggregate(Sum('fuel_consumed'))
        Fuel_Consumed = float(FuelConsumed['fuel_consumed__sum'])
        AvgFC = round(Fuel_Consumed/(Run*0.000277778), 2)

        # Energy_output_avg = DevicesInfo.objects.filter(device_id=device_id).exclude(
        #     energy_output_kva=0).aggregate(Avg('energy_output_kva'))
        # Energy_output = round(
        #     float(Energy_output_avg['energy_output_kva__avg']), 2)
        # RatingD = Device.objects.get(device_id=device_id).device_rating
        # Energy_OA = round((Energy_output/RatingD)*100, 2)

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

        MaxDL = DeviceOperational.objects.filter(
            device_id=device_id).aggregate(Max('maximum_demand_load'))
        MaxDLoad = round(float(MaxDL['maximum_demand_load__max']), 2)

        DeviceC = DeviceCounterView.objects.filter(
            device_id=device_id)[0].counter

        DeviceC = DeviceC + \
            int(Before_DGMA_INSTALLATION.objects.get(
                Device_ID=device_id).Run_Count)

        RT = round(DevicesInfo.objects.filter(device_id=device_id).exclude(
            room_temperature=0).last().room_temperature, 2)

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

        Fuel_Level = DevicesInfo.objects.filter(
            device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-device_time')

        Fuel1 = []
        Time1 = []
        Time2 = []
        Time = []
        Level = []
        for Fuel in Fuel_Level:
            Fuel1.append(Fuel.fuel_level_litre)
            Time2.append(Fuel.device_time.strftime('%Y-%m-%d %H:%M:%S'))

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

        for t in Time2:
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

        Fuel1.reverse()
        Time.reverse()

        status = ['power_factor']

        alerts = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alerts)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        asset_info = Asset.objects.get(Device_ID=device_id)

        service_info = Service_History.objects.get(Device_ID=device_id)

        DTNS = (Service_History.objects.get(
            Device_ID=device_id).Next_Service_Date) - (datetime.date.today())

    return render(request, 'dgms/dgms_dashboard_device.html', {'DTNS': DTNS, 'service_info': service_info, 'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'Fuel2': Fuel2, 'DDOI': DDOI, 'alert_count': alert_count, 'Fuel1': Fuel1, 'Time': Time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Fuel2': Fuel2, 'Tank_Size': Tank_Size, 'Fuel_Per': Fuel_Per, 'hh': hh, 'UG': UG, 'Carbon_Foot_Print': Carbon_Foot_Print, 'BV': BV, 'AvgFC': AvgFC, 'Energy_OA': Energy_OA, 'MaxDLoad': MaxDLoad, 'DeviceC': DeviceC, 'asset_info': asset_info, 'Star': Star, 'RT': RT, 'diff': diff, 'Level': Level, 'Fuel1': Fuel1, 'Time': Time})


@ login_required(login_url='login')
def energyPara(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        UG = []
        VLL = []
        VLN = []
        FREQ = []
        Time1 = []
        Time = []

        for det in Details:
            Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
            UG.append(round(det.unit_generated_kwh, 2))
            VLN.append(round(det.vln_average, 2))
            VLL.append(round(det.vll_average, 2))
            FREQ.append(round(det.frequency, 2))

        UG.reverse()
        VLN.reverse()
        VLL.reverse()
        FREQ.reverse()

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

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        Name = "Energy Parameters"

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

        return render(request, 'dgms/dgms_energyPara.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'DDOI': DDOI, 'VLN': VLN, 'VLL': VLL, 'FREQ': FREQ, 'alert_count': alert_count, 'Time': Time,  'TR': TR, 'myFilter': myFilter, 'UG': UG, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def loadKPI(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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
            WT.append(round(det.energy_output_kw_total, 2))
            EO.append(round(det.energy_output_kva, 2))
            CA.append(round(det.current_average, 2))
            CR.append(round(det.current_r_phase, 2))
            CY.append(round(det.current_y_phase, 2))
            CB.append(round(det.current_b_phase, 2))

        WT.reverse()
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

        elif Count >= 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        return render(request, 'dgms/dgms_loadKPI.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'DDOI': DDOI, 'alert_count': alert_count, 'WT': WT, 'EO': EO, 'Time': Time, 'TR': TR, 'myFilter': myFilter, 'CA': CA, 'CR': CR, 'CY': CY, 'CB': CB, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def enginePara(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        Time1 = []
        Time = []
        DL = []
        DBV = []
        RPM = []

        for det in Details:
            Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
            DL.append(round(det.fuel_level_litre, 2))
            DBV.append(round(det.dg_battery_voltage, 2))
            RPM.append(round(det.rpm, 2))
            # print(det.device_time.strftime('%Y-%m-%d %H:%M:%S') +
            #       "Fuel litre:" + str(round(det.fuel_level_litre, 2)) + "Fuel litre Percentage:" + str(round(det.fuel_level_percentage, 2)))

        DL.reverse()
        DBV.reverse()
        RPM.reverse()

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

        elif Count >= 10000:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
            for t in TimeN:
                Time.append(t[sl1]+"-"+t[sl2]+"/"+t[sl3])

            Time.reverse()

        # status = ['power_factor','gateway_device_battery','fuel_level_percentage','gsm_signal', 'energy_output_kw_total', 'dg_battery_voltage', 'room_temperature', 'frequency',
        #           'rpm_ctrl', 'current_b_phase', 'vll_average', 'energy_output_kva', 'current_r_phase', 'rpm', 'current_y_phase', ]

        # status = ['power_factor', 'gateway_device_battery', 'fuel_level_percentage', 'gsm_signal',  'dg_battery_voltage', 'room_temperature', 'frequency',
        #           'rpm_ctrl', 'vll_average', 'rpm', ]

        # alerts = Alerts.objects.filter(
        #     device_id=device_id).exclude(alert_type_name__in=status).order_by('-created_at')

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        Name = "Engine Parameters"

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

        return render(request, 'dgms/dgms_enginePara.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'DDOI': DDOI, 'alert_count': alert_count, 'Time': Time, 'myFilter': myFilter, 'TR': TR, 'DL': DL, 'RPM': RPM, 'DBV': DBV, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def performanceKPI(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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
            Details = DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time')

            myFilter = DeviceOperationalFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 hour':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 hours':

                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 7 hours':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 12 hours':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 24 hours':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 days':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 5 days':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 week':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 weeks':

                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 month':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 months':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 6 months':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 1 year':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            elif request.GET['time_range'] == 'Last 2 years':
                Details = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(
                    request.GET, queryset=Details)
                Details = myFilter.qs

                Count = Details.count()

            TR = request.GET['time_range']

        else:
            Details = DeviceOperational.objects.filter(
                device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-start_time')

            myFilter = DeviceOperationalFilter(request.GET, queryset=Details)
            Details = myFilter.qs

            Count = Details.count()

        Time1 = []
        Time = []
        MDL = []
        LE = []
        CF = []
        FC = []
        FCO = []
        RH = []
        UG = []
        RC = []
        Total_FC = 0
        Total_FCO = 0
        Total_RH1 = 0
        Total_RH = 0
        Total_UG = 0

        for det in Details:
            if det.run_hours == None:
                pass
            else:
                RH.append(round(float(det.run_hours), 2))
                MDL.append(round(det.maximum_demand_load, 2))
                Time1.append(det.start_time.strftime('%Y-%m-%d %H:%M:%S'))
                LE.append(round(det.efficiency, 2))
                CF.append(round(det.carbon_footprint, 2))
                FC.append(round(det.fuel_consumed, 2))
                FCO.append(round(det.fuel_cost, 2))
                if det.unit_generated_kwh == 0:
                    UG.append(0)
                else:
                    UG.append(round(det.energy_generated_kwh, 2))
                RC.append(round(det.run_count, 2))

        RH.reverse()
        MDL.reverse()
        LE.reverse()
        CF.reverse()
        FC.reverse()
        FCO.reverse()
        UG.reverse()
        RC.reverse()

        Total_UG = round(sum(UG), 2)
        Total_FC = round(sum(FC), 2)
        Total_FCO = round(sum(FCO), 2)
        Total_RH1 = round((sum(RH)*3600), 2)

        seconds = Total_RH1
        # seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        Total_RH = "%d:%02d:%02d" % (hour, minutes, seconds)

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

        if Count < 100:
            sl1 = slice(5, 7)
            sl2 = slice(8, 11)
            sl3 = slice(11, -6)
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

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

        RunCount = len(RH)

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

        Name = "PERFORMANCE BASED KPI"

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

        return render(request, 'dgms/dgms_performanceKPI.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Total_UG': Total_UG, 'Name': Name, 'LTOD': LTOD, 'RC': RC, 'temperature': temperature, 'description': description, 'icon': icon, 'Total_RH': Total_RH, 'RunCount': RunCount, 'Total_FC': Total_FC, 'Total_FCO': Total_FCO, 'UG': UG, 'DDOI': DDOI, 'RH': RH, 'MDL': MDL, 'LE': LE, 'CF': CF, 'FC': FC, 'FCO': FCO, 'alert_count': alert_count, 'Time': Time, 'myFilter': myFilter, 'TR': TR, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def deviceInfoKPI(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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
            PS1.append(round(det.gateway_power_status, 2))
            BV1.append(round(det.gateway_device_battery, 2))

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

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        Name = "DGMS DEVICE INFO"

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

        return render(request, 'dgms/dgms_deviceInfoKPI.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'GSMSignal': GSMSignal, 'PowerStatus': PowerStatus, 'BatteryVoltage': BatteryVoltage, 'DDOI': DDOI, 'GSM': GSM, 'GB': GB, 'alert_count': alert_count, 'Time': Time, 'myFilter': myFilter, 'TR': TR, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


@ login_required(login_url='login')
def fuel_report(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        # Fuel = FuelFilledReport.objects.filter(
        #     device_id=device_id).order_by('device_time')

        # myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
        # Fuel = myFilter.qs

        TR = None
        Count = None
        Details = None
        myFilter = None
        daterange = None
        startdate = None
        enddate = None
        if request.method == 'GET' and 'date' in request.GET:
            Fuel = FuelFilledReport.objects.filter(
                device_id=device_id).order_by('-device_time')

            myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
            Fuel = myFilter.qs

            enddate = (request.GET['start_date'])
            startdate = (request.GET['end_date'])

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':

                Fuel = FuelFilledReport.objects.filter(device_id=device_id, device_time__gte=datetime.datetime.now(
                ) - datetime.timedelta(minutes=30)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':
                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':
                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':
                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':
                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id, device_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).order_by('-device_time')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

            else:

                Fuel = FuelFilledReport.objects.filter(
                    device_id=device_id).order_by('-device_time')

                enddate = (FuelFilledReport.objects.filter(
                    device_id=device_id).order_by('-device_time').last().device_time).strftime('%d-%m-%Y')
                startdate = (FuelFilledReport.objects.filter(
                    device_id=device_id).order_by('-device_time').first().device_time).strftime('%d-%m-%Y')

                myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
                Fuel = myFilter.qs

            TR = request.GET['time_range']

        else:
            Fuel = FuelFilledReport.objects.filter(
                device_id=device_id).order_by('-device_time')

            if len(Fuel) == 0:
                enddate = 'None'
                startdate = 'None'
            else:
                enddate = (FuelFilledReport.objects.filter(
                    device_id=device_id).order_by('-device_time').last().device_time).strftime('%d-%m-%Y')
                startdate = (FuelFilledReport.objects.filter(
                    device_id=device_id).order_by('-device_time').first().device_time).strftime('%d-%m-%Y')

            myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
            Fuel = myFilter.qs

        Count = Fuel.count()
        Total = 0
        Time1 = []
        for F in Fuel:
            Total = F.fuel_added + Total
            Time1.append(F.device_time.strftime('%Y-%m-%d %H:%M:%S'))

        UTC = '0000-00-00 05:30:00'
        y = UTC[:4]
        mo = UTC[5:7]
        da = UTC[8:10]
        h = UTC[11:13]
        m = UTC[14:16]
        s = UTC[17:19]
        d1 = datetime.timedelta(days=(int(
            y)*365 + int(mo)*30 + int(da)*1), hours=int(h), minutes=int(m), seconds=int(s))

        Time = []
        for t in Time1:

            y1 = t[:4]
            mo1 = t[5:7]
            da1 = t[8:10]
            h1 = t[11:13]
            m1 = t[14:16]
            s1 = t[17:19]
            d21 = datetime.datetime(year=int(y1), month=int(mo1), day=int(
                da1), hour=int(h1), minute=int(m1), second=int(s1))

            Time.append(d1 + d21)

        Fuel_Details = zip(Time, Fuel)

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Address = User_Detail.objects.get(Device_ID=device_id).Address

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        Name = "Fuel filled report"

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

    return render(request, 'dgms/dgms_fuel_report.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'DDOI': DDOI, 'alert_count': alert_count, 'startdate': startdate, 'enddate': enddate, 'daterange': daterange, 'TR': TR, 'Address': Address, 'Tank_Size': Tank_Size, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'device_id': device_id, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id, 'Fuel_Details': Fuel_Details, 'Total': Total, 'Count': Count, 'myFilter': myFilter})


@ login_required(login_url='login')
def operational_report(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name
        # OPR = DeviceOperational.objects.filter(
        #     device_id=device_id).order_by('start_time')

        # myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
        # OPR = myFilter.qs

        TR = None
        Count = None
        Details = None
        myFilter = None
        daterange = None
        startdate = None
        enddate = None
        if request.method == 'GET' and 'date' in request.GET:
            OPR = DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time')

            myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
            OPR = myFilter.qs

            enddate = (request.GET['start_date'])
            startdate = (request.GET['end_date'])

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':

                OPR = DeviceOperational.objects.filter(device_id=device_id, start_time__gte=datetime.datetime.now(
                ) - datetime.timedelta(minutes=30)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':
                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':
                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':
                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':
                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                OPR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

            else:
                OPR = DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time')

                enddate = (DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time').last().start_time).strftime('%d-%m-%Y')
                startdate = (DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time').first().end_time)
                if startdate == None:
                    startdate = datetime.datetime.now().strftime('%d-%m-%Y')
                else:
                    startdate = (DeviceOperational.objects.filter(
                        device_id=device_id).order_by('-start_time').first().end_time).strftime('%d-%m-%Y')

                myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

            TR = request.GET['time_range']

        else:
            OPR = DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time')

            enddate = (DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time').last().start_time).strftime('%d-%m-%Y')
            startdate = (DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time').first().end_time)
            if startdate == None:
                startdate = datetime.datetime.now().strftime('%d-%m-%Y')
            else:
                startdate = (DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time').first().end_time).strftime('%d-%m-%Y')

            myFilter = DeviceOperationalFilter(request.GET, queryset=OPR)
            OPR = myFilter.qs

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        Count = OPR.count()
        Total_RHour = []
        Total_Fuel = []
        Total_FuelCon = []
        Total_energy = []
        Total_RH = 0
        Total_F = 0
        Total_FC = 0
        Total_EG = 0
        Total_RH1 = 0
        RC = []
        Run1 = []
        Run = []
        Start_Time1 = []
        End_Time1 = []

        # for p in PR:
        #     if p.run_hours == None:
        #         Total_RH = 0 + Total_RH
        #     else:
        #         Total_RH = p.run_hours + Total_RH
        #         Total_F = abs(p.fuel_consumed + Total_F)
        #         FC.append(p.fuel_consumed)
        #         RH.append(p.run_hours)
        #         Total_PL.append(p.maximum_demand_load)
        #         Total_AL.append(p.efficiency)

        for o in OPR:
            if o.run_hours == None:
                Start_Time1.append(
                    o.start_time.strftime('%Y-%m-%d %H:%M:%S'))
                End_Time1.append(None)
                Total_RH = 0 + Total_RH
                Run1.append(0)
                Total_RHour.append(0)
                Total_Fuel.append(0)
                Total_FuelCon.append(0)
                Total_energy.append(0)
            else:
                Start_Time1.append(
                    o.start_time.strftime('%Y-%m-%d %H:%M:%S'))
                End_Time1.append(
                    o.end_time.strftime('%Y-%m-%d %H:%M:%S'))
                Run1.append(float(o.run_hours*3600))
                Total_RHour.append(round(o.run_hours, 2))
                Total_Fuel.append(abs(round(o.fuel_consumed, 2)))
                Total_FuelCon.append(abs(round(o.fuel_cost, 2)))
                Total_energy.append(abs(round(o.energy_generated_kwh, 2)))
                RC.append(o.run_count)

                # Total_RH1 = o.run_hours + Total_RH1
                # Total_F = abs(o.fuel_consumed + Total_F)
                # Total_FC = abs(o.fuel_cost + Total_FC)
                # Total_EG = o.energy_generated_kwh + Total_EG

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

            if e == None:
                End_Time.append(None)
            else:

                y2 = e[:4]
                mo2 = e[5:7]
                da2 = e[8:10]
                h2 = e[11:13]
                m2 = e[14:16]
                s2 = e[17:19]
                d22 = datetime.datetime(year=int(y2), month=int(mo2), day=int(
                    da2), hour=int(h2), minute=int(m2), second=int(s2))

                End_Time.append(d1 + d22)

        Total_RH1 = sum(Total_RHour)
        Total_F = sum(Total_Fuel)
        Total_FC = sum(Total_FuelCon)
        Total_EG = sum(Total_energy)

        for rh in Run1:
            seconds = rh
            # seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            hh = "%d:%02d:%02d" % (hour, minutes, seconds)
            Run.append(hh)

        Total_RH2 = (Total_RH1*3600)

        seconds = Total_RH2
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        Total_RH = "%d:%02d:%02d" % (hour, minutes, seconds)

        # RC.reverse()

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Address = User_Detail.objects.get(Device_ID=device_id).Address

        OP1 = zip(Start_Time, End_Time, OPR, RC, Run)

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        Name = "Operational report"

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

    return render(request, 'dgms/dgms_operational_report.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'RC': RC, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'DDOI': DDOI, 'alert_count': alert_count, 'RC': RC, 'startdate': startdate, 'enddate': enddate, 'daterange': daterange, 'TR': TR, 'Address': Address, 'Tank_Size': Tank_Size, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'OP1': OP1, 'Count': Count, 'Total_RH': Total_RH, 'Total_F': Total_F, 'Total_FC': Total_FC, 'Total_EG': Total_EG, 'device_id': device_id, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id, 'myFilter': myFilter})


@ login_required(login_url='login')
def performance_report(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        # PR = DeviceOperational.objects.filter(
        #     device_id=device_id).order_by('start_time')

        # myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
        # PR = myFilter.qs

        TR = None
        Count = None
        myFilter = None
        daterange = None
        startdate = None
        enddate = None
        if request.method == 'GET' and 'date' in request.GET:
            PR = DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time')

            myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
            PR = myFilter.qs

            enddate = (request.GET['start_date'])
            startdate = (request.GET['end_date'])

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':

                PR = DeviceOperational.objects.filter(device_id=device_id, start_time__gte=datetime.datetime.now(
                ) - datetime.timedelta(minutes=30)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':
                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':
                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':
                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':
                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                PR = DeviceOperational.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).order_by('-start_time')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

            else:
                PR = DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time')

                enddate = (DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time').last().start_time).strftime('%d-%m-%Y')
                startdate = (DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time').first().end_time)
                if startdate == None:
                    startdate = datetime.datetime.now().strftime('%d-%m-%Y')
                else:
                    startdate = (DeviceOperational.objects.filter(
                        device_id=device_id).order_by('-start_time').first().end_time).strftime('%d-%m-%Y')

                myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
                PR = myFilter.qs

            TR = request.GET['time_range']

        else:
            PR = DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time')

            enddate = (DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time').last().start_time).strftime('%d-%m-%Y')
            startdate = (DeviceOperational.objects.filter(
                device_id=device_id).order_by('-start_time').first().end_time)
            if startdate == None:
                startdate = datetime.datetime.now().strftime('%d-%m-%Y')
            else:
                startdate = (DeviceOperational.objects.filter(
                    device_id=device_id).order_by('-start_time').first().end_time).strftime('%d-%m-%Y')

            myFilter = DeviceOperationalFilter(request.GET, queryset=PR)
            PR = myFilter.qs

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        Count = PR.count()
        RC = []
        Total_RH = 0
        Total_F = 0
        Total_PL = []
        Total_AL = []
        Total_RH1 = 0
        Run1 = []
        Run = []
        Start_Time1 = []
        End_Time1 = []

        FC = []
        RH = []

        for p in PR:
            if p.run_hours == None:
                Start_Time1.append(
                    p.start_time.strftime('%Y-%m-%d %H:%M:%S'))
                End_Time1.append(None)
                Total_RH = 0 + Total_RH
                Run1.append(0)
            else:
                Start_Time1.append(
                    p.start_time.strftime('%Y-%m-%d %H:%M:%S'))
                End_Time1.append(
                    p.end_time.strftime('%Y-%m-%d %H:%M:%S'))
                RC.append(p.run_count)
                Total_RH1 = p.run_hours + Total_RH1
                Run1.append(float(p.run_hours*3600))
                Total_F = abs(p.fuel_consumed + Total_F)
                FC.append(p.fuel_consumed)
                RH.append(p.run_hours)
                Total_PL.append(p.maximum_demand_load)
                Total_AL.append(p.efficiency)

        for rh in Run1:
            seconds = rh
            # seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            hh = "%d:%02d:%02d" % (hour, minutes, seconds)
            Run.append(hh)

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

            if e == None:
                End_Time.append(None)
            else:

                y2 = e[:4]
                mo2 = e[5:7]
                da2 = e[8:10]
                h2 = e[11:13]
                m2 = e[14:16]
                s2 = e[17:19]
                d22 = datetime.datetime(year=int(y2), month=int(mo2), day=int(
                    da2), hour=int(h2), minute=int(m2), second=int(s2))

                End_Time.append(d1 + d22)

        Total_RH2 = (Total_RH1*3600)

        seconds = Total_RH2
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        Total_RH = "%d:%02d:%02d" % (hour, minutes, seconds)

        if len(Total_PL) == 0:
            Avg_PL = 0
        else:
            Avg_PL = round(sum(Total_PL)/len(Total_PL), 2)

        if len(Total_AL) == 0:
            Avg_AL = 0
        else:
            Avg_AL = round(sum(Total_AL)/len(Total_AL), 2)

        FR = zip(FC, RH)
        AFC = []
        for f, r in FR:
            if f == 0:
                AFC.append(0)
            else:
                AFC.append(round(float(f/r), 2))

        FuelConsumed = PR.aggregate(Sum('fuel_consumed'))
        Fuel_Consumed = float(FuelConsumed['fuel_consumed__sum'])

        if len(AFC) == 0:
            Avg_FC = 0
        else:
            Avg_FC = round(Fuel_Consumed/(Total_RH2 * 0.000277778), 2)

        # RC.reverse()

        context1 = zip(Start_Time, End_Time, PR, AFC, RC, Run)

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Address = User_Detail.objects.get(Device_ID=device_id).Address

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

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

        Name = "Performance report"

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

    return render(request, 'dgms/dgms_performance_report.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'Name': Name, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'DDOI': DDOI, 'alert_count': alert_count, 'startdate': startdate, 'enddate': enddate, 'daterange': daterange, 'Avg_AL': Avg_AL, 'Avg_PL': Avg_PL, 'Avg_FC': Avg_FC, 'TR': TR, 'PR': PR, 'Address': Address, 'Tank_Size': Tank_Size, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'context1': context1, 'Count': Count, 'Total_RH': Total_RH, 'Total_F': Total_F, 'device_id': device_id, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id, 'myFilter': myFilter})


@ login_required(login_url='login')
def customerInfo(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email

        if request.user.is_superuser:
            Customer_Details = Customer.objects.all()
            CustomerID = []
            for Cus in Customer_Details:
                CustomerID.append(Cus.Customer_ID)
            Total_Customer = Customer.objects.all().count()
            Total = 0
            Live = 0
            Offline = 0
            Location1 = 0
            DeviceID = []
            for Customer_ID in CustomerID:
                Total1 = Device.objects.filter(account_id=Customer_ID).count()
                Total = Total1 + Total
                Live1 = Device.objects.filter(
                    account_id=Customer_ID, device_status='ON').count()
                Live = Live1 + Live
                Offline1 = Device.objects.filter(
                    account_id=Customer_ID, device_status='OFF').count()
                Offline = Offline1 + Offline
                Location2 = Device.objects.filter(
                    account_id=Customer_ID).count()
                Location1 = Location1 + Location2

                Device_ID = Device.objects.filter(account_id=Customer_ID)
                for i in range(Total1):
                    a = Device_ID[i].device_id
                    DeviceID.append(a)

                Location = []
                State = []
                City = []
                Status = []
                Rating = []
                Customer_Name = []
                Customer_Email = []
                Contact_Person = []
                User_Email = []
                User_Contact1 = []
                User_Contact2 = []
                for j in DeviceID:
                    Sta = User_Detail.objects.filter(
                        Device_ID=j)[0].State
                    Cit = User_Detail.objects.filter(
                        Device_ID=j)[0].City
                    Loc = User_Detail.objects.filter(
                        Device_ID=j)[0].Location
                    Stat = Device.objects.filter(device_id=j)[0].device_status
                    Rat = Device.objects.filter(device_id=j)[0].device_rating
                    CN = User_Detail.objects.filter(
                        Device_ID=j)[0].Customer_Name
                    Customer_Name.append(CN)
                    CP = User_Detail.objects.filter(
                        Device_ID=j)[0].Contact_Person
                    Contact_Person.append(CP)
                    UE = User_Detail.objects.filter(
                        Device_ID=j)[0].Email_ID
                    User_Email.append(UE)
                    UC = User_Detail.objects.filter(
                        Device_ID=j)[0].Email_ID
                    User_Email.append(UE)
                    UserC1 = User_Detail.objects.filter(Device_ID=j)[
                        0].Contact1
                    User_Contact1.append(UserC1)
                    UserC2 = User_Detail.objects.filter(Device_ID=j)[
                        0].Contact2
                    User_Contact2.append(UserC2)

                    for cu in Customer_Name:
                        Customer_Email1 = Customer.objects.filter(
                            Customer_Name=cu)[0].Email_ID
                        Customer_Email.append(Customer_Email1)

                    Rating.append(Rat)
                    State.append(Sta)
                    City.append(Cit)
                    Location.append(Loc)
                    Status.append(Stat)

                UserDetail = zip(State, City, Location, Status, Rating,
                                 Customer_Name, DeviceID, Customer_Email, Contact_Person, User_Email, User_Contact1, User_Contact2)

                status = ['power_factor']
                alert = Alerts.objects.filter(
                    alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
                alert_count = len(alert)

        return render(request, 'dgms/admindashboard.html', {'alert_count': alert_count, 'UserDetail': UserDetail, 'username': username, 'Total_Customer': Total_Customer, 'Location1': Location1,  'Total': Total, 'Live': Live, 'Offline': Offline})


@ login_required(login_url='login')
def customer(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
    Manager_name = User_Detail.objects.get(Device_ID=device_id).Manager_Name
    Manager_Detais = Manager.objects.filter(Manager_Name=Manager_name)
    Customer_name = User_Detail.objects.get(Device_ID=device_id).Customer_Name
    User_details = User_Detail.objects.filter(Customer_Name=Customer_name)
    Total_User = User_details.count()

    myFilter = CustomerFilter(request.GET, queryset=User_details)
    User_details = myFilter.qs

    DI = request.GET.get('device_id')

    alert = Alerts.objects.filter(
        alert_open=True).order_by('-created_at')
    alert_count = len(alert)

    return render(request, 'dgms/customer.html', {'alert_count': alert_count, 'myFilter': myFilter, 'User_details': User_details, 'Total_User': Total_User, 'Manager_Detais': Manager_Detais})


@ login_required(login_url='login')
def update(request):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email

    price = Price.objects.all()

    Total = len(price)

    form = PriceForm()

    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            form.save()
            form = PriceForm()

    status = ['power_factor']
    alert = Alerts.objects.filter(
        alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
    alert_count = len(alert)
    return render(request, 'dgms/update.html', {'Total': Total, 'form': form, 'price': price, 'username': username, 'alert_count': alert_count})


@ login_required(login_url='login')
def updateprice(request, location):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email

    price = Price.objects.get(Location=location)

    form = PriceForm(instance=price)

    if request.method == 'POST':
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect('update')

    status = ['power_factor']
    alert = Alerts.objects.filter(
        alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
    alert_count = len(alert)
    return render(request, 'dgms/updateprice.html', {'form': form, 'username': username, 'alert_count': alert_count})


@ login_required(login_url='login')
def device_alert(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
        Stat = Device.objects.get(device_id=device_id).device_status

        # Energy_output_avg = DevicesInfo.objects.filter(device_id=device_id).exclude(
        #     energy_output_kva=0).aggregate(Avg('energy_output_kva'))
        # Energy_output = round(
        #     float(Energy_output_avg['energy_output_kva__avg']), 2)

        # RatingD = Device.objects.get(device_id=device_id).device_rating
        # Energy_OA = round((Energy_output/RatingD)*100, 2)
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

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

        TR = None
        Count = None
        alerts = None
        myFilter = None
        startdate = None
        enddate = None
        status = ['power_factor']

        if request.method == 'GET' and 'date' in request.GET:
            alerts = Alerts.objects.filter(
                device_id=device_id).exclude(alert_type_name__in=status).order_by('-alert_open', '-created_at')

            myFilter = DeviceAlertFilter(request.GET, queryset=alerts)
            alerts = myFilter.qs

            enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
            startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

        elif request.method == 'GET' and 'range' in request.GET:

            status = ['power_factor']

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
            status = ['power_factor']

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

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Address = User_Detail.objects.get(Device_ID=device_id).Address

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

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

        alerts_details = zip(Start_Time, End_Time, alerts)

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

        return render(request, 'dgms/dgms_device_alert.html', {'PowerStatus': PowerStatus, 'GWDB': GWDB, 'gsm': gsm, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'Tank_Size': Tank_Size, 'Address': Address, 'TR': TR, 'myFilter': myFilter, 'alerts_details': alerts_details, 'alert_count': alert_count, 'DDOI': DDOI, 'Count': Count,  'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff,  'current_time': current_time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, })


@ login_required(login_url='login')
def asset_library(request, device_id):
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        if request.user.is_customer:
            Customer_Name = Customer.objects.get(
                Customer_Name=username).Customer_Name
        if request.user.is_superuser:
            Customer_Name = 'Admin'
        if request.user.is_user:
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
        if request.user.is_manager:
            Customer_Name = Manager.objects.get(
                Manager_Name=username).Customer_Name

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
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

        status = ['power_factor']

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        alert_count = len(alert)

        DDOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation

        Address = Service_History.objects.get(Device_ID=device_id).Address

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

        asset_info = Asset.objects.get(Device_ID=device_id)

        library = Library.objects.filter(Device_ID=device_id)

        myFilter = LibraryFilter(
            request.GET, queryset=library)
        library = myFilter.qs

    return render(request, 'dgms/dgms_asset_library.html', {'library': library, 'myFilter': myFilter, 'GWDB': GWDB, 'PowerStatus': PowerStatus, 'library': library, 'asset_info': asset_info, 'gsm': gsm, 'Address1': Address1, 'LTOD': LTOD, 'temperature': temperature, 'description': description, 'icon': icon, 'Address': Address, 'DDOI': DDOI, 'alert_count': alert_count, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'current_time': current_time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat})

# @ login_required(login_url='login')
# def addCustomer(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AddCustomerForm()
#     if request.method == 'POST':
#         form = AddCustomerForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             form = AddCustomerForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'addCustomer.html', context)


# @ login_required(login_url='login')
# def addManager(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AddManagerForm()

#     if request.method == 'POST':
#         form = AddManagerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = AddManagerForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'addManager.html', context)


# @ login_required(login_url='login')
# def addUser(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AddUserForm()

#     if request.method == 'POST':
#         form = AddUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = AddUserForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'addUser.html', context)


# @ login_required(login_url='login')
# def assetInfo(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AssetForm()

#     if request.method == 'POST':
#         form = AssetForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             form = AssetForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'assetInfo.html', context)


# @ login_required(login_url='login')
# def deviceInfo(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AddDevice_InfoForm()

#     if request.method == 'POST':
#         form = AddDevice_InfoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = AddDevice_InfoForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'deviceInfo.html', context)


# @ login_required(login_url='login')
# def sensorInfo(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AddSensor_InfoForm()

#     if request.method == 'POST':
#         form = AddSensor_InfoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = AddSensor_InfoForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'sensorInfo.html', context)


# @ login_required(login_url='login')
# def addService_history(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AddService_HistoryForm()

#     if request.method == 'POST':
#         form = AddService_HistoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = AddService_HistoryForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'addService_history.html', context)


# @ login_required(login_url='login')
# def beforedgms_installation(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email
#     form = AddBefore_DGMA_INSTALLATIONForm()

#     if request.method == 'POST':
#         form = AddBefore_DGMA_INSTALLATIONForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = AddBefore_DGMA_INSTALLATIONForm()

#     context = {'form': form, 'username': username}
#     return render(request, 'addService_history.html', context)


# @ login_required(login_url='login')
# def setAlert(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         email = request.user.email

#     form = AlterForm()

#     if request.method == 'POST':
#         form = AlterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = AlterForm()

#     context = {'form': form, 'username': username}

#     return render(request, 'setAlert.html', context)
