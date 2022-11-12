# ----------------------------------------------------------
# M1. Actividad
#
# Date: 11-Nov-2022
# Authors:
#           A01379299 Ricardo R. Condado
#
# ----------------------------------------------------------

from Cleaner import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agente):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.6}


    if isinstance(agente, Cleanner):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0.2
    else:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0.5
        portrayal["r"] = 0.4
    return portrayal


_N = 15
_M = 15
numAgents = 8
ttrash = 40
_time = 200


grid = CanvasGrid(agent_portrayal, _N, _M, 750, 750)
server = ModularServer(Roomba,
                       [grid],
                       "Roomba",
                       {"_N": _N,
                        "_M": _M,
                        "numAgents": numAgents,
                        "ttrash": ttrash,
                        "_time": _time})
server.port = 8521  # Puerto default
server.launch()
