interaction_history = []

def update_memory(sender_id, receiver_id, message):
    interaction = {
        'from': sender_id,
        'to': receiver_id,
        'message': message
    }
    interaction_history.append(interaction)