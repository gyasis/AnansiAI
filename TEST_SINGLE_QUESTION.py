import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from agent_system.agents.overseer_agent import OverseerAgent
from agent_system.utils.message_pool import MessagePool
from agent_system.models.model_pool import ModelPool

def main():
    logging.info("Initializing components...")
    available_agents = []
    message_pool = MessagePool()
    model_pool = ModelPool()

    # Add models to the pool
    model_pool.add_model("default", "chatgpt", "gpt-4o-mini")

    # Create an overseer agent
    overseer = OverseerAgent("I manage the agents.", available_agents, message_pool, model_pool)
    available_agents.append(overseer)

    # Define a custom system message
    custom_system_message = """
    You are a specialized Task Agent. Your responsibilities include:
    - Handling specific tasks with a focus on efficiency and accuracy.
    - Providing detailed explanations and insights.
    - Utilizing advanced language models to generate responses.
    """

    # Create a task agent with reflection mode and a custom system message
    task_agent = overseer.create_task_agent("I perform tasks.", "default", mode='reflection', system_message=custom_system_message)

    # Initial message from Overseer
    print("Overseer: Hello, how can I assist you today?")
    
    # Get user input for the task
    user_task = input("Please enter your task: ")

    # Use ask_question method to send a message to the task agent
    overseer.ask_question(task_agent, user_task)

if __name__ == "__main__":
    main()