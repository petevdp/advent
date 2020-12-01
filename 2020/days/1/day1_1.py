input_list = { int(s) for s in open('days/1/input').read().strip().split('\n') }


for n in input_list:
  if (2020 - n) in input_list:
    print('answer: ', (2020 - n) * n)
    break
