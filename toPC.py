#!/usr/bin/env python3
from  agent import Agent
from tinydb import TinyDB,Query
from time import sleep
from datetime import datetime as dt
db = TinyDB("lista.json")
User = Query()
classPi = Agent()
name, channel = classPi.getNameFanout()
while True:
    ToList = classPi.consumeFanout(name, channel)
    if ToList != None:
        ToValidate = [space != None for space in ToList]
        if all(ToValidate):
            dec = ToList[2].decode("utf-8")
            toDB = dec.split(" ")
            atte = dt.timestamp(dt.now())
            db.insert({'ID': str(toDB[0]), 'Nombre': str(toDB[1] + " " + toDB[2]), 'Fecha': str(atte)})
            db.search(User.Nombre == str(toDB[1]))
