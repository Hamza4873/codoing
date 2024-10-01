import re

text = "Some other text ‘Recipient’: [value, value,value]"
match = re.search(r"Recipient\s*:\s*\[([^\]]+)\]", text)

if match:
    print(match.group(1))  # Outputs: value, value,value