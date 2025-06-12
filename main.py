from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization import CanvasGrid, ModularServer
from mesa.datacollection import DataCollector
import random
from medical import MedicalAidAgent
from search import SearchRescueAgent
from logistics import LogisticsAgent
from coordinator import CoordinatorAgent
from engineer import EngineerAgent

# main model
class DisasterResponseModel(Model):
    def __init__(self, width, height, num_agents_each):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.reported_victims = []
        self.debris_locations = [(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(10)]
        self.field_hospitals = []

        self.datacollector = DataCollector(
            agent_reporters={"Position": "pos"}
        )

        agent_classes = [SearchRescueAgent, MedicalAidAgent, LogisticsAgent, EngineerAgent, CoordinatorAgent]
        for agent_class in agent_classes:
            for i in range(num_agents_each):
                agent = agent_class(f"{agent_class.__name__}_{i}", self)
                self.schedule.add(agent)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def broadcast_victim_location(self, pos):
        if pos not in self.reported_victims:
            self.reported_victims.append(pos)

    def get_closer_position(self, current_pos, target_pos):
        x, y = current_pos
        tx, ty = target_pos
        new_x = x + (1 if tx > x else -1 if tx < x else 0)
        new_y = y + (1 if ty > y else -1 if ty < y else 0)
        return (new_x % self.grid.width, new_y % self.grid.height)

# Visualization
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.8,
        "text": str(agent.unique_id),
        "text_color": "white"
    }
    color_map = {
        SearchRescueAgent: "red",
        MedicalAidAgent: "green",
        LogisticsAgent: "blue",
        EngineerAgent: "orange",
        CoordinatorAgent: "purple"
    }
    portrayal["Color"] = color_map.get(type(agent), "gray")

    if hasattr(agent.model, 'field_hospitals') and agent.pos in agent.model.field_hospitals:
        portrayal["Layer"] = 1
        portrayal["Color"] = "lightblue"

    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(
    DisasterResponseModel,
    [grid],
    "Disaster Response Model",
    {"width": 10, "height": 10, "num_agents_each": 3}
)

server.launch()