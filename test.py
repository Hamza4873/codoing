import json

def add_variable_blocks(data, topic, num_blocks):
    index = -1
    for i, block in enumerate(data["blocks"]):
        if "text" in block and "text" in block["text"] and block["text"]["text"] == f"*{topic}*":
            index = i
            break

    if index == -1:
        print(f"Error: Could not find topic '{topic}' in the JSON.")
        return

    variables = ["red", "blue", "green", "yellow", "grey"]
    for i in range(num_blocks):
        for j in range(len(variables)):
            new_block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{variables[j]}*"
                }
            }
            user_input = input(f"What do you want to put for {variables[j]} in block {i + 1}? ")
            new_block["text"]["text"] = f"*{variables[j]}*: {user_input}"
            data["blocks"].insert(index + 2 + (i * len(variables)) + j, new_block)

# Example usage
core = {
    "blocks": [
        {"type": "header", "text": {"type": "plain_text", "text": "Your Header Text"}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": "*Topic 1*"}},
        {"type": "divider"},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": "*Topic 2*"}},
        {"type": "divider"},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": "*Topic 3*"}},
        {"type": "divider"},
        {"type": "divider"}
    ]
}

topic1_blocks = int(input("How many blocks are in Topic 1? "))
add_variable_blocks(core, "Topic 1", topic1_blocks)

topic2_blocks = int(input("How many blocks are in Topic 2? "))
add_variable_blocks(core, "Topic 2", topic2_blocks)

topic3_blocks = int(input("How many blocks are in Topic 3? "))
add_variable_blocks(core, "Topic 3", topic3_blocks)

date = input("What date would you like to add to the header? ")
core["blocks"][0]["text"]["text"] = f"Your Header Text {date}"

# Print the modified JSON
print(json.dumps(core, indent=2))