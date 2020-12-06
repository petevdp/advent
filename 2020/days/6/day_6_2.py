import re

groups = []
with open('days/6/input') as f:
    for group in f.read().split('\n\n'):
        candidate_questions, *rest = [set(g) for g in group.strip().split('\n')]
        for person in rest:
            candidate_questions = candidate_questions & person
        groups.append(candidate_questions)
        
print(sum((len(g) for g in groups)))
