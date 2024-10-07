import logging
from agent_system.agents.overseer_agent import OverseerAgent
from agent_system.utils.message_pool import MessagePool
from agent_system.models.model_pool import ModelPool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    # Define agent descriptions
    agent_descriptions = [
        ("Scientist", "I conduct experiments and analyze data."),
        ("Engineer", "I design and build systems and structures."),
        ("Researcher", "I investigate and study various topics to gather information.")
    ]

    # Create task agents for each description
    for name, description in agent_descriptions:
        task_agent = overseer.create_task_agent(description, "default")
        available_agents.append(task_agent)

    # Initial message from Overseer
    print("Overseer: Please describe the task you need assistance with.")
    
    # Get user input for the task
    user_task = input("Task description: ")

    # Use the selection method to nominate the best agent
    custom_system_prompt = "Select the best agent for the task based on the following options:"
    options = [f"{agent.id}: {agent.description}" for agent in available_agents if agent.agent_type == 'Task']
    
    try:
        selected_option = overseer.model.selection(user_task, options, custom_system_prompt)
        logging.info(f"Selected option: {selected_option}")
        
        # Extract the selected agent's ID from the selection result
        selected_agent_id = int(selected_option.split(":")[0].strip())
        selected_agent = next(agent for agent in available_agents if agent.id == selected_agent_id)
        
        # Start a chat with the selected agent
        overseer.start_chat(selected_agent, user_task)
    except ValueError as e:
        logging.error(f"Selection error: {str(e)}")

if __name__ == "__main__":
    main()