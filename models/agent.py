# backend/models/agent.py

import numpy as np
import uuid
import random
from config import Config

class Agent:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.state = 'alive'
        self.set_color()
        self.age = 0
    
    def set_color(self):
        colors = Config.SIMULATION_PARAMS['colors']
        color = random.choice(colors)
        color = np.array(color, dtype=float)
        color /= 255
        # color = (1, 1, 1)
        self.color = {
            'alive': color,
            'dead': (0, 0, 0)
        }

    