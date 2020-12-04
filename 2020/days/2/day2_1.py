inpt = [line.strip() for  line in open('days/2/input').readlines()]



def test_password(inpt_line):
  words = inpt_line.split(' ')
  min_chars, max_chars = [int(c) for c in words[0].split('-')]
  char = words[1][0]
  password = words[-1]
  num_of_char = len([c for c in password if c == char])
  return num_of_char <= max_chars and num_of_char >= min_chars



answer = len([True for inpt_line in inpt if test_password(inpt_line)])

print(answer)
