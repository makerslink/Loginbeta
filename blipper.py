#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Simple script for registering members coming and going. """

import sqlite3 as lite
import time
import requests
import hasher
import getpass
import users

def wait_for_valid_rfid():
    while True:
        try:
            temp = getpass.getpass("Blip me! ")
            rfid = hasher.encode(temp)
            break
        except ValueError:
            print("Blip not recognised")
    print("")

    return rfid


def log_action(who, what):
    requests.put('http://127.0.0.1:5001/', json = {'who': who, 'what': what})


def trigger_random_sound():
    try:
        requests.get('http://192.168.42.12:5000/',timeout=0.001)
    except:
        pass


while True:
    rfid_tag_id = wait_for_valid_rfid()

    user = users.fetch(rfid_tag_id)

    if not user:
        print("-----------------------------------------------")
        print('There is no rfidtag named {rfid}, creating user!'.format(rfid=rfid_tag_id))

        new_user_nick = input("input your nick: ")

        users.add(new_user_nick, rfid_tag_id)

        log_action(new_user_nick, 'login')

        trigger_random_sound()

        print('You now exist and are logged in! Dont forget to logout!')
        print("-----------------------------------------------")
    else:
        if user['isHere']:
            users.logout(rfid_tag_id)

            log_action(user['Nick'], 'logout')

            trigger_random_sound()

            user = users.fetch(rfid_tag_id)

            print("-----------------------------------------------")
            print('Goodbye {Nick}, your highscore is: {totalTime}'.format(**user))
            print("-----------------------------------------------")

        else:
            users.login(rfid_tag_id)

            log_action(user['Nick'], 'login')

            trigger_random_sound()

            print("-----------------------------------------------")
            print("Welcome {Nick}!".format(**user))
            print("-----------------------------------------------")
