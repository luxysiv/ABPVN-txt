import re

def sort_and_group_rules(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        rules = f.readlines()

    categorized_rules = {
        'block_rules': [],
        'hide_rules': [],
        'script_rules': [],
        'media_rules': [],
        'image_rules': [],
        'other_rules': []
    }

    for rule in rules:
        rule = rule.strip()
        if not rule or rule.startswith('!'):
            continue
        if rule.startswith('||'):
            categorized_rules['block_rules'].append(rule)
        elif '##' in rule:
            categorized_rules['hide_rules'].append(rule)
        elif '$script' in rule:
            categorized_rules['script_rules'].append(rule)
        elif '$media' in rule:
            categorized_rules['media_rules'].append(rule)
        elif '$image' in rule:
            categorized_rules['image_rules'].append(rule)
        else:
            categorized_rules['other_rules'].append(rule)

    for key in categorized_rules:
        categorized_rules[key].sort()

    with open(file_path, 'w', encoding='utf-8') as f:
        for category, rules in categorized_rules.items():
            if rules:
                f.write(f'! {category.upper()}\n')
                f.write('\n'.join(rules) + '\n\n')

file_path = 'adblock.txt'
sort_and_group_rules(file_path)
