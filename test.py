import re
s = 'as possible as'
print('1: ', re.findall(r'as\s(\w+)\s(\w+)', s))
print('2: ', re.findall(r'as\s([\w+])\s([\w+])', s))


class A:
    def __call__(self, *args, **kwargs):
        return 0

print(A()())