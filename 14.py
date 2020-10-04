#!/usr/bin/python
import math
import copy


# amoutn of source to get one output
def get_required(react, needed, count):
    if needed == "ORE":
        react[needed]['used'] += count
        return

    reactions = math.ceil((count-react[needed]['remains'])/react[needed]['produces'])
    react[needed]['remains'] += reactions*react[needed]['produces'] - count
    react[needed]['used'] += count

    for source, required in react[needed]['requires'].items():
        get_required(react, source, reactions*required)

    return react['ORE']['used']


react = {}
with open("input", "r") as f:
    for line in f:
        spl = line.split("=>")
        sources = {}
        for source in spl[0].strip().split(", "):
            sources[source.split()[1]] = int(source.split()[0])
        target = spl[1].strip().split()
        react[target[1]] = {'requires': sources,
                            'produces': int(target[0]),
                            'used': 0,
                            'remains': 0}

react['ORE'] = {'requires': [], 'produces': 0, 'remains': 0, 'used': 0}
fuel_ore = get_required(copy.deepcopy(react), "FUEL", 1)
print(fuel_ore)

ores = 1000000000000
required = 0
produces = ores/fuel_ore
fuels = ores/fuel_ore

while ores - required > 0:
    required = get_required(copy.deepcopy(react), "FUEL", fuels)
    fuels += (ores - required)/fuel_ore
    print(fuels)

