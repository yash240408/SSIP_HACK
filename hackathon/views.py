from django.contrib import messages
import requests, matplotlib.pyplot as plt
from django.shortcuts import redirect,render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def login(request):
    if request.method == 'POST':
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        url = "https://espnodewebsite.000webhostapp.com/API2/loginapi.php"
        params = {
            "phone": phone,
            "password": password
        }
        r2 = requests.post(url=url, data=params)
        print(r2.text)

        res = r2.json()
        ev = res['error']
        if not ev:
            uloginid = res['user']['LOGIN_ID']
            role = res['user']['ROLE']
            ufname = res['user']['FIRST_NAME']
            ulname = res['user']['LAST_NAME']
            ugender = res['user']['GENDER']
            uaddress = res['user']['ADDRESS']
            uemail = res['user']['EMAIL_ID']
            uland = res['user']['FLAND_ACERS']
            uphone=res['user']['PHONE_NO']


            # This will store information of farmer.
            if role == "0":
                request.session['log_email'] = uemail
                request.session['log_role'] = role
                request.session['log_id'] = uloginid
                request.session['log_fname'] = ufname
                request.session['log_lname'] = ulname
                request.session['log_gender'] = ugender
                request.session['log_address'] = uaddress
                request.session['log_land'] = uland
                request.session['log_phone'] = uphone
                request.session.save()
                return redirect(farmer_dash)

            # This will store information of admin.
            else:
                request.session['log_user_email'] = uemail
                request.session['log_user_id'] = uloginid
                request.session['log_user_fname'] = ufname
                request.session['log_user_lname'] = ulname
                request.session['log_user_gender'] = ugender
                request.session['log_user_address'] = uaddress
                request.session['log_user_land'] = uland
                request.session['log_user_phone'] = uphone
                request.session['log_user_role'] = role
                request.session.save()
                return redirect(admin_dashboard)

    try:
        if request.session["log_phone"] is not None:
            return redirect(farmer_dash)
    except:
        pass
    try:
        if request.session["log_user_phone"] is not None:
            return redirect(admin_dashboard)
        else:
            return render(request, 'index.html')
    except:
        pass
    return render(request,'index.html')

def admin_dashboard(request):
    try:
        if request.session['log_user_phone'] is None:
            return redirect(login)
        else:
            records = {}
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchwarningapi.php"
            response = requests.get(url=url)
            warning_res = response.json()
            last_val= []
            ev = warning_res['error']
            records['data'] = warning_res
            for i in records["data"]["warning"]:
                last_val.append(i)
            irsensor_value=last_val[-1]["IR_VALUE"]
            soilsensor_value=last_val[-1]["SOILMOISTURE_VALUE"]
            ultrasonicsensor_value=last_val[-1]["ULTRASONIC_VALUE"]
            dhth_value = last_val[-1]["DHT_HUMIDITY_VALUE"]
            dhtt_value = last_val[-1]["DHT_TEMPERATURE_VALUE"]
            water_value=last_val[-1]["WATER_VALUE"]
            context={'irvalue':irsensor_value,
                     "soilvalue":soilsensor_value,
                     "dhthvalue":dhth_value,
                     "dhttvalue":dhtt_value,
                     "ultravalue":ultrasonicsensor_value,
                     "watervalue":water_value
                    }
            return render(request,'dashboard.html',context)
    except:
        pass
    return render(request,'index.html')

def admin_profile(request):
    try:
        if request.session["log_user_phone"] is None:
            return render(request,'index.html')
        else:
            return render(request,'profile.html')
    except:
        pass
    return render(request,'index.html')

def farmer_profile(request):
    try:
        if request.session["log_phone"] is None:
            return redirect(login)
        else:
            return render(request,'farmer_profile.html')
    except:
        pass
    return render(request,'index.html')

def admin_map(request):
    try:
        if request.session["log_user_phone"] is None:
            return redirect(login)
        else:
            return render(request,'sitemap.html')
    except:
        pass
    return render(request,'index.html')

def logout(request):
    try:
        del request.session['log_user_email']
        del request.session['log_user_id']
        del request.session['log_user_fname']
        del request.session['log_user_lname']
        del request.session['log_user_gender']
        del request.session['log_user_address']
        del request.session['log_user_land']
        del request.session['log_user_phone']
        del request.session['log_user_role']

    except:
        pass
    return render(request,'logout.html')

