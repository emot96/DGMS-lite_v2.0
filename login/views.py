from django.core.checks.messages import CRITICAL, ERROR
from django.db.models.aggregates import Max
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
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


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
            device_id = User_Detail.objects.get(User_Name=username).Device_ID
            Customer_Name = User_Detail.objects.get(
                Device_ID=device_id).Customer_Name
            Cit = User_Detail.objects.get(Device_ID=device_id).City
            Loc = User_Detail.objects.get(Device_ID=device_id).Location
            Rat = Device.objects.get(device_id=device_id).device_rating
            Stat = Device.objects.get(device_id=device_id).device_status
            Date = datetime.datetime.now()
            Fuel2 = round(DevicesInfo.objects.filter(
                device_id=device_id).exclude(fuel_level_litre=0).last().fuel_level_litre, 2)
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

            DOI = Asset.objects.get(Device_ID=device_id).Date_Of_Installation

            WS = Asset.objects.get(Device_ID=device_id).Warranty_Status

            LSD = Service_History.objects.get(
                Device_ID=device_id).Last_Service_Date
            NSD = Service_History.objects.get(
                Device_ID=device_id).Next_Service_Date
            SP = Service_History.objects.get(
                Device_ID=device_id).Service_Provider

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

            return render(request, 'dgmsDashboard.html', {'temperature': temperature, 'description': description, 'icon': icon, 'Fuel2': Fuel2, 'DDOI': DDOI, 'alert_count': alert_count, 'Fuel1': Fuel1, 'Time': Time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Fuel2': Fuel2, 'Tank_Size': Tank_Size, 'Fuel_Per': Fuel_Per, 'hh': hh, 'UG': UG, 'Carbon_Foot_Print': Carbon_Foot_Print, 'BV': BV, 'AvgFC': AvgFC, 'Energy_OA': Energy_OA, 'MaxDLoad': MaxDLoad, 'DeviceC': DeviceC, 'DOI': DOI, 'WS': WS, 'LSD': LSD, 'NSD': NSD, 'SP': SP, 'Star': Star, 'RT': RT, 'diff': diff, 'Level': Level, 'Fuel1': Fuel1, 'Time': Time})

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

                    # PreRH.append(Before_DGMA_INSTALLATION.objects.get(
                        # Device_ID=j).Previous_Run_Hour)
                    # RunHour2 = zip(RunHour1, PreRH)
                    for rh in RunHour1:
                        seconds = rh
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

            return render(request, 'dashboard1.html', {'alert_count': alert_count, 'username': username, 'Customer_Name': Customer_Name, 'Total': Total, 'Live': Live, 'Offline': Offline, 'Capacity': Capacity, 'InUse': InUse, 'Fuel__Consumed': Fuel__Consumed, 'Fuel__Cost': Fuel__Cost, 'Carbon_Foot__Print': Carbon_Foot__Print, 'UserDetail': UserDetail})

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
            DeviceID = []
            for i in range(Total):
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

                # PreRH.append(Before_DGMA_INSTALLATION.objects.get(
                    # Device_ID=j).Previous_Run_Hour)
                # RunHour2 = zip(RunHour1, PreRH)
                for rh in RunHour1:
                    seconds = rh
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
                # Energy_output_avg = DevicesInfo.objects.filter(
                #     device_id=j).exclude(energy_output_kva=0).aggregate(Avg('energy_output_kva'))
                # Energy_output = round(float(
                #     Energy_output_avg['energy_output_kva__avg']), 2)
                # RatingD = Device.objects.get(
                #     device_id=j).device_rating
                # Energy_OA = round((Energy_output/RatingD)*100, 2)
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
                    EnergyPrice = Price.objects.get(Location=c).Energy_Price
                    DieselPrice = Price.objects.get(Location=c).Diesel_Price
                    Diesel.append(DieselPrice)
                    Energy.append(EnergyPrice)

                UserDetail = zip(State, City, Location,
                                 Status, Rating, UnitGen, FuelCon, CarbonFP, FuelC, CPU, EnergyOA, MaxDemLoad, Star, Diesel, Energy, RunHour, DeviceID)

            status = ['power_factor']

            alert = Alerts.objects.filter(
                device_id__in=Device_ID, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')
            alert_count = len(alert)

        return render(request, 'dashboard.html', {'alert_count': alert_count, 'username': username, 'Customer_Name': Customer_Name, 'Total': Total, 'Live': Live, 'Offline': Offline, 'Capacity': Capacity, 'InUse': InUse, 'Fuel__Consumed': Fuel__Consumed, 'Fuel__Cost': Fuel__Cost, 'Carbon_Foot__Print': Carbon_Foot__Print, 'UserDetail': UserDetail})


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

        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Oem = Asset.objects.get(Device_ID=device_id).OEM
        SellerName = Asset.objects.get(Device_ID=device_id).Seller_Name
        WSD = Asset.objects.get(Device_ID=device_id).Warranty_Start_Date
        WED = Asset.objects.get(Device_ID=device_id).Warranty_End_Date
        WP = Asset.objects.get(Device_ID=device_id).Warranty_Period
        WS = Asset.objects.get(Device_ID=device_id).Warranty_Status
        EM = Asset.objects.get(Device_ID=device_id).Engine_Make
        EMN = Asset.objects.get(Device_ID=device_id).Engine_Model_No
        ESN = Asset.objects.get(Device_ID=device_id).Engine_S_NO
        EOI = Asset.objects.get(Device_ID=device_id).Engine_Other_Info
        AM = Asset.objects.get(Device_ID=device_id).Alternator_Make
        AMN = Asset.objects.get(Device_ID=device_id).Alternator_Model_No
        ASN = Asset.objects.get(Device_ID=device_id).Alternator_S_NO
        AOI = Asset.objects.get(Device_ID=device_id).Alternator_Other_Info
        BM = Asset.objects.get(Device_ID=device_id).Battery_Make
        BMN = Asset.objects.get(Device_ID=device_id).Battery_Model_No
        BSN = Asset.objects.get(Device_ID=device_id).Battery_S_NO
        BOI = Asset.objects.get(Device_ID=device_id).Battery_Other_Info
        BCM = Asset.objects.get(Device_ID=device_id).Battery_Charger_Make
        BCMN = Asset.objects.get(
            Device_ID=device_id).Battery_Charger_Model_No
        BCSN = Asset.objects.get(Device_ID=device_id).Battery_Charger_S_NO
        BCOI = Asset.objects.get(
            Device_ID=device_id).Battery_Charger_Other_Info
        DSN = DGMS_Device_Info.objects.get(
            Device_ID=device_id).Device_Serial_No
        Version = DGMS_Device_Info.objects.get(Device_ID=device_id).Version
        SC = DGMS_Device_Info.objects.get(Device_ID=device_id).Sim_Card
        IMEI = DGMS_Device_Info.objects.get(Device_ID=device_id).IMEI_No
        Other = DGMS_Device_Info.objects.get(Device_ID=device_id).Other
        OtherInfo = DGMS_Device_Info.objects.get(
            Device_ID=device_id).Other_Info
        EMMI = Sensor_Info.objects.get(
            Device_ID=device_id).Energy_Meter_Make_Info
        EMMN = Sensor_Info.objects.get(
            Device_ID=device_id).Energy_Meter_Model_No
        EMS = Sensor_Info.objects.get(
            Device_ID=device_id).Energy_Meter_S_No
        CTMI = Sensor_Info.objects.get(
            Device_ID=device_id).Current_Transformer_Make_Info
        CTMN = Sensor_Info.objects.get(
            Device_ID=device_id).Current_Transformer_Model_No
        CTSN = Sensor_Info.objects.get(
            Device_ID=device_id).Current_Transformer_S_No
        CTCR = Sensor_Info.objects.get(
            Device_ID=device_id).Current_Transformer_CT_Ratio
        FSMI = Sensor_Info.objects.get(
            Device_ID=device_id).Fuel_Sensor_Make_Info
        FSMN = Sensor_Info.objects.get(
            Device_ID=device_id).Fuel_Sensor_Model_No
        FSN = Sensor_Info.objects.get(Device_ID=device_id).Fuel_SensorS_No
        FSL = Sensor_Info.objects.get(
            Device_ID=device_id).Fuel_Sensor_Length
        DOI = DGMS_Device_Info.objects.get(
            Device_ID=device_id).DGMS_Date_Of_Installation
        CD = Asset.objects.get(Device_ID=device_id).Commissioning_Date
        OP = Asset.objects.get(Device_ID=device_id).Operations
        DP = Price.objects.get(Location=Cit).Diesel_Price
        EP = Price.objects.get(Location=Cit).Energy_Price
        now = datetime.datetime.now()
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        PRH = Before_DGMA_INSTALLATION.objects.get(
            Device_ID=device_id).Previous_Run_Hour
        PFC = Before_DGMA_INSTALLATION.objects.get(
            Device_ID=device_id).Previous_Fuel_Consumed
        RC = Before_DGMA_INSTALLATION.objects.get(
            Device_ID=device_id).Run_Count
        UG = Before_DGMA_INSTALLATION.objects.get(
            Device_ID=device_id).Units_Generated

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

    return render(request, 'asset_detail.html', {'temperature': temperature, 'description': description, 'icon': icon, 'Address': Address, 'DDOI': DDOI, 'alert_count': alert_count, 'CD': CD, 'OP': OP, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'PRH': PRH, 'PFC': PFC, 'RC': RC, 'UG': UG, 'current_time': current_time, 'EP': EP, 'DP': DP, 'DOI': DOI, 'EMMI': EMMI, 'EMMN': EMMN, 'EMS': EMS, 'CTMI': CTMI, 'CTMN': CTMN, 'CTSN': CTSN, 'CTCR': CTCR, 'FSMI': FSMI, 'FSMN': FSMN, 'FSN': FSN, 'FSL': FSL, 'DSN': DSN, 'Version': Version, 'SC': SC, 'IMEI': IMEI, 'OtherInfo': OtherInfo, 'Other': Other, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Tank_Size': Tank_Size, 'SellerName': SellerName, 'Oem': Oem, 'WSD': WSD, 'WED': WED, 'WP': WP, 'WS': WS, 'EM': EM, 'EMN': EMN, 'ESN': ESN, 'EOI': EOI, 'BM': BM, 'BMN': BMN, 'BSN': BSN, 'BOI': BOI, 'AM': AM, 'AMN': AMN, 'ASN': ASN, 'AOI': AOI, 'BCM': EM, 'BCMN': BCMN, 'BCSN': BCSN, 'BCOI': BCOI})


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
                    device_id__in=Device_ID).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(request.GET, queryset=alerts)
                alerts = myFilter.qs

                enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
                startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

            elif request.method == 'GET' and 'range' in request.GET:

                if request.GET['time_range'] == 'Last 30 mins':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 hour':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 7 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 12 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 24 hours':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 days':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 5 days':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=5)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 week':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 weeks':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 month':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=30)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 months':
                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=60)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 6 months':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=183)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 1 year':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=365)).strftime('%d-%m-%Y')

                elif request.GET['time_range'] == 'Last 2 years':

                    alerts = Alerts.objects.filter(
                        device_id__in=Device_ID, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                    myFilter = AlertFilter(
                        request.GET, queryset=alerts)
                    alerts = myFilter.qs

                    startdate = (datetime.datetime.now()
                                 ).strftime('%d-%m-%Y')
                    enddate = (datetime.datetime.now() -
                               datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

                TR = request.GET['time_range']

            else:

                alerts = Alerts.objects.filter(device_id__in=Device_ID).exclude(
                    alert_level="V").order_by('-alert_open', '-created_at')

                enddate = (Alerts.objects.filter(
                    device_id__in=Device_ID).order_by('-created_at').last().created_at).strftime('%d-%m-%Y')
                startdate = (Alerts.objects.filter(
                    device_id__in=Device_ID).order_by('-created_at').first().updated_at).strftime('%d-%m-%Y')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

            status = ['power_factor']

            alert = Alerts.objects.filter(
                device_id__in=Device_ID, alert_open=True).exclude(alert_type_name__in=status)

            Count = len(alert)

        return render(request, 'alert.html', {'alerts': alerts, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})

    if request.user.is_superuser:
        Customer_Name = 'Admin'
        TR = None
        Count = None
        alerts = None
        myFilter = None
        status = ['power_factor']

        if request.method == 'GET' and 'date' in request.GET:
            alerts = Alerts.objects.filter().exclude(
                alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

            myFilter = AlertFilter(request.GET, queryset=alerts)
            alerts = myFilter.qs

            enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
            startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':
                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(days=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(days=5)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':
                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(days=30)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':
                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(days=60)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(days=183)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(days=365)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                alerts = Alerts.objects.filter(created_at__gte=datetime.datetime.now(
                ) - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = AlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

            TR = request.GET['time_range']

        else:
            status = ['power_factor']

            alerts = Alerts.objects.filter().exclude(
                alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

            enddate = Alerts.objects.filter().order_by(
                '-created_at').exclude(alert_type_name__in=status, alert_level="V").last().created_at
            startdate = Alerts.objects.filter().order_by(
                '-created_at').exclude(alert_type_name__in=status, alert_level="V").first().updated_at

        myFilter = AlertFilter(
            request.GET, queryset=alerts)
        alerts = myFilter.qs

        alert = Alerts.objects.filter(
            alert_open=True).exclude(alert_type_name__in=status)

        Count = len(alert)

    return render(request, 'alert.html', {'alerts': alerts, 'startdate': startdate, 'enddate': enddate, 'TR': TR, 'myFilter': myFilter, 'Count': Count, 'Customer_Name': Customer_Name, 'username': username})


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
        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        SP = Service_History.objects.get(
            Device_ID=device_id).Service_Provider
        SC = Service_History.objects.get(
            Device_ID=device_id).Service_Contract
        Address = Service_History.objects.get(Device_ID=device_id).Address
        Con = Service_History.objects.get(Device_ID=device_id).Contact
        LSD = Service_History.objects.get(
            Device_ID=device_id).Last_Service_Date
        Activity = Service_History.objects.get(
            Device_ID=device_id).Activity
        Remark = Service_History.objects.get(Device_ID=device_id).Remark
        Activity1 = Service_History.objects.get(
            Device_ID=device_id).Activity1
        Remark1 = Service_History.objects.get(Device_ID=device_id).Remark1
        NSD = Service_History.objects.get(
            Device_ID=device_id).Next_Service_Date

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

    return render(request, 'service_history.html', {'temperature': temperature, 'description': description, 'icon': icon, 'Tank_Size': Tank_Size, 'Remark1': Remark1, 'Activity1': Activity1, 'alert_count': alert_count, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'Remark': Remark, 'SP': SP, 'SC': SC, 'Address': Address, 'Con': Con, 'LSD': LSD, 'Activity': Activity, 'NSD': NSD, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id})


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
        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        Rat = Device.objects.get(device_id=device_id).device_rating
        Stat = Device.objects.get(device_id=device_id).device_status
        Date = datetime.datetime.now()
        Fuel2 = round(DevicesInfo.objects.filter(
            device_id=device_id).exclude(fuel_level_litre=0).last().fuel_level_litre, 2)
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

        DOI = Asset.objects.get(Device_ID=device_id).Date_Of_Installation

        WS = Asset.objects.get(Device_ID=device_id).Warranty_Status

        LSD = Service_History.objects.get(
            Device_ID=device_id).Last_Service_Date
        NSD = Service_History.objects.get(
            Device_ID=device_id).Next_Service_Date
        SP = Service_History.objects.get(
            Device_ID=device_id).Service_Provider

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

    return render(request, 'dgmsDashboard.html', {'temperature': temperature, 'description': description, 'icon': icon, 'Fuel2': Fuel2, 'DDOI': DDOI, 'alert_count': alert_count, 'Fuel1': Fuel1, 'Time': Time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Fuel2': Fuel2, 'Tank_Size': Tank_Size, 'Fuel_Per': Fuel_Per, 'hh': hh, 'UG': UG, 'Carbon_Foot_Print': Carbon_Foot_Print, 'BV': BV, 'AvgFC': AvgFC, 'Energy_OA': Energy_OA, 'MaxDLoad': MaxDLoad, 'DeviceC': DeviceC, 'DOI': DOI, 'WS': WS, 'LSD': LSD, 'NSD': NSD, 'SP': SP, 'Star': Star, 'RT': RT, 'diff': diff, 'Level': Level, 'Fuel1': Fuel1, 'Time': Time})


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
        RC = []
        VLL = []
        VLN = []
        FREQ = []
        Time1 = []
        Time = []

        for det in Details:
            Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
            UG.append(det.unit_generated_kwh)
            VLN.append(round(det.vln_average, 2))
            VLL.append(round(det.vll_average, 2))
            FREQ.append(round(det.frequency, 2))
            RC.append(round(det.dg_counter_ctrl, 2))

        UG.reverse()
        VLN.reverse()
        VLL.reverse()
        FREQ.reverse()
        RC.reverse()

        # RunHour1 = []
        # RunHour2 = []
        # UG1 = []
        # PS1 = []
        # BV1 = []
        # Time1 = []
        # Time = []
        # RC = []
        # DL = []
        # GSM = []
        # GB = []

        # for det in Details:
        #     if det.dg_runtime_seconds == 0:
        #         pass
        #     else:
        #         RunHour1.append(det.dg_runtime_seconds)

        #     if det.runtime_second_ctrl == 0:
        #         pass
        #     else:
        #         RunHour2.append(det.runtime_second_ctrl)

        #     if det.unit_generated_kwh == 0:
        #         pass
        #     else:
        #     UG1.append(det.unit_generated_kwh)

        #     Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
        #     DL.append(round(det.fuel_level_litre, 2))
        #     if det.dg_counter_ctrl == 0:
        #         pass
        #     else:
        #     RC.append(round(det.dg_counter_ctrl, 2))
        #     GSM.append(round(det.gsm_signal, 2))
        #     GB.append(round(det.gateway_device_battery, 2))
        #     PS1.append(det.gateway_power_status)
        #     BV1.append(det.gateway_device_battery)

        # PS1.reverse()
        # DL.reverse()
        # GSM.reverse()
        # GB.reverse()
        # BV1.reverse()
        # RC.reverse()

        # if len(PS1) == 0:
        #     PS = 'NA'
        # else:
        #     PS = PS1[-1]

        # if len(BV1) == 0:
        #     BatteryVoltage = 0
        # else:
        #     BatteryVoltage = BV1[-1]

        # PowerStatus = 0
        # if PS == 1:
        #     PowerStatus = 'Healthy'
        # else:
        #     PowerStatus = 'Battery'

        # l1 = len(RunHour1)  # [-1]
        # l2 = len(RunHour2)  # [-1]

        # if (l1 == 0) & (l2 == 0):
        #     Run = 0
        # elif l1 == 0:
        #     Run = abs(RunHour2[0] - RunHour2[-1])
        # else:
        #     Run = abs(RunHour1[0] - RunHour1[-1])

        # if len(UG1) == 0:
        #     UG = 0
        # else:
        #     UG = abs(round(UG1[0] - UG1[-1]))

        # if len(RC) == 0:
        #     DC = 0
        # else:
        #     DC = round(RC[0] - RC[-1])

        # if len(GSM) == 0:
        #     GSMSignal = 0
        # else:
        #     GSMSignal = GSM[-1]

        # seconds = Run
        # hour = seconds // 3600
        # seconds %= 3600
        # minutes = seconds // dg
        # seconds %= 60
        # hh = "%d:%02d:%02d" % (hour, minutes, seconds)

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

        return render(request, 'energyPara.html', {'temperature': temperature, 'description': description, 'icon': icon, 'DDOI': DDOI, 'RC': RC, 'VLN': VLN, 'VLL': VLL, 'FREQ': FREQ, 'alert_count': alert_count, 'Time': Time,  'TR': TR, 'myFilter': myFilter, 'UG': UG, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


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

        # WT.reverse()
        # EO.reverse()
        # CA.reverse()
        # CR.reverse()
        # CY.reverse()
        # CB.reverse()

        # MDL = []
        # LE = []
        # CF = []
        # FC = []
        # FCO = []
        # Time1 = []
        # Time = []
        # for det in Details:
        #     if det.maximum_demand_load == None:
        #         pass
        #     else:
        #         MDL.append(round(det.maximum_demand_load, 2))
        #     Time1.append(det.start_time.strftime('%Y-%m-%d %H:%M:%S'))
        #     if det.efficiency == 0 or det.efficiency == None:
        #         pass
        #     else:
        #         LE.append(round(det.efficiency, 2))
        #     if det.carbon_footprint == None:
        #         pass
        #     else:
        #         CF.append(round(det.carbon_footprint, 2))
        #     if det.fuel_consumed == None:
        #         pass
        #     else:
        #         FC.append(round(det.fuel_consumed, 2))
        #     if det.fuel_cost == None:
        #         pass
        #     else:
        #         FCO.append(round(det.fuel_cost, 2))

        # if len(MDL) == 0:
        #     MDL_avg = 0
        #     LE_avg = 0
        #     CF_avg = 0
        #     FC_avg = 0
        #     FCO_avg = 0

        # else:
        #     MDL_avg = abs(round(sum(MDL)/len(MDL), 2))
        #     LE_avg = abs(round(sum(LE)/len(LE), 2))
        #     CF_avg = abs(round(sum(CF), 2))
        #     FC_avg = abs(round(sum(FC)/len(FC), 2))
        #     FCO_avg = abs(round(sum(FCO)/len(FCO), 2))

        # MDL.reverse()
        # LE.reverse()
        # CF.reverse()

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

        return render(request, 'loadKPI.html', {'temperature': temperature, 'description': description, 'icon': icon, 'DDOI': DDOI, 'alert_count': alert_count, 'WT': WT, 'EO': EO, 'Time': Time, 'TR': TR, 'myFilter': myFilter, 'CA': CA, 'CR': CR, 'CY': CY, 'CB': CB, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


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

        DL.reverse()
        DBV.reverse()
        RPM.reverse()

        # WT = []
        # EO = []
        # CA = []
        # CR = []
        # CY = []
        # CB = []

        # for det in Details:
        #     Time1.append(det.device_time.strftime('%Y-%m-%d %H:%M:%S'))
        #     WT.append(round(det.energy_output_kw_total, 2))
        #     EO.append(round(det.energy_output_kva, 2))
        #     CA.append(round(det.current_average, 2))
        #     CR.append(round(det.current_r_phase, 2))
        #     CY.append(round(det.current_y_phase, 2))
        #     CB.append(round(det.current_b_phase, 2))

        # WT.reverse()
        # EO.reverse()
        # CA.reverse()
        # CR.reverse()
        # CY.reverse()
        # CB.reverse()

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

        return render(request, 'enginePara.html', {'temperature': temperature, 'description': description, 'icon': icon, 'DDOI': DDOI, 'alert_count': alert_count, 'Time': Time, 'myFilter': myFilter, 'TR': TR, 'DL': DL, 'RPM': RPM, 'DBV': DBV, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


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
                device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-start_time')

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
        Total_FC = 0
        Total_FCO = 0
        Total_RH1 = 0
        Total_RH = 0

        for det in Details:
            if det.run_hours == None:
                pass
            else:
                RH.append(float(det.run_hours))
                MDL.append(round(det.maximum_demand_load, 2))
                Time1.append(det.start_time.strftime('%Y-%m-%d %H:%M:%S'))
                LE.append(round(det.efficiency, 2))
                CF.append(round(det.carbon_footprint, 2))
                FC.append(round(det.fuel_consumed, 2))
                FCO.append(round(det.fuel_cost, 2))
                UG.append(round(det.energy_generated_kwh, 2))

        RH.reverse()
        MDL.reverse()
        LE.reverse()
        CF.reverse()
        FC.reverse()
        FCO.reverse()
        UG.reverse()

        Total_FC = sum(FC)
        Total_FCO = sum(FCO)
        Total_RH1 = (sum(RH)*3600)

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

        return render(request, 'performanceKPI.html', {'temperature': temperature, 'description': description, 'icon': icon, 'Total_RH': Total_RH, 'RunCount': RunCount, 'Total_FC': Total_FC, 'Total_FCO': Total_FCO, 'UG': UG, 'DDOI': DDOI, 'RH': RH, 'MDL': MDL, 'LE': LE, 'CF': CF, 'FC': FC, 'FCO': FCO, 'alert_count': alert_count, 'Time': Time, 'myFilter': myFilter, 'TR': TR, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


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

        # WT.reverse()
        # EO.reverse()
        # CA.reverse()
        # CR.reverse()
        # CY.reverse()
        # CB.reverse()

        # MDL = []
        # LE = []
        # CF = []
        # FC = []
        # FCO = []
        # Time1 = []
        # Time = []
        # for det in Details:
        #     if det.maximum_demand_load == None:
        #         pass
        #     else:
        #         MDL.append(round(det.maximum_demand_load, 2))
        #     Time1.append(det.start_time.strftime('%Y-%m-%d %H:%M:%S'))
        #     if det.efficiency == 0 or det.efficiency == None:
        #         pass
        #     else:
        #         LE.append(round(det.efficiency, 2))
        #     if det.carbon_footprint == None:
        #         pass
        #     else:
        #         CF.append(round(det.carbon_footprint, 2))
        #     if det.fuel_consumed == None:
        #         pass
        #     else:
        #         FC.append(round(det.fuel_consumed, 2))
        #     if det.fuel_cost == None:
        #         pass
        #     else:
        #         FCO.append(round(det.fuel_cost, 2))

        # if len(MDL) == 0:
        #     MDL_avg = 0
        #     LE_avg = 0s
        #     CF_avg = 0
        #     FC_avg = 0
        #     FCO_avg = 0

        # else:
        #     MDL_avg = abs(round(sum(MDL)/len(MDL), 2))
        #     LE_avg = abs(round(sum(LE)/len(LE), 2))
        #     CF_avg = abs(round(sum(CF), 2))
        #     FC_avg = abs(round(sum(FC)/len(FC), 2))
        #     FCO_avg = abs(round(sum(FCO)/len(FCO), 2))

        # MDL.reverse()
        # LE.reverse()
        # CF.reverse()

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

        return render(request, 'deviceInfoKPI.html', {'temperature': temperature, 'description': description, 'icon': icon, 'GSMSignal': GSMSignal, 'PowerStatus': PowerStatus, 'BatteryVoltage': BatteryVoltage, 'DDOI': DDOI, 'GSM': GSM, 'GB': GB, 'alert_count': alert_count, 'Time': Time, 'myFilter': myFilter, 'TR': TR, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Star': Star, 'diff': diff})


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

            enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
            startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

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

            TR = request.GET['time_range']

        else:
            Fuel = FuelFilledReport.objects.filter(
                device_id=device_id).order_by('-device_time')

            enddate = (FuelFilledReport.objects.filter(
                device_id=device_id).order_by('-device_time').last().device_time).strftime('%d-%m-%Y')
            startdate = (FuelFilledReport.objects.filter(
                device_id=device_id).order_by('-device_time').first().device_time).strftime('%d-%m-%Y')

            myFilter = FuelFilledReportFilter(request.GET, queryset=Fuel)
            Fuel = myFilter.qs

        Count = Fuel.count()
        Total = 0
        for F in Fuel:
            Total = F.fuel_added + Total

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

    return render(request, 'fuel_report.html', {'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'DDOI': DDOI, 'alert_count': alert_count, 'startdate': startdate, 'enddate': enddate, 'daterange': daterange, 'TR': TR, 'Address': Address, 'Tank_Size': Tank_Size, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'device_id': device_id, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id, 'Fuel': Fuel, 'Total': Total, 'Count': Count, 'myFilter': myFilter})


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
        # OPR = OperationalPerformanceReport.objects.filter(
        #     device_id=device_id).order_by('start_time')

        # myFilter = OperationalReportFilter(request.GET, queryset=OPR)
        # OPR = myFilter.qs

        TR = None
        Count = None
        Details = None
        myFilter = None
        daterange = None
        startdate = None
        enddate = None
        if request.method == 'GET' and 'date' in request.GET:
            OPR = OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time')

            myFilter = OperationalReportFilter(request.GET, queryset=OPR)
            OPR = myFilter.qs

            enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
            startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':

                OPR = OperationalPerformanceReport.objects.filter(device_id=device_id, start_time__gte=datetime.datetime.now(
                ) - datetime.timedelta(minutes=30)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':
                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':
                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':
                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':
                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                OPR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).order_by('-start_time')

                myFilter = OperationalReportFilter(request.GET, queryset=OPR)
                OPR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

            TR = request.GET['time_range']

        else:
            OPR = OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time')

            enddate = (OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time').last().start_time).strftime('%d-%m-%Y')
            startdate = (OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time').first().end_time).strftime('%d-%m-%Y')

            myFilter = OperationalReportFilter(request.GET, queryset=OPR)
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
        Total_RH = 0
        Total_F = 0
        Total_FC = 0
        Total_EG = 0
        Total_RH1 = 0
        RC = []
        Run1 = []
        Run = []

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
                Total_RH = 0 + Total_RH
                Run1.append(0)
            else:
                Run1.append(float(o.run_hours*3600))
                Total_RH1 = o.run_hours + Total_RH1
                Total_F = abs(o.fuel_consumed + Total_F)
                Total_FC = abs(o.fuel_cost + Total_FC)
                Total_EG = o.energy_generated_kwh + Total_EG

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

        for num in range(Count + 1):
            RC.append(num)

        RC.remove(0)

        RC.reverse()

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Address = User_Detail.objects.get(Device_ID=device_id).Address

        OP1 = zip(OPR, RC, Run)
        OP2 = zip(OPR, RC, Run)

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

    return render(request, 'operational_report.html', {'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'DDOI': DDOI, 'alert_count': alert_count, 'RC': RC, 'startdate': startdate, 'enddate': enddate, 'daterange': daterange, 'TR': TR, 'Address': Address, 'Tank_Size': Tank_Size, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'OP1': OP1, 'OP2': OP2, 'Count': Count, 'Total_RH': Total_RH, 'Total_F': Total_F, 'Total_FC': Total_FC, 'Total_EG': Total_EG, 'device_id': device_id, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id, 'myFilter': myFilter})


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
        Cit = User_Detail.objects.get(Device_ID=device_id).City
        Loc = User_Detail.objects.get(Device_ID=device_id).Location
        # PR = OperationalPerformanceReport.objects.filter(
        #     device_id=device_id).order_by('start_time')

        # myFilter = PerformanceReportFilter(request.GET, queryset=PR)
        # PR = myFilter.qs

        TR = None
        Count = None
        myFilter = None
        daterange = None
        startdate = None
        enddate = None
        if request.method == 'GET' and 'date' in request.GET:
            PR = OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time')

            myFilter = PerformanceReportFilter(request.GET, queryset=PR)
            PR = myFilter.qs

            enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
            startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

        elif request.method == 'GET' and 'range' in request.GET:

            if request.GET['time_range'] == 'Last 30 mins':

                PR = OperationalPerformanceReport.objects.filter(device_id=device_id, start_time__gte=datetime.datetime.now(
                ) - datetime.timedelta(minutes=30)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':
                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':
                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':
                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=5)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':
                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=30)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=60)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=183)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=365)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                PR = OperationalPerformanceReport.objects.filter(
                    device_id=device_id, start_time__gte=datetime.datetime.now() - datetime.timedelta(days=2*365)).order_by('-start_time')

                myFilter = PerformanceReportFilter(request.GET, queryset=PR)
                PR = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

            TR = request.GET['time_range']

        else:
            PR = OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time')

            enddate = (OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time').last().start_time).strftime('%d-%m-%Y')
            startdate = (OperationalPerformanceReport.objects.filter(
                device_id=device_id).order_by('-start_time').first().end_time).strftime('%d-%m-%Y')

            myFilter = PerformanceReportFilter(request.GET, queryset=PR)
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

        FC = []
        RH = []

        for p in PR:
            if p.run_hours == None:
                Total_RH = 0 + Total_RH
                Run1.append(0)
            else:
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
            AFC.append(round(float(f/r), 2))
        if len(AFC) == 0:
            Avg_FC = 0
        else:
            Avg_FC = abs(round(sum(AFC)/len(AFC), 2))

        for num in range(Count + 1):
            RC.append(num)

        RC.remove(0)

        RC.reverse()

        context1 = zip(PR, AFC, RC, Run)
        context2 = zip(PR, AFC, RC, Run)

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

    return render(request, 'performance_report.html', {'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'DDOI': DDOI, 'alert_count': alert_count, 'startdate': startdate, 'enddate': enddate, 'daterange': daterange, 'Avg_AL': Avg_AL, 'Avg_PL': Avg_PL, 'Avg_FC': Avg_FC, 'TR': TR, 'context2': context2, 'PR': PR, 'Address': Address, 'Tank_Size': Tank_Size, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff, 'context1': context1, 'Count': Count, 'Total_RH': Total_RH, 'Total_F': Total_F, 'device_id': device_id, 'Customer_Name': Customer_Name, 'username': username, 'Cit': Cit, 'device_id': device_id, 'myFilter': myFilter})


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

        return render(request, 'admindashboard.html', {'alert_count': alert_count, 'UserDetail': UserDetail, 'username': username, 'Total_Customer': Total_Customer, 'Location1': Location1,  'Total': Total, 'Live': Live, 'Offline': Offline})


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

    return render(request, 'customer.html', {'alert_count': alert_count, 'myFilter': myFilter, 'User_details': User_details, 'Total_User': Total_User, 'Manager_Detais': Manager_Detais})


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
    return render(request, 'update.html', {'Total': Total, 'form': form, 'price': price, 'username': username, 'alert_count': alert_count})


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
    return render(request, 'updateprice.html', {'form': form, 'username': username, 'alert_count': alert_count})


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
                device_id=device_id).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

            myFilter = DeviceAlertFilter(request.GET, queryset=alerts)
            alerts = myFilter.qs

            enddate = (request.GET['start_date']).strftime('%d-%m-%Y')
            startdate = (request.GET['end_date']).strftime('%d-%m-%Y')

        elif request.method == 'GET' and 'range' in request.GET:

            status = ['power_factor']

            if request.GET['time_range'] == 'Last 30 mins':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(minutes=30)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(minutes=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 hour':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 7 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=7)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=7)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 12 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=12)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=12)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 24 hours':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(hours=24)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(hours=24)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 days':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 5 days':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=5)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=5)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 week':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=1)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=1)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 weeks':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(weeks=2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(weeks=2)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 month':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=30)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=30)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 months':
                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=60)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now().strftime(
                    '%d-%m-%Y')).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=60)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 6 months':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=183)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now().strftime(
                    '%d-%m-%Y')).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=183)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 1 year':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=365)).strftime('%d-%m-%Y')

            elif request.GET['time_range'] == 'Last 2 years':

                alerts = Alerts.objects.filter(
                    device_id=device_id, created_at__gte=datetime.datetime.now() - datetime.timedelta(days=365*2)).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

                myFilter = DeviceAlertFilter(
                    request.GET, queryset=alerts)
                alerts = myFilter.qs

                startdate = (datetime.datetime.now()).strftime('%d-%m-%Y')
                enddate = (datetime.datetime.now() -
                           datetime.timedelta(days=2*365)).strftime('%d-%m-%Y')

            TR = request.GET['time_range']

        else:
            status = ['power_factor']

            alerts = Alerts.objects.filter(
                device_id=device_id).exclude(alert_type_name__in=status, alert_level="V").order_by('-alert_open', '-created_at')

            startdate = (Alerts.objects.filter(
                device_id=device_id).order_by('-created_at').exclude(alert_type_name__in=status, alert_level="V").first().updated_at).strftime('%d-%m-%Y')
            enddate = (Alerts.objects.filter(
                device_id=device_id).order_by('-created_at').exclude(alert_type_name__in=status, alert_level="V").last().created_at).strftime('%d-%m-%Y')

            myFilter = DeviceAlertFilter(
                request.GET, queryset=alerts)
            alerts = myFilter.qs

        alert = Alerts.objects.filter(
            device_id=device_id, alert_open=True).exclude(alert_type_name__in=status).order_by('-created_at')

        Count = len(alert)

        Tank_Size = Asset.objects.get(Device_ID=device_id).Diesel_Tank_Size
        Address = User_Detail.objects.get(Device_ID=device_id).Address

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6841e5450643e5d4ff59981dbf58944e'
        r = requests.get(url.format(Cit)).json()
        temperature = round((float(r['main']['temp'])-32)*0.555, 2)
        description = r['weather'][0]['description']
        icon = r['weather'][0]['icon']

        # http://openweathermap.org/img/w/{{icon}}.png

        return render(request, 'device_alert.html', {'temperature': temperature, 'description': description, 'icon': icon, 'startdate': startdate, 'enddate': enddate, 'Tank_Size': Tank_Size, 'Address': Address, 'TR': TR, 'myFilter': myFilter, 'alerts': alerts, 'Count': Count, 'DDOI': DDOI, 'Count': Count,  'Cit': Cit, 'Loc': Loc, 'Rat': Rat, 'Stat': Stat, 'Energy_OA': Energy_OA, 'Star': Star, 'diff': diff,  'current_time': current_time, 'device_id': device_id, 'username': username, 'Customer_Name': Customer_Name, 'Cit': Cit, 'Loc': Loc, 'Rat': Rat, })


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
