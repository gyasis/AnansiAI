from agents.overseer_agent import OverseerAgent
from agents.task_agent import TaskAgent
from utils.message_pool import MessagePool
from models.model_pool import ModelPool

def main():
    # Initialize components
    available_agents = []
    message_pool = MessagePool()
    model_pool = ModelPool()

    # Add models to the pool
    model_pool.add_model("default", "chatgpt", "gpt-4o-mini")

    # Create an overseer agent
    overseer = OverseerAgent("I manage the agents.", available_agents, message_pool, model_pool)
    available_agents.append(overseer)

    # Create a task agent
    task_agent = overseer.create_task_agent("I perform tasks.", "default")

    # Initial message from Overseer
    print("Overseer: Hello, how can I assist you today?")
    
    # Get user input for the task
    user_task = input("Please enter your task: ")

    # Start a chat with the task agent
    overseer.start_chat(task_agent, user_task)

if __name__ == "__main__":
    main()