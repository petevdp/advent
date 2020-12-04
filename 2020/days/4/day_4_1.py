import re

whitespace = re.compile('\s')

passports = []
with open('days/4/input') as f:
  for entry in f.read().split('\n\n'):
      fields = whitespace.split(entry.strip())
      passport_pairs = {}
      for field in fields:
          key, value = field.split(':')
          passport_pairs[key] = value
      passports.append(passport_pairs)



required_fields = set([
  'byr', # (Birth Year)
  'iyr', # (Issue Year)
  'eyr', # (Expiration Year)
  'hgt', # (Height)
  'hcl', # (Hair Color)
  'ecl', # (Eye Color)
  'pid', # (Passport ID)
  # 'cid', # (Country ID)
])


print(len([p for p in passports if all([k in p.keys() for k in required_fields])]))

# print(passports)
