#!/usr/bin/env python3
from  agent import Agent
from RFID import  ReadRFID, WriteRFID
from time import sleep
piClass = Agent()
while True:
    id, name = ReadRFID()
<<<<<<< HEAD
    piClass.produceFanout(str(id) + " " + name)
=======
    piClass.produceFanout(id + " " + name)
>>>>>>> 7c1d0453ba94ddff04d64ef8c96b92fa1c3adef6
