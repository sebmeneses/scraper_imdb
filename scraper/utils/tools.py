import re

def iso8601_to_minutes(duration_str):
    hours = minutes = 0
    if 'H' in duration_str:
        match = re.search(r'PT(\d+)H(\d+)?M?', duration_str)
        if match:
            hours = int(match.group(1))
            if match.group(2):
                minutes = int(match.group(2))
    elif 'M' in duration_str:
        match = re.search(r'PT(\d+)M', duration_str)
        if match:
            minutes = int(match.group(1))
    return hours * 60 + minutes
