# models/agent.py

from config import Config

class Agent:
    def __init__(self, state='dead'):
        self.state = state
        self.age = 0
        self.color = {'alive': (1.0, 1.0, 1.0), 'dead': (0.0, 0.0, 0.0)}
        self.height = 0.0

    def set_color_and_height(self, oldest_agent):
        if self.state == 'alive':
            colors = Config.SIMULATION_PARAMS['colors']
            oldest_agent = max(1, oldest_agent)
            
            color_phase = (len(colors) - 1) * self.age / oldest_agent
            color = colors[int(color_phase)]
            self.color['alive'] = tuple(c / 255.0 for c in color)
            
            self.height = self.age / oldest_agent