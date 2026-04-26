def trim_conversation(messages, max_messages=5):
    """
    Keep last N messages (STM)
    """
    if len(messages) > max_messages:
        print(messages)
        return messages[-max_messages:]
    return messages