def farmer_logout(request):
    try:
        del request.session['log_email']
        del request.session['log_id']
        del request.session['log_fname']
        del request.session['log_lname']
        del request.session['log_gender']
        del request.session['log_address']
        del request.session['log_land']
        del request.session['log_phone']
        del request.session['log_role']
    except:
        pass
    return render(request, 'farmer_logout.html')

# Water Level
def admin_water(request):
    try:
        if request.session['log_user_phone'] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchwatersensorapi.php"
            response = requests.get(url=url)
            water_res = response.json()
            print(water_res)
            records1={}
            records1['data'] = water_res
            print(records1)
            watervalue={}
            waterdata=[]
            watertime=[]
            watervalue['water_val']= water_res['water']
            for i in watervalue['water_val']:
                waterdata.append(i['WATER_VALUE'])
                watertime.append(i['READING_TIMESTAMP'][11:16])
            # ev = r2['error']
            fig, ax = plt.subplots()
            ax.set_title('WATER LEVEL')
            ax.barh(watertime[::10], waterdata[::10], align='center')
            plt.savefig('hackathon/static/src/images/water/water.jpg')
            return render(request,'Water_Level.html', records1)
    except Exception as a:
        print(a)
        pass
    return render(request, "index.html")

# IR sensor
def admin_obstacle(request):
    try:
        if request.session["log_user_phone"] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchirsensorapi.php"
            response = requests.get(url=url)
            ir_res = response.json()
            records = {}
            records['data'] = ir_res
            irvalue={}
            irgraph=[]
            irtime=[]
            irvalue['ir_val'] = records['data']['ir']
            for i in irvalue['ir_val']:
                irgraph.append(i['IR_VALUE'])
                irtime.append(i['READING_TIME'][11:16])
            fig, ax = plt.subplots()
            ax.barh(irtime[0::5], irgraph[0::5], align='center')
            ax.set_title('OBSTACLE DETECTION')
            plt.savefig('hackathon/static/src/images/ir/ir_obstacle.jpg')
            return render(request,'Obstacle_Detection.html',records)
    except:
        pass
    return render(request,'index.html')

# Soil Moisture
def admin_moisture(request):
    try:
        if request.session["log_user_phone"] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchsoilapi.php"
            response = requests.get(url=url)
            soil_res = response.json()
            records = {}
            records['data'] = soil_res
            soilvalue={}
            soilgraph=[]
            soiltime=[]
            soilvalue['soil_val'] = records['data']['soil']
            for i in soilvalue['soil_val']:
                soilgraph.append(i['SOIL_VALUE'])
                soiltime.append(i['READING_TIMESTAMP'][11:16])
            print(soilgraph)
            print(soiltime)
            fig, ax = plt.subplots()
            ax.set_title('SOIL MOISTURE LEVEL')
            ax.barh(soiltime[::5], soilgraph[::5], align='center')
            plt.savefig('hackathon/static/src/images/soil/soil.jpg')
            return render(request,'Moisture_Level.html',records)
    except Exception as e:
        print(e)
        pass
    return render(request,'index.html')

# DONE
def admin_height(request):
    try:
        if request.session['log_user_phone'] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchultrasonicapi.php"
            response = requests.get(url=url)
            ultra_res = response.json()
            records = {}
            records['data'] = ultra_res
            ultravalue = {}
            ultragraph = []
            ultratime = []
            ultravalue['ultra_val'] = records['data']['ultrasonic']
            for i in ultravalue['ultra_val']:
                ultragraph.append(i['ULTRASONIC_VALUE'])
                ultratime.append(i['READING_TIME'][11:16])

            fig, ax = plt.subplots()
            ax.set_title('HEIGHT MEASURE')
            ax.barh(ultratime[0::5], ultragraph[0::5], align='center')
            plt.savefig('hackathon/static/src/images/ultra/height.jpg')
            return render(request, 'Height_Measure.html',records)
    except:
        pass
    return render(request, 'index.html')

# IMPLEMENTATION
def admin_warning(request):
    try:
        if request.session['log_user_phone'] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchwarningapi.php"
            response = requests.get(url=url)
            ultra_res = response.json()
            records = {}
            records['data'] = ultra_res
            print(records)
            return render(request, 'datatable.html',records)
    except Exception as e:
        print(e)
        pass
    return render(request, 'index.html')

