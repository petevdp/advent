from collections import namedtuple


Rule = namedtuple('Rule', 'bag_name sub_bags')
SubBag = namedtuple('SubBag', 'num bag_name')

with open('days/7/input') as f:
# with open('days/7/example') as f:
    rules = f.read().strip().split('\n')
    
    
TARGET = 'shiny gold'


parsed_rules = {}
for rule in rules:
    bag_type = ' '.join(rule.split(' ')[:2])
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
    
    

names_to_check = [SubBag(1, TARGET)]
checked_bags = set()
num_sub_bags = 0
while len(names_to_check) > 0:
    curr_mult, curr_name = names_to_check.pop()
    rules_for_name = parsed_rules[curr_name]
    checked_bags.add(curr_name)
    for rule in rules_for_name:
        for sub_bag in rule.sub_bags:
            num_bags_to_add = sub_bag.num * curr_mult
            num_sub_bags += num_bags_to_add
            names_to_check.append(SubBag(num_bags_to_add, sub_bag.bag_name))

print(checked_bags)
print(num_sub_bags)


