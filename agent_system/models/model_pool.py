from ._model_ import Model

class ModelPool:
    def __init__(self):
        self.models = {}

    def add_model(self, model_name, model_type, model_path):
        print(f"Adding model: {model_name}")
        print(f"Model type: {model_type}")
        print(f"Model path: {model_path}")
        try:
            model = Model(model_type, model_path)
            self.models[model_name] = model
            print(f"Model '{model_name}' successfully created and added to the pool.")
        except Exception as e:
            print(f"Error creating model '{model_name}': {str(e)}")

    def get_model(self, model_name):
        return self.models.get(model_name)

    def list_models(self):
        return list(self.models.keys())