def farmer_dash(request):
    try:
        if request.session['log_phone'] is None:
            return redirect(login)
        else:
            records = {}
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchwarningapi.php"
            response = requests.get(url=url)
            warning_res = response.json()
            last_val= []
            ev = warning_res['error']
            records['data'] = warning_res
            for i in records["data"]["warning"]:
                last_val.append(i)
            irsensor_value=last_val[-1]["IR_VALUE"]
            dht_temp_value=last_val[-1]["DHT_TEMPERATURE_VALUE"]
            dht_hum_value=last_val[-1]["DHT_HUMIDITY_VALUE"]
            ultra_value=last_val[-1]["ULTRASONIC_VALUE"]
            water_value=last_val[-1]["WATER_VALUE"]
            soil_value=last_val[-1]["SOILMOISTURE_VALUE"]
            context={'irvalue':irsensor_value,
                     "tempvalue":dht_temp_value,
                     "watervalue":water_value,
                     "humvalue":dht_hum_value,
                     "ultravalue":ultra_value,
                     "soilvalue":soil_value
                    }
            print(context)
            return render(request,'farmer_dash.html',context)
    except:
        pass
    return render(request,'index.html')

@csrf_exempt
def admin_add(request):
    try:
        if request.session["log_user_phone"] is None:
            return render(request, 'index.html')
        else:
            if request.method == 'POST':
                fname = request.POST.get("fname")
                lname = request.POST.get("lname")
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                address = request.POST.get("address")
                gender = request.POST.get("inlineRadioOptions")
                land = request.POST.get('land')

                print(fname,lname,email,phone,address,gender,land)
                # Random Password generator code
                import random
                import array
                MAX_LEN = 6
                DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

                LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',

                                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',

                                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',

                                     'z']

                UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',

                                     'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',

                                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',

                                     'Z']

                SYMBOLS = ['@', '#', '$','*']
                COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

                rand_digit = random.choice(DIGITS)

                rand_upper = random.choice(UPCASE_CHARACTERS)

                rand_lower = random.choice(LOCASE_CHARACTERS)

                rand_symbol = random.choice(SYMBOLS)

                temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

                for x in range(MAX_LEN - 4):
                    temp_pass = temp_pass + random.choice(COMBINED_LIST)

                    temp_pass_list = array.array('u', temp_pass)

                    random.shuffle(temp_pass_list)

                password = ""

                for x in temp_pass_list:
                    password = password + x
                print(password)
                print(len(password))


                # # Email Code
                # import smtplib
                # gmail_user = 'projectrailway002@gmail.com'
                # gmail_password = 'spicljeotjmnwzdh'
                # sent_from = gmail_user
                # to = [email]
                # subject = 'Railway Project Account New Password.'
                # body = 'The password for Railway Project.\n ' \
                #        'Your password for your Railway Project Account is ' \
                #        ' ' + str(password)
                #
                # email_text = """\
                #                      From: %s
                #                      To: %s
                #                      Subject: %s
                #
                #                      %s
                #                      """ % (sent_from, ", ".join(to), subject, body)
                # try:
                #     smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                #     smtp_server.ehlo()
                #     smtp_server.login(gmail_user, gmail_password)
                #     smtp_server.sendmail(sent_from, to, email_text)
                #     smtp_server.close()
                #     print("Email sent successfully!")
                # except Exception as ex:
                #     print("Something went wrong….", ex)
                # message = 'New Password has been sent to your email.'

                # Phone sms code
                spass=password
                print('This is s pass'+spass)
                url4 = f"https://2factor.in/API/V1/e4101674-4627-11ed-9c12-0200cd936042/SMS/+91{phone}/{spass}/OTP1"
                r4= requests.get(url4)
                print(r4.text)

                url2 = "https://espnodewebsite.000webhostapp.com/API2/signupapi.php"
                params1 = {
                    'fname': fname,
                    'lname': lname,
                    'email': email,
                    'password': password,
                    'phone': phone,
                    'address': address,
                    'gender': gender,
                    'land':land
                }

                rtt55 = requests.post(url=url2, data=params1)
                print(rtt55.text)
                res = rtt55.json()
                ev = res['error']
                if not ev:
                    return render(request, 'form-basic.html', params1)
            else:
                return render(request,'form-basic.html')
    except:
        pass
    return render(request, 'index.html')

# QUERY
def admin_status(request):
    try:
        if request.session["log_user_phone"] is None:
            return redirect(login)
        else:
            records = {}
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchcomplainapi.php"
            response = requests.get(url=url)
            complain = response.json()
            ev = complain['error']
            records['complain'] = complain
            return render(request, 'form-wizard.html',records)
    except:
        pass
    return render(request,'index.html')


