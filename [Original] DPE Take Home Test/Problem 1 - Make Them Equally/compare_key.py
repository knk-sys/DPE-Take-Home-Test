def find_differences(source, target, parent_key=[]):
    actions = []
    source_keys = list(source.keys())
    target_keys = list(target.keys())

    i = 0
    for key in target_keys:
        if i < len(source_keys):
            current_source_key = source_keys[i]
        else:
            current_source_key = None

        if key in source:
            source_value = source[key]
            target_value = target[key]

            if isinstance(source_value, dict) and isinstance(target_value, dict):
                actions.extend(find_differences(source_value, target_value, parent_key + [key]))
            elif source_value != target_value:
                actions.append({
                    "operation": "modify_value",
                    "value": target_value,
                    "parent_key": parent_key,
                    "after_key": current_source_key if current_source_key != key else None
                })
            i += 1
        else:
            actions.append({
                "operation": "add_new_key",
                "value": target[key],
                "parent_key": parent_key,
                "after_key": current_source_key if i > 0 else None
            })
            i += 1

    return actions


# Source JSON
source = {
    "event": {
        "name": "Global Music Festival",
        "location": {
            "city": "Tokyo",
            "country": "Hokkaido"
        },
        "performances": {
            "headliner": {
                "artist": "Imagine Dragons",
                "genre": "Rock"
            },
            "supporting": {
                "first": {
                    "artist": "Twice",
                    "genre": "K-Pop"
                },
                "second": {
                    "genre": "Indie Rock"
                }
            }
        }
    }
}

# Target JSON
target = {
    "event": {
        "name": "Global Music Festival",
        "date": "2024-08-10",
        "location": {
            "city": "Tokyo",
            "country": "Japan",
            "venue": {
                "name": "Tokyo Dome",
                "capacity": 55000
            }
        },
        "performances": {
            "headliner": {
                "artist": "Imagine Dragons",
                "genre": "Rock"
            },
            "supporting": {
                "first": {
                    "artist": "Twice",
                    "genre": "K-Pop"
                },
                "second": {
                    "artist": "Alt-J",
                    "genre": "Indie Rock"
                }
            }
        }
    }
}

# Find differences between Source and Target
actions = find_differences(source, target)

# Output the actions
import json
print(json.dumps(actions, indent=2))
