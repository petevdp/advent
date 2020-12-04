inpt = [line.strip() for  line in open('days/2/input').readlines()]



def test_password(inpt_line):
  words = inpt_line.split(' ')
  index_1, index_2 = [int(c) - 1 for c in words[0].split('-')]
  char = words[1][0]
  password = words[-1]
  return (password[index_1] == char) ^ (password[index_2] == char)



answer = len([True for inpt_line in inpt if test_password(inpt_line)])

print(answer)
