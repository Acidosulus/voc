import re

s = """Ехал.

Грека!? Через реку... Видит грека - в реке рак? Сунул грека руку в реку. Рак его за руку - цап!

"""

for s in re.split(r'(?<=[.!?…]) ', s):
    print(s)