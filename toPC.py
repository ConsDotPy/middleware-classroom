#!/usr/bin/env python3
from  agent import Agent
from tinydb import TinyDB,Queue
from time import sleep
from datetime import datetime as dt
db = TinyDB("lista.json")
classPi = Agent()
while True:
    ToList = Agent.consumeFanout()
    print(ToList)
    ToValidate = [space != None for space in ToList]
    if all(ToValidate):
        toDB = ToList[2].split(" ")
        atte = dt.timestamp(dt.now())
        db.insert({'ID': str(toDB[0]), 'Nombre': str(toDB[1]), 'Fecha': str(atte)})
        db.search(User.Nombre == str(toDB[1]))
