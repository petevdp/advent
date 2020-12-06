def get_sid(boarding_pass):
    sid = 0
    for i, char in enumerate(boarding_pass[::-1]):
        if char in {'B', 'R'}:
            sid += 2**i
    return sid

with open('days/5/input') as f:
    passes = f.read().strip().split('\n')

max_sid = 2**10 - 2**8
min_sid = 2**7

all_sids = [sid for sid in range(min_sid, max_sid)]
present_sids = {*map(get_sid, passes)}
for sid in all_sids:
    if sid not in present_sids:
        print(sid)
        break
