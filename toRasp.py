#!/usr/bin/env python3
from  agent import Agent
from RFID import  ReadRFID, WriteRFID
from time import sleep
piClass = Agent()
while True:
    id, name = ReadRFID()
    classPi.produceFanout(str(id) + " " + str(name))
