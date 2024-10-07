from .agent import Agent
from ..models.model_pool import ModelPool, Model
from .task_agent import TaskAgent
import logging
import re

class OverseerAgent(Agent):
    def __init__(self, description, available_agents, message_pool, model_pool, model_type="chatgpt", model_path=None):
        super().__init__('Overseer', description, model_type, model_path)
        self.available_agents = available_agents
        self.message_pool = message_pool
        self.model_pool = model_pool
        self.self_nomination_count = 0  # Track consecutive self-nominations
        self.overseer_id = self.id  # Store the overseer's own ID
        self.model_type = model_type  # Ensure model_type is stored
        self.model_path = model_path or self.DEFAULT_MODEL_PATH  # Ensure model_path is stored
        logging.debug("OverseerAgent initialized with description: '%s'", description)

        # Initialize the overseer's own model
        self.model = Model(self.model_type, self.model_path)
        logging.info(f"OverseerAgent model initialized: {self.model_type} with path: {self.model_path}")

    def receive_message(self, message):
        logging.debug("Received message: '%s'", message)
        prompt = f"Route this message to agent that can best process to handle the task as quickly as possible: {message}"
        lm_output = self.model.generate(prompt)
        logging.debug("Generated LM output: '%s'", lm_output)
        target_agent = self.route_message(lm_output)
        logging.debug("Routing message to target agent: '%s'", target_agent.id)
        target_agent.receive_message(message)

    def route_message(self, lm_output):
        logging.debug("Routing message based on LM output: '%s'", lm_output)
        return self.available_agents[0]  # Simplified for demonstration

    def create_task_agent(self, description, model_name, mode='normal', system_message=None, max_tokens=100):
        logging.debug("Creating TaskAgent with description: '%s', model_name: '%s', mode: '%s'", description, model_name, mode)
        model = self.model_pool.get_model(model_name)
        if model:
            logging.debug("Model found: '%s'", model_name)
            cloned_model = model.clone()  # Clone the existing model
            task_agent = TaskAgent(description, model_type=cloned_model.model_type, model_path=cloned_model.model_path, mode=mode, system_message=system_message, max_tokens=max_tokens)
            self.available_agents.append(task_agent)
            logging.info("TaskAgent created: %s with model: %s, mode: %s", task_agent.id, cloned_model.model_type, mode)
            return task_agent
        else:
            logging.error("Model '%s' not found in the pool.", model_name)
            raise ValueError(f"Model '{model_name}' not found in the pool.")

    def ask_question(self, task_agent, initial_message):
        logging.debug("Asking question to TaskAgent: '%s'", initial_message)
        task_agent.receive_message(initial_message)

    def start_chat(self, task_agent, initial_message):
        logging.debug("Starting chat with TaskAgent: '%s'", initial_message)
        response = task_agent.receive_message(initial_message)
        
        while True:
            logging.debug("Received response from TaskAgent: '%s'", response)
            if re.search(r'\bTERMINATE\b', response):
                logging.info("TaskAgent indicates task completion.")
                break
            
            if self.evaluate(response):
                logging.info("Overseer evaluates the task as complete.")
                break
            try:
                logging.info("Nominating next agent based on response: '%s'", response)
                logging.info("Available agents: %s", [agent.id for agent in self.available_agents])
                self.nominate(self.available_agents, response)
            except Exception as e:
                logging.error("Error during agent nomination: %s", str(e))
            finally:
                logging.info("Agent nomination process completed")
            user_decision = input("Do you want to continue the chat? (yes/no): ").strip().lower()
            logging.debug("User decision to continue chat: '%s'", user_decision)
            if user_decision == 'no':
                logging.info("Ending chat session.")
                break
            else:
                next_message = input("Enter next message for TaskAgent: ")
                logging.debug("Next message for TaskAgent: '%s'", next_message)
                response = task_agent.receive_message(next_message)

    def evaluate(self, response):
        logging.debug("Evaluating response: '%s'", response)
        return "complete" in response.lower()

    def nominate(self, agents, response):
        logging.info("Nominating next agent based on response: '%s'", response)
        
        # Populate options
        options = [f"{agent.description}" for agent in agents]
        
        # Log the options to check if they are populated
        logging.info(f"Available options: {options}")
        
        custom_system_prompt = "Select the best agent for the task based on the following options:"
        
        # Check if options are empty
        if not options:
            logging.error("No available agents to nominate.")
            raise ValueError("No available agents to nominate.")
        
        # Log the current state of the model
        logging.info(f"Current model: {self.model}")
        
        try:
            # Check if the model is None
            if self.model is None:
                raise ValueError("Model is not initialized.")
            
            selected_option = self.model.selection(response, options, custom_system_prompt)
            logging.info(f"Selected option: {selected_option}")
            # Logic to route to the selected agent
        except ValueError as e:
            logging.error(f"Selection error: {str(e)}")
        except Exception as e:
            logging.error(f"Error during agent nomination: {str(e)}")

    def get_system_message(self):
        logging.debug("Getting system message.")
        return """
        You are the Overseer Agent. Your responsibilities include:
        - Managing the system of agents.
        - Routing messages to the appropriate task agents.
        - Ensuring efficient task completion.
        """