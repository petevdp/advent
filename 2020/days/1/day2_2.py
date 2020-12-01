input_list = { int(s) for s in open('days/1/input').read().strip().split('\n') }


for m in input_list:
  sub_sum = 2020 - m
  for n in input_list:
    if (sub_sum - n) in input_list:
      print('answer: ', m * (sub_sum - n) * n)
      break
