import re

def sort_and_group_rules(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        rules = list(set(line.strip() for line in f if line.strip()))

    categorized_rules = {
        'block_rules': set(),
        'hide_rules': set(),
        'script_rules': set(),
        'media_rules': set(),
        'image_rules': set(),
        'other_rules': set()
    }

    for rule in rules:
        if rule.startswith('!'):
            continue
        if rule.startswith('||'):
            categorized_rules['block_rules'].add(rule)
        elif '##' in rule:
            categorized_rules['hide_rules'].add(rule)
        elif '$script' in rule.lower():
            categorized_rules['script_rules'].add(rule)
        elif '$media' in rule.lower():
            categorized_rules['media_rules'].add(rule)
        elif '$image' in rule.lower():
            categorized_rules['image_rules'].add(rule)
        else:
            categorized_rules['other_rules'].add(rule)

    for key in categorized_rules:
        categorized_rules[key] = sorted(categorized_rules[key])

    with open(file_path, 'w', encoding='utf-8') as f:
        for category, rules in categorized_rules.items():
            if rules:
                f.write(f'! {category.upper()}\n')
                f.write('\n'.join(rules) + '\n\n')

file_path = 'adblock.txt'
sort_and_group_rules(file_path)
