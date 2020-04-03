#!/usr/bin/env python3
from  agent import Agent
piClass = Agent(host = '192.168.0.5')
piClass.produceFanout("Hola, esto es fanout de Publisher a Subcriptor")
