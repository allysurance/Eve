#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
from random import randint
import random
import json
from django.http import HttpResponse
import pprint
def fBMI(kg,heightfeet,heightinch):
	he = float((heightfeet*12 + heightinch)*2.5)/100
	he = he*he
	bmi = float(kg/he)
	return int(bmi)

def goals(request):
	#D = decimal.Decimal
	age = (request.GET.get('age'))
	sex = (request.GET.get('sex'))
	heightfeet = (request.GET.get('heightfeet'))
	#heightfeet = json.dumps(heightfeet)
	print heightfeet
	heightinch = (request.GET.get('heightinch'))
	kg = (request.GET.get('kg'))
	kg1 = float(kg)
	hinch = float(heightinch)
	hfeet = float(heightfeet)
	BMI = fBMI(kg1,hfeet,hinch)
	if(BMI<15):
		activity = 1.2
	elif(BMI>15 and BMI<18):
		activity = 1.375
	elif(BMI>18 and BMI<21):
		activity = 1.55
	elif(BMI>21 and BMI<25):
		activity = 1.725
	else:
		activity = 1.9
	activity = str(activity)
	url=str("http://www.calculator.net/calorie-calculator.html?ctype=standard&cage="+ str(age) + "&csex=" + sex + "&cheightfeet=" + heightfeet + "&cheightinch=" + heightinch + "&ckg=" + kg + "&cactivity=" + activity + "&printit=0&x=100&y=8")
	r=requests.get(url)
	soup = bs(r.text,"html.parser")
	table = soup.find_all('table')
	tr = soup.find_all('tr')
	tips = []
	for i in range(5):
		values = tr[i].text
		l = values.split()
		cal = ''
		cal = cal + l[2].split(',')[0]
		cal = cal + l[2].split(',')[1]
		if (i==1 or i==2) and BMI>18:
			tips.append({"cal":(-1)*float(cal),"weight":(-1)*float(l[6])*0.414})
		if (i==3 or i==4) and BMI<=18:
			tips.append({"cal":(-1)*float(cal),"weight":(-1)*float(l[6])*0.414})
			
	plan = []
	print tips
	for i in range(7):
		plan.append({"id":i+1,"Steps": str(randint(1,5)*randint(1,5)*randint(20,30)*360)})

	breakfast = ['1 stuffed muli/ cauli flower paratha + curd (2nos.)' ,'2 idlis/ 1 mung chila + A bowl of sambar + A small bowl of Red Chill Chutney + boiled egg white (2 nos.) ','2 Brown bread veg sandwich + + 1 Banana/ Pear/ Papaya','A medium bowl of Barley Porridge/Oats + Boiled egg white / sprouts cooked (3tbsp)','A medium bowl of Oats / Cereals + A small bowl of fresh fruits','A medium bowl of Oats / Cereals + A small bowl of fresh fruits','1 Dosa + A  bowl bowl of pumpkin sambar + A small bowl of coriander chutney + A glass of cucumber and carrot  Juice ']		
	lunch = ['2 Missi rotis or palak tilwala Brown rice (1 bowl) + A small bowl of Paneer makhni + A small bowl of capsicum + salad','1 small bowl of Brown rice + 1 bowl matki amti curry  / a small bowl lean meat / fish preparation (low oil) + Mixed veg salad','1 small bowl of roasted chicken and veggies salad + 2 Wheat Rotis + Mix veg curry + A small cup of low-fat yoghurt','1 plate of Paneer tikka kabab + brown rice veg pulao (1 bowl) + Raita','1 medium bowl of poha + a plate of fish fry + 1 Roti + A small bowl of salad','1 medium bowl of Steamed brown rice + A bowl of veggie salad + Lauki ki sabzi + Dal curry or egg white omelette','1 bowl of Veg Khichdi + 1 small bowl of Veg Raitha']
	eveningSnacks = ['1 cup  ginger tea +  2 whole wheat low on oil khakra','1 cup Green tea +  Steamed Corn (3tbsp)','1 cup Green tea + bowl of Sprouts chat','1 glass Fresh Strawberry smoothie','A glass of Buttermilk and 1 Khakra/khandvi','A cup of fat free , flavour free yoghurt + 2 flax sesame ladoo','A glass of whey protein shake + A small bowl of amaranth and raisin mix']
	dinner = ['1 veg Uttapam + mint chutney (3 tsp) + green soup (1 bowl)','1 Ragi Roti +  choley masala + Mixed vegetable  Salads (1 bowl)','1 bajra roti + a small bowl of pepper dal curry / paneer gravy + mixed veg soup (1 bowl)','Paneer frankie + cucumber sprouts salads (1 bowl) Tomato soup (1 bowl)','1 small bowl of Veg ragi semiya or ragi ball + A small cup of sambar + Mixed pepper corn salad (1 bowl)','1 palak wheat roti + usual curry + 1 bowl of Mixed veg salads','Boiled or baked sweet potato + 2 pieces boiled fish / paneer tikka + lentil and tomato soup']
	diet = []
	for i in range(7):
		diet.append({"breakfast": breakfast[i],"lunch": lunch[i],"eveningSnacks": eveningSnacks[i],"dinner":dinner[i] })
	finalJson = {"diet":diet,"workout":plan,"tips":tips}
	#finalJson = pprint.pprint(finalJson)
	return HttpResponse(json.dumps(finalJson,indent=4),content_type="application/json")

def points(request):
	steps_d = float(request.GET.get('d_steps'))
	steps_r = float(request.GET.get('r_steps'))
	cal_d = float(request.GET.get('d_cal'))
	cal_r = float(request.GET.get('r_cal'))
	cal_goal = float(cal_d/cal_r)
	steps_goal = float(steps_d/steps_r)
	points = cal_goal*100 + steps_goal*100
	return HttpResponse(json.dumps({"points":str(points)},indent=4),content_type="application/json")