from .memory import update_memory

class MessagePool:
    def __init__(self):
        self.messages = []

    def add_message(self, message, sender_id):
        self.messages.append((message, sender_id))

    def dispatch_messages(self, overseer):
        while self.messages:
            message, sender_id = self.messages.pop(0)
            overseer.receive_message(message)
            update_memory(sender_id, overseer.id, message)