def get_sid(boarding_pass):
    sid = 0
    for i, char in enumerate(boarding_pass[::-1]):
        if char in {'B', 'R'}:
            sid += 2**i
    return sid
    
with open('days/5/input') as f:
    passes = f.read().strip().split('\n')

max_sid = 0
for boarding_pass in passes:
    max_sid = max(get_sid(boarding_pass), max_sid)

print(max_sid)
