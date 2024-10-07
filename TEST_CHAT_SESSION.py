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

    # Create an overseer agent with a clear name
    overseer_description = "Overseer: I manage the agents."
    overseer = OverseerAgent(overseer_description, available_agents, message_pool, model_pool)
    available_agents.append(overseer)

    # Log overseer details
    logging.info(f"OverseerAgent created: {overseer.id} with description: {overseer.description}")

    # Create a single task agent with reflection mode
    task_agent_name = "TaskAgent1"
    task_agent_description = f"{task_agent_name}: I perform tasks."
    task_agent = overseer.create_task_agent(task_agent_description, "default", mode='reflection')
    available_agents.append(task_agent)

    # Log task agent details
    logging.info(f"TaskAgent created: {task_agent.id} with description: {task_agent.description}")

    # Initial message from Overseer
    print("Overseer: Please describe the task you need assistance with.")
    
    # Get user input for the task
    user_task = input("Task description: ")

    # Use the selection method to decide on the agent
    custom_system_prompt = "Select the best agent for the task based on the following options:"
    options = [agent.description for agent in available_agents if agent.agent_type == 'Task']
    
    try:
        selected_option = overseer.model.selection(user_task, options, custom_system_prompt)
        logging.info(f"Selected option: {selected_option}")
        
        # Find the selected agent by description
        selected_agent = next(agent for agent in available_agents if agent.description == selected_option)
        
        # Start a chat with the selected agent
        overseer.start_chat(selected_agent, user_task)
    except ValueError as e:
        logging.error(f"Selection error: {str(e)}")

    # Check for self-nomination
    if overseer.self_nomination_count > 0:
        overseer.prompt_human(user_task)

if __name__ == "__main__":
    main()