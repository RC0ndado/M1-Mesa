# ----------------------------------------------------------
# M1. Actividad
#
# Date: 11-Nov-2022
# Authors:
#           A01379299 Ricardo R. Condado
# ----------------------------------------------------------

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner


def CreateGraph(model):
    return model.stepsTime


class Garbage(Agent):
    """
    We decide to model two agents, one for 
    be a cleaner (vaccum), another for be part
    of the garbage.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Cleanner(Agent):
    """
        This represent the other class
        (code from the tutorial Mesa Python).
        But this part also has a modification
        to the code, we add a new functions for 
        the agent will delete the trash in the
        grid.
    """
    _step = 0
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        

    def clean(self, agent):     # Check 
        self.model.grid.remove_agent(agent)
        self.model.cleanCells += 1
        
    def step(self):
        """
        This part check into the grid what is the trash
        and then remove and clean the part. The method
        is similar to the 
        """
        
        gridContent = self.model.grid.get_cell_list_contents([self.pos])
        trash = False
        trashElements = None
        
        for element in gridContent:
            if isinstance(element, Garbage):
                trash = True
                trashElements = element
            if not trash:
                Cleanner._step += 1
                self.move()
            else:
                self.clean(trashElements)
    
class Roomba(Model):
    def __init__(self, numAgents, _M, _N, ttrash, _time):
        
        self.grid = MultiGrid(_M, _N, False)
        self.numAgents = numAgents
        self.tle = _time
        self.stepsTime = 0
        self.dirtyCells = int((ttrash * (_N*_M)) / 100)
        self.cleanCells = 0
        self.schedule = RandomActivation(self)
        self.running = True
        self.cleanLimit = False
        
        # Create agents
        for i in range(0, self.numAgents):
            agente = Cleanner(i, self)
            self.schedule.add(agente)
            
            self.grid.place_agent(agente, (1,1))
            
        trashCelda = set()
        for j in range(self.numAgents+1, self.dirtyCells+self.numAgents+1):
            container = Garbage(j, self)
            self.schedule.add(container)
            Cleanner._step = 0
            
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            
            while (x,y) in trashCelda:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            trashCelda.add((x, y))
            self.grid.place_agent(container, (x, y))
        
    def step(self):
        if(self.cleanCells == self.dirtyCells):
            self.cleanLimit = True
            
        if(self.cleanLimit or self.tle == self.stepsTime):
                self.running = False
            
                if(self.cleanLimit):
                    print("\nThe cleaner clean all the trash\n")
                else:
                    print("\nThe cleaner didn't clean all the trash\n")
                    
            #print("\nThe cleaner clean " + str(self.cleanCells) + " cells\n")
            #print("\nThe cleaner didn't clean " + str(self.dirtyCells - self.cleanCells) + " cells\n")
            #print("\nThe cleaner took " + str(self.stepsTime) + " steps\n")
            #print("\nThe cleaner took " + str(self.stepsTime / self.dirtyCells) + " steps per cell\n")
            #print("\nThe cleaner took " + str(self.stepsTime / self.cleanCells) + " steps per clean cell\n")
            #print("\nThe cleaner took " + str(self.stepsTime / self.numAgents) + " steps per agent\n")
            #print("\nThe cleaner took " + str(self.stepsTime / (self.numAgents * self.dirtyCells)) + " steps per agent per cell\n")
            #print("\nThe cleaner took " + str(self.stepsTime / (self.numAgents * self.cleanCells)) + " steps per agent per clean cell\n")
            
                print("\nTime: " + str(self.stepsTime) + " \n")
                print("\nPercentage: " +str(int((self.cleanCells*100)/self.dirtyCells)) + " % \n")
                print("\n Move: " + str(Cleanner._step) + " \n")
            
        else:
            self.stepsTime +=1
            self.schedule.step()
            #self.remaining_steps -= 1
