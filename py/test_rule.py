import threading

from rule import execute as rule_exec


ff = {'height': 171, 'weight': 140.1}
fw = {'TunWei_167': 111, 'ShoulderWei_104':112, 'TS_sum': (111 + 112), 'WaistWei_155': 94}

f21 = {'JianKuan': 63, 'TouKuan':50}
f22 = {'height': 100, 'Head_Height':80}
f23 = {'Leg_Length': 10, 'top_half_Length':50}

rule_exec({**ff, **fw})

rule_exec(fw, 'figure-body')

rule_exec({**ff, **fw})

rule_exec(ff, 'figure-bmi')

rule_exec(f21, 'figure-part')
rule_exec(f22, 'figure-part')
rule_exec(f23, 'figure-part')
