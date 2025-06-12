from mesa import Agent


class CoordinatorAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.maintain_communication()
        self.prioritize_areas()
        self.make_global_decision()

    def maintain_communication(self):
        print(f"[CoordinatorAgent {self.unique_id}] relaying info from field agents")

    def prioritize_areas(self):
        center = (self.model.grid.width // 2, self.model.grid.height // 2)
        self.model.reported_victims.sort(key=lambda pos: abs(pos[0] - center[0]) + abs(pos[1] - center[1]))
        print(f"[CoordinatorAgent {self.unique_id}] prioritized victims: {self.model.reported_victims}")

    def make_global_decision(self):
        if len(self.model.reported_victims) > 5:
            print(f"[CoordinatorAgent {self.unique_id}] dispatching additional resources!")
