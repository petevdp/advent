with open('days/10/input') as f:
    adapters = [int(n) for n in f.read().strip().split('\n')]
    
s_adapters = [0, *sorted(adapters)]
diff_1_count = 0
diff_3_count = 1
for i in range(0, len(s_adapters) - 1):
    curr_adapter = s_adapters[i]
    next_adapter = s_adapters[i + 1]
    
    diff = next_adapter - curr_adapter
    assert diff < 4
    if diff  == 1:
        diff_1_count += 1
    if diff == 3:
        diff_3_count += 1


print('diff 1: ', diff_1_count)
print('diff 3: ', diff_3_count)
print(diff_1_count * diff_3_count)

