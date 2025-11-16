import os
import re

# Emoji replacements
replacements = {
    'START': 'START',
    'BRAIN': 'BRAIN',
    'FAST': 'FAST',
    'PREDICT': 'PREDICT',
    'ADAPT': 'ADAPT',
    'HEALTH': 'HEALTH',
    'SUCCESS': 'SUCCESS',
    'ERROR': 'ERROR',
    'DATA': 'DATA',
    'SEARCH': 'SEARCH',
    'VOICE': 'VOICE',
    'GROWTH': 'GROWTH',
    'STOP': 'STOP',
    'ALERT': 'ALERT',
    'TEST': 'TEST'
}

def replace_emojis_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for emoji, text in replacements.items():
        content = content.replace(emoji, text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Find all Python files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            replace_emojis_in_file(filepath)
            print(f"Processed {filepath}")

print("All emojis replaced!")