# backend/simulation/engine.py

import time
import threading
from models.agent import Agent
import numpy as np
import random
from config import Config

class SimulationEngine:
    def __init__(self, bounds=(800, 800), params=None):
        self.bounds = bounds
        self.agents = np.zeros(bounds)
        self.running = False
        self.params = params
        if self.params is None:
            self.params = Config.SIMULATION_PARAMS
        self.x = max(0, self.agents.shape[0] // 2)
        self.y = max(0, self.agents.shape[1] // 2)
        self.lock = threading.Lock()

    

    def initialize_agents(self, num_agents=4):
        i = -1
        while i < num_agents:
            i += 1
            self.agents[self.x, self.y] = Agent()
            if i % 4 == 0:
                self.x += 1
            if i % 4 == 1:
                self.y += 1
            if i % 4 == 2:
                self.x -= 1
            if i % 4 == 3:
                self.y -= 1
                

    def update(self):
        agent:Agent
        with self.lock:
            for i in range(len(self.agents.shape[0])):
                for j in range(len(self.agents.shape[1])):
                    agent = self.agents[i, j]
                    # from https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
                        
                    i_min = i
                    j_min = j
                    if i > 0:
                        i_min = i - 1
                    if j > 0:
                        j_min = j - 1

                    i_max = i
                    j_max = j
                    if i < self.agents.shape[0] - 1:
                        i_max = i + 1
                    if j < self.agents.shape[1] - 1:
                        j_max = j + 1
                    
                    i_tests = [i_min, i, i_max]
                    j_tests = [j_min, j, j_max]

                    neighbors = 0
                    for i_test in i_tests:
                        for j_test in j_tests:
                            if i_test == i and j_test == j:
                                continue
                            if self.agents[i_test, j_test].state == 'alive':
                                neighbors += 1
                    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                    # Any live cell with more than three live neighbours dies, as if by overpopulation.
                    # Any live cell with two or three live neighbours lives on to the next generation.
                    if neighbors < 2 or neighbors > 3:
                        agent.state = 'dead'
                        
                    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                    if neighbors == 3:
                        agent.state = 'alive'
                        
                    

    def get_state(self):
        agent:Agent
        with self.lock:
            # return {
            #     'agents': self.agents
            # }

            # the statement below returns a list of dictionaries based on the agent properties.  this works well with a web application that can't 
            # jsonify a custom class.
            ans = []
            for i in range(len(self.agents.shape[0])):
                for j in range(len(self.agents.shape[1])):
                    agent = self.agents[i, j]
                    ans.append({
                        'id': agent.id,
                        'position': [i, j],
                        'state': agent.state,
                        'color': agent.color,
                    })
            return ans

    def run(self, update_interval=0.1):
        self.running = True
        while self.running:
            self.update()
            # time.sleep(update_interval)

    def stop(self):
        self.running = False
