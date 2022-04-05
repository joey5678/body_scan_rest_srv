import collections

Person = collections.namedtuple('figure', 'name age gender')
from rule import execute as rule_exec


ff = {'height': 175,  'weight': 140.1,}
# fw = {'TunWei_167': 111, 'ShoulderWei_104':112, 'TS_sum': (111 + 112), 'WaistWei_155': 94}

# f21 = {'JianKuan': 63, 'TouKuan':50}
# f22 = {'height': 100, 'Head_Height':80}
# f23 = {'Leg_Length': 10, 'top_half_Length':50}

# rule_exec({**ff, **fw})



fx = {'height': 170,  'weight': 140.1, 'TunWei_167': 111, 'ShoulderWei_104':112, 'TS_sum': (111 + 112), 
    'WaistWei_155': 94, 'JianKuan': 63, 'TouKuan':50, 'LeftThigh_111': 89, 'RightThigh_112':91, 'Head_Height':80,
    'LeftArm_125': 34, 'LeftWrist_123': 22, 'RightArm_126':35, 'RightWrist_121': 23, 'Leg_Length': 10, 'top_half_Length':50,
    'top_leg_Length':10, 'Nip_Distance': 23, }

rule_exec(fx, 'figure-body')
rule_exec(fx, 'figure-bmi')

for i in range(6):
    print(f"\nfigure-part-2{i+1}\n")
    rule_exec(fx, f'figure-part-2{i+1}')

for i in range(8):
    print(f"\nfigure-detail-3{i+1}\n")
    rule_exec(fx, f'figure-detail-3{i+1}')



