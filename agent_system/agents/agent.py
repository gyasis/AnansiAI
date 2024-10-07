from ..models._model_ import Model

class Agent:
    DEFAULT_MODEL_PATH = "gpt-4o-mini"  # Set to a valid model identifier

    def __init__(self, agent_type, description, model_type="chatgpt", model_path=None):
        self.agent_type = agent_type
        self.description = description
        self.id = id(self)
        # Initialize the model using the Model class
        self.model = Model(model_type, model_path or self.DEFAULT_MODEL_PATH)

    def receive_message(self, message):
        pass  # To be implemented by subclasses