import json


# mandate = abgeordneter in 1 legislatur periode

def get_fraction_color(name):
    if name == 'SPD': return "red"
    if name == 'CDU': return "black"
    if name == 'FDP': return "yellow"
    if name == 'Die Linke':
        return "magenta"
    else:
        return "pink"


def parse_json_mandates(json_file):
    data = json.loads(json_file)
    factions = {}
    mandates = []
    for id, name in data['factions']:
        print("{} - {}".format(id, name))
        factions[id] = (name, get_fraction_color(name))
    print("factions", factions)
    for id, name, f_id in data['mandates']:
        print("fid", f_id)
        fr, c = factions[f_id]
        mandates.append((name, fr, id, c))
    return factions, mandates


# TODO: add further info to node than just name, fraction?
# mandate should be a tuple of (name, fraction, mandate_id, color)
def write_mandates_as_nodes(file_name, mandates):
    file = open(file_name, "a")
    file.write("*vertices" + str(len(mandates)))
    for index, name, fraction, id, color in enumerate(mandates):
        file.write(
            str(index) + " " + f"\"{name}\" " + f"\"{fraction}\"" + f"\" {id}\"" + f"\" {color}\"" + "\n")  # further info should be put before \n
    file.close()


test = {"factions": [{"id": 234, "name": 'DIE LINKE'}, {"id": 345, "name": 'SPD'}, ],
        "mandates": [{"id": 54325, "name": 'Peter Müller', "faction_id": 234},
                     {"id": 53264, "name": 'Angela Angel', "faction_id": 345}, ]}
# test = str(test)
js = json.dumps(test)
# print(js)
f, m = parse_json_mandates(js)
write_mandates_as_nodes(" test", m)
