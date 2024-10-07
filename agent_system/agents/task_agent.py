from .agent import Agent
from ..models._model_ import Model

class TaskAgent(Agent):
    def __init__(self, description, model_type="chatgpt", model_path=None, mode='normal', system_message=None, max_tokens=100):
        super().__init__('Task', description, model_type, model_path)
        self.model = Model(model_type, model_path or self.DEFAULT_MODEL_PATH)
        self.mode = mode  # Store the mode as an attribute
        self.custom_system_message = system_message  # Store the custom system message
        self.max_tokens = max_tokens  # Store the max tokens

    def receive_message(self, message):
        return self.process_message(message, self.mode)  # Return the response

    def process_message(self, message, mode='normal'):
        if mode == 'reflection':
            return self.reflection(message)
        elif mode == 'chain_of_thought':
            return self.chain_of_thought()
        elif mode == 'round':
            return self.round()
        else:
            return self.default_process(message)

    def default_process(self, message):
        system_message = self.get_system_message()
        prompt = f"{system_message} {message}"
        response = self.model.generate(prompt, max_tokens=self.max_tokens)
        
        # Append termination message if task is complete
        if "TERMINATE" in response:
            response += "\nTask complete. TERMINATE"
        
        print(f"TaskAgent {self.id} response: {response}")
        return response  # Return the response

    def reflection(self, message):
        """Reflect on the task before attempting to complete it."""
        reflection_prompt = f"""
        Before attempting to complete the task described in the message, take a moment to reflect on it. The message which consists of a task(question or request) and may or may not have chat history attached. Consider the following:

        1. What is the nature of the task?
        2. What skills or knowledge might be required to complete it?
        3. Are there any potential challenges or considerations?
        4. If there is chat history is there anything that can help with insights, tips, past mistakes, outside information?
        5. What steps might be involved in solving this task?

        After your reflection, provide your thoughts in a <reflection> tag. Then, attempt to complete the task based on your reflection.

        Your response should be structured as follows:

        ## Reflection
        [Your reflection on the task, considering the points mentioned above]
     

        ## Task Attempt
        [Your attempt to complete the task based on your reflection]
    
        Remember to think carefully about the task before attempting it, and use proper spelling and grammar in your response.

        Now here is the message {message}

        Based on the message my response is : 
        """
        # Use regex to constrain generation to stop at the closing </task_attempt> tag
        reflect_response = self.model.generate(
            reflection_prompt,
            max_tokens=self.max_tokens,
            stop_regex=r'</task_attempt>'
        )
        print(f"TaskAgent {self.id} reflection response: {reflect_response}")
        return reflect_response  # Return the reflection response

    def chain_of_thought(self):
        """Placeholder for chain of thought logic."""
        print("Executing chain of thought logic...")
        return "Chain of thought response"  # Placeholder return value

    def round(self):
        """Placeholder for round logic."""
        print("Executing round logic...")
        return "Round response"  # Placeholder return value

    def get_system_message(self):
        if self.custom_system_message:
            return self.custom_system_message
        return """
        You are a Task Agent. Your responsibilities include:
        - Performing specific tasks as directed by the Overseer Agent.
        - Engaging in two-way conversations to assist users.
        - Generating responses using the provided language model.
        """