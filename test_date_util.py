from dateutil import parser

DT = parser.parse("Jun 25 2024 07:31PM")

DT2 = parser.parse("Jun 24 2024 07:31PM")


print(DT)

if DT > DT2:
    print("Yes")
else:
    print("No")