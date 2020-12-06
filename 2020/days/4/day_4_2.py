import re
from functools import reduce

WHITESPACE = re.compile('\s')


def main():
    passports = []
    with open('days/4/input') as f:
        for entry in f.read().strip().split('\n\n'):
            fields = WHITESPACE.split(entry.strip())
            passport_pairs = {}
            for field in fields:
                key, value = field.split(':')
                passport_pairs[key] = value
            passports.append(passport_pairs)

    print(len([p for p in passports if validate_passport(p)]))


REQUIRED_FIELDS = set([
    'byr',  # (Birth Year)
    'iyr',  # (Issue Year)
    'eyr',  # (Expiration Year)
    'hgt',  # (Height)
    'hcl',  # (Hair Color)
    'ecl',  # (Eye Color)
    'pid',  # (Passport ID)
    # 'cid', # (Country ID)
])


def has_required_fields(passport):
    return all([k in passport.keys() for k in REQUIRED_FIELDS])


def validate_birth_year(passport):
    year = int(passport['byr'])
    return year >= 1920 and year <= 2002


def validate_issue_year(passport):
    year = int(passport['iyr'])
    return year >= 2010 and year <= 2020


def validate_expiration_year(passport):
    year = int(passport['eyr'])
    return year >= 2020 and year <= 2030


def validate_height(passport):
    height = int(passport['hgt'][0:-2])
    measure = passport['hgt'][-2:]
    if measure not in ['cm', 'in']:
        return False
    if measure == 'cm':
        return height >= 150 and height <= 193
    elif measure == 'in':
        return height >= 59 and height <= 76
    else:
        print('wut: ', passport['hgt'])

def validate_hair_color(passport):
    return bool(re.match('#[0-9a-f]{6}', passport['hcl']))

def validate_eye_color(passport):
    color = passport['ecl']
    return color in [
        'amb',
        'blu',
        'brn',
        'gry',
        'grn',
        'hzl',
        'oth',
    ]


def validate_passport_id(passport):
    print('pid: ', passport['pid'])
    out =  bool(re.match("^\d{9}$", passport['pid']))
    print('out: ', out)
    if not out:
        print('passport: ', passport)
    return out


VALIDATIONS = [
    has_required_fields, validate_birth_year, validate_issue_year,
    validate_expiration_year, validate_height, validate_hair_color, validate_eye_color,
    validate_passport_id
]


def validate_passport(passport):
    return all(validation(passport) for validation in VALIDATIONS)

if __name__ == '__main__':
    main()
