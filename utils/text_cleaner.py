import re

def clean_code(lines):
    cleaned_lines = []

    for line in lines:
        # ✅ Keep quotes, commas, dots, etc.
        line = re.sub(r'[^a-zA-Z0-9_()=:+\-*/\[\]\'\"., ]', '', line)

        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return cleaned_lines