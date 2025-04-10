import re

message_pattern = r"value(.+?)path(.*?)sender(.+?)$"


def is_valid_string_message(message):
    return bool(re.match(message_pattern, message))

def extract_message_parts(message):
    match = re.match(message_pattern, message)
    if match:
        return {
            "value": match.group(1),
            "path": match.group(2),
            "sender": match.group(3)
        }
    return None  # If not valid

def get_valid_messages_as_strings(messages):
    return [message for message in messages if is_valid_string_message(message)]

def process_nested_message_lists(nested_messages):
    valid_messages = []
    for messages in nested_messages:
        valid_messages.extend(get_valid_messages_as_strings(messages))
    return valid_messages

def extract_parts_from_nested_messages(nested_messages):
    extracted_parts = []
    for messages in nested_messages:
        for message in messages:
            if is_valid_string_message(message):
                extracted_parts.append(extract_message_parts(message))
    return extracted_parts

