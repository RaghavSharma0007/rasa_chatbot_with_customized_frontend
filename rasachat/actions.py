# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import difflib
import random

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted 

import sqlite3
import logging
import requests
import json
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted , Restarted




logger = logging.getLogger(__name__)

class ActionFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = "I'm sorry. Please enter expected details."
        dispatcher.utter_message(message)

        return [UserUtteranceReverted()]

class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        print("restart has been printed")
        return [Restarted()]



class Actionnorth(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_north"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        foodn= tracker.get_slot('food')
        con = sqlite3.connect('chatbot.db')
        with con:
    

            cur = con.cursor()
            cur.execute('SELECT id, item name,price FROM restuarant')
            rows = cur.fetchall()
            b=foodn
            c=str(b)
            print('food',b)
 
            for i in range(4):
        
                a=rows[i][1]
                print('a',a)
                seq = difflib.SequenceMatcher(None,a,c)
                d = seq.ratio()*100
                print('d',d)
                print('north')
                if d>=60.0:
                    print(rows[i][1])
                    message='Please enter your address and mobile number. Your address must be within the 5 km distance range from Punjabi Tadka.'
                    dispatcher.utter_message(message)
                    return []
                elif i==3:
                    message='Please enter North Indian food item name.'
                    dispatcher.utter_message(message)
                    return [UserUtteranceReverted()]

class Actionsouth(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_south"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        foods = tracker.get_slot('food')
        con = sqlite3.connect('chatbot.db')
        with con:
    

            cur = con.cursor()
            cur.execute('SELECT id, item name,price FROM restuarant')
            rows = cur.fetchall()
            b=foods
            c=str(b)
            print(b)
            print('south')
            for i in range(4,8):
        
                a=rows[i][1]
                seq = difflib.SequenceMatcher(None,a,c)
                d = seq.ratio()*100
        
                if d>=60.0:
                    print(rows[i][1])
                    message='Mention your address and mobile number. Your address must be within the 5 km distance range from Punjabi Tadka.'
                    dispatcher.utter_message(message)
                    return []
                elif i==7:
                    message='Please enter South Indian food item name.'
                    dispatcher.utter_message(message)
                    return [UserUtteranceReverted()]
        





class ActionJoke(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_distance"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        food = tracker.get_slot('food')
        house= tracker.get_slot('house')
        add = tracker.get_slot('address')
        mobile = tracker.get_slot('mobile')
        if house == None or add == None or mobile == None:
            message5 = 'Please enter the complete address and the mobile number'
            dispatcher.utter_message(message5)
            return [UserUtteranceReverted()]
        else:
            u = house.split()
            l = len(u)
            # x= list(house)
            k = '#' in house
            if k == True:
                if u[0] == '#':
                    n = '#' + u[1]
                    print(n)
                else:
                    n = u[0]
                    print(n)
            elif l == 1:
                n = '#' + house
                print(n)
            else:
                n = '#' + u[l - 1]
                print(n)

            origins = "sec-23,chandigarh"

            print(house)
            print(add)
            print(mobile)

            con = sqlite3.connect('chatbot.db')
            with con:

                cur = con.cursor()
                cur.execute('SELECT id, item name,price FROM restuarant')
                rows = cur.fetchall()

                for i in range(8):
                    # print(rows[i][1])
                    a = rows[i][1]
                    seq = difflib.SequenceMatcher(None, a, food)
                    d = seq.ratio() * 100

                    if d >= 60.0:
                        item = rows[i][1]
                        price = rows[i][2]
                        # print(d)

            key = 'AIzaSyC1PaCkmpMXcJygTZPByALiE8dCiqNwVo4'
            units = 'imperial'
            api = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=' + units + '&origins=' + origins + '&destinations=' + add + '&key=' + key
            request = json.loads(requests.get(api).text)
            # req = requests.get(api).text
            distance = request['rows'][0]['elements'][0]['distance']['text']
            Add = request['destination_addresses']
            Address = Add[0]
            # print(req)
            x = distance.split()
            y = float(x[0])
            if (y <= 3):

                message1 = "Selected item: {}".format(item)
                message2 = "Address: {}, {}".format(n, Address)
                message3= "Mobile no: {}".format(mobile)
                message4 = "Amount to be paid: Rs {}. To confirm click on 'yes', otherwise click on 'no'.".format(price)

                button = [{'title': 'Yes',
                           'payload': '/user_affirm'},
                          {'title': 'No',
                           'payload': '/user_deny'}]
                dispatcher.utter_message(message1)
                dispatcher.utter_message(message2)
                dispatcher.utter_message(message3)
                dispatcher.utter_button_message(message4, buttons=button)
                return []



            else:
                dispatcher.utter_message(
                    'I am very sorry. I can not place order for travelling distance more than 5 Km.')
                dispatcher.utter_message('Please enter address and mobile number within distance range.')
                return [UserUtteranceReverted()]


class Action_order(Action):
    def name(self):
        # define the name of the action which can then be included in training stories
        return "action_order"

    def run(self, dispatcher, tracker, domain):
        # what your action should do
        food1 = tracker.get_slot('food')
        #house= tracker.get_slot('house')
        #origins="sec-23,chandigarh"
        #add=tracker.get_slot('address')
        #mobile=tracker.get_slot('mobile')
        con = sqlite3.connect('chatbot.db')
        



        with con:
    

            cur = con.cursor()
            cur.execute('SELECT id, item name,price FROM restuarant')
            rows = cur.fetchall()
            
            for i in range(8):
                
                a=rows[i][1]
                seq = difflib.SequenceMatcher(None,a,food1)
                d = seq.ratio()*100
        
                if d>=70.0:
                    item1=rows[i][1]
                    price=rows[i][2]
                    print(d)
        url='http://api.timezonedb.com/v2.1/get-time-zone?key=OA3Q8MJLH6OJ&format=json&by=zone&zone=Asia/Kolkata'
        request = json.loads(requests.get(url).text)
        dt=request['formatted']
        dt_current=dt.split()
        date=dt_current[0]
        time=dt_current[1]
        order_id=random.randint(10000,99999)
        #key='AIzaSyA8fAAXYG2OkiM2PSCOeH-NCTGqYi1obFw'
        #units='imperial'
        #api='https://maps.googleapis.com/maps/api/distancematrix/json?units='+units+'&origins='+origins+'&destinations='+sec+city+'&key='+key
        #request = json.loads(requests.get(api).text)
        #distance=request['rows'][0]['elements'][0]['distance']['text']
        #address= request['destination_addresses']
        #x = distance.split()
        #y = float(x[0])
        #if (y<=3):
        message1 = "Your order for {} has been placed with Order Id {} on {} at {}.".format(item1, order_id, date, time)
        message2 = "Amount to be paid: Rs {}.".format(price)
        # message3 ="Our agent will visit your address: {}, {} within 30 minutes.".format(house,address)
        dispatcher.utter_message(message1)
        dispatcher.utter_message(message2)
        # dispatcher.utter_message(message3)
        return []
        #else:
          #  dispatcher.utter_message('I am very sorry. I can not place order for travelling distance more than 5 km.')
           # return []
        