@csrf_exempt
def farmer_complain(request):
    try:
        if request.session["log_phone"] is None:
            return redirect(login)
        else:
            if request.method == "POST":
                fname = request.POST.get("fname")
                lname = request.POST.get("lname")
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                state=request.POST.get("state")
                sensor_type=request.POST.get("sensortype")
                company_name=request.POST.get("companyname")
                problem = request.POST.get("problem")
                url = "https://espnodewebsite.000webhostapp.com/API2/addcomplaint.php"
                last_val1=[]
                params = {
                           'FIRST_NAME': fname,
                           'LAST_NAME': lname,
                           'COMPLAIN_EMAIL': email,
                           'PHONE_NUMBER': phone,
                           'SELECT_STATE': state,
                           'SENSOR_TYPE': sensor_type,
                           'COMPANY_NAME': company_name,
                           'PROBLEM': problem,
                           'COMPLAIN_STATUS': 'IN PROGRESS'
                }
                for i in params.values():
                    last_val1.append(i)
                COMPLAIN_EMAIL=last_val1[2]
                COMPLAIN_FIRST_NAME=last_val1[0]
                COMPLAIN_LAST_NAME=last_val1[1]
                COMPLAIN_PROBLEM=last_val1[-2]
                import smtplib
                gmail_user = 'railwayguard345@gmail.com'
                gmail_password = 'ovntshhotwrtvsgw'
                sent_from = gmail_user
                to = ['projectrailway002@gmail.com']
                subject = 'Complain Added.'
                body = 'Complain Registered\n ' \
                       'NEW COMPLAIN REGISTERED' \
                       ' ' + str( "COMPLAIN ADDED--\t"+"\nCOMPLAIN SENDER'S EMAIL - ID --\t"+COMPLAIN_EMAIL+ " \nAND THE COMPLAIN IS REGISTERD BY\t" + COMPLAIN_FIRST_NAME+"\t" + COMPLAIN_LAST_NAME
                                  +"\nAND THE PROBLEM REGISTERED IN THE COMPLAIN IS\t" + COMPLAIN_PROBLEM)
                email_text = """\
                                                     From: %s
                                                     To: %s
                                                     Subject: %s

                                                     %s
                                                     """ % (sent_from, ", ".join(to), subject, body)
                try:
                    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    smtp_server.ehlo()
                    smtp_server.login(gmail_user, gmail_password)
                    smtp_server.sendmail(sent_from, to, email_text)
                    smtp_server.close()
                    print("Email sent successfully!")
                except Exception as ex:
                    print("Something went wrong….", ex)
                r2 = requests.post(url=url, data=params)
                print(r2.text)
                print(params)
                res = r2.json()
                return render(request,'farmer_form-wizard.html',params)
            else:
                return render(request, 'farmer_form-wizard.html')
    except:
        pass
    return render(request,'index.html')

# DONE
def admin_temp(request):
    try:
        if request.session['log_user_phone'] is None:
            return redirect(login)
        else:
            url = "https://espnodewebsite.000webhostapp.com/API2/fetchdhtapi.php"
            response = requests.get(url=url)
            dht_res = response.json()
            records = {}
            records['data'] = dht_res
            tempvalue = {}
            tempgraph = []
            temptime=[]
            humvalue = {}
            humgraph = []
            humtime = []
            tempvalue['TEMPERATURE'] = records['data']['dht']
            humvalue['HUMIDITY'] = records['data']['dht']

            # For temperature values
            for i in tempvalue['TEMPERATURE']:
                tempgraph.append(i['TEMPERATURE'])
                temptime.append(i['READING_TIMESTAMP'][11:16])
            #
            # # For humidity values
            for i in humvalue['HUMIDITY']:
                humgraph.append(i['HUMIDITY'])
                humtime.append(i['READING_TIMESTAMP'][11:16])
            #
            fig, ax = plt.subplots()
            ax.set_title('TEMPERATURE LEVEL')
            ax.barh(temptime[0::25], tempgraph[0::25], align='center')
            plt.savefig('hackathon/static/src/images/dht/temperature.jpg')
            #

            fig, ax = plt.subplots()
            ax.set_title('HUMIDITY LEVEL')
            ax.barh(humtime[0::25], humgraph[0::25], align='center')
            plt.savefig('hackathon/static/src/images/dht/humidity.jpg')

            return render(request, 'Temp_Hum.html',records)
    except:
        pass
    return render(request, 'index.html')