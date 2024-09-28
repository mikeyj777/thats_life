# main_3d.py

from simulation.engine import SimulationEngine
from view.renderer import Renderer
import traceback

def main():
    try:
        print("Initializing simulation...")
        simulation = SimulationEngine()
        print("Simulation initialized.")
        
        print("Creating renderer...")
        renderer = Renderer(simulation)
        print("Renderer created.")
        
        print("Starting renderer...")
        renderer.start()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()