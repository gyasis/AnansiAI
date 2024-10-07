import guidance
import logging
from guidance import select  # Add this import at the top of the file

class Model:
    def __init__(self, model_type="chatgpt", model_path=None):
        # Store model_type and model_path as attributes
        self.model_type = model_type
        self.model_path = model_path

        # Map model types to their corresponding classes
        model_mapping = {
            "chatgpt": guidance.models.LiteLLMCompletion,
            # Add other models as needed
        }
        try:
            if model_type in model_mapping:
                # Initialize the model using the mapped class
                self.model = model_mapping[model_type](model_path, echo=False)
                logging.debug(f"Creating model of type '{model_type}' with path '{model_path}'")
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
        except Exception as e:
            logging.error(f"Error initializing model: {str(e)}")
            raise

    def generate(self, prompt, history=False, max_tokens=2000, stop=None, stop_regex=None):
        if history:
            prompt = history_variable + prompt
            lm = self.model + prompt + guidance.gen(max_tokens=max_tokens, name="response", stop=stop, stop_regex=stop_regex)
        else:
            lm = self.model + prompt + guidance.gen(max_tokens=max_tokens, name="response", stop=stop, stop_regex=stop_regex)
            
        return lm['response']

    def clone(self):
        logging.debug(f"Cloning model of type '{self.model_type}' with path '{self.model_path}'")
        return Model(model_type=self.model_type, model_path=self.model_path)

    def selection(self, prompt, options, custom_system_prompt=None):
        logging.info("Starting selection process")
        
        if not custom_system_prompt:
            logging.info("No custom system prompt provided")
            raise ValueError("A custom system prompt is required for selection.")
        
        logging.info(f"Custom system prompt: {custom_system_prompt}")
        logging.info(f"Prompt: {prompt}")
        logging.info(f"Options: {options}")
        
        # Initialize a new model for selection
        selection_model = []
        selection_model = Model(self.model_type, self.model_path)
        
        # Create the selection prompt
        selection_prompt = f"{custom_system_prompt} {prompt} my selection is:"
        
        # Generate the selection
        try:
            selection_result = selection_model.model + selection_prompt + select(options, name="selection")
            logging.info(f"Selection result: {selection_result['selection']}")
            return selection_result['selection']
        except Exception as e:
            logging.error(f"Error during selection: {str(e)}")
            raise
