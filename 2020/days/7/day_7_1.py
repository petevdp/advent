from collections import namedtuple


Rule = namedtuple('Rule', 'bag_name sub_bags')
SubBag = namedtuple('SubBag', 'num bag_name')

with open('days/7/input') as f:
# with open('days/7/example') as f:
    rules = f.read().strip().split('\n')
    
    
TARGET = 'shiny gold'


starting_name = []
parsed_rules = {}
for rule in rules:
    bag_type = ' '.join(rule.split(' ')[:2])
    # print(bag_type)
    # print('rule: ', rule)
    # print('no?: ', rule.split(' ')[4])
    if rule.split(' ')[4:6] == ['no', 'other']:
        parsed_rule = Rule(bag_type, [])
        if bag_type in parsed_rules:
            parsed_rules[bag_type].append(parsed_rule)
        else:
            parsed_rules[bag_type] = [parsed_rule]
    else:
        rest = rule.split(' ')[4:]
        sub_bags = ' '.join(rest)[:-1].split(', ')
        sub_bag_names = []
        parsed_sub_bags = []
        for bag in sub_bags:
            num = int(bag[0])
            name = ' '.join(bag.split(' ')[1:3])
            sub_bag_names.append(name)
            parsed_sub_bags.append(SubBag(num, name))
        
        parsed_rule = Rule(bag_type, parsed_sub_bags)
        if bag_type in parsed_rules:
            parsed_rules[bag_type].append(parsed_rule)
        else:
            parsed_rules[bag_type] = [parsed_rule]
    
        if TARGET in sub_bag_names:
            starting_name.append(bag_type)



names_to_check = [*starting_name]
bag_names = set()

for r in parsed_rules.values():
    print(r)
    
print()
print()

while len(names_to_check) > 0:
    print('names to check: ')
    print(names_to_check)
    print('bag names: ')
    print(bag_names)
    print('')
    curr_name = names_to_check.pop()
    bag_names.add(curr_name)
    for rule_list in parsed_rules.values():
        for rule in rule_list:
            if curr_name in [s.bag_name for s in rule.sub_bags]:
                names_to_check.append(rule.bag_name)
                break

print(bag_names)
print('answer: ', len(bag_names)) # remove one, first bag doesn't contain itself
