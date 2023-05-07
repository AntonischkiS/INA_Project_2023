import json


# mandate = abgeordneter in 1 legislatur period

def get_fraction_color(name):
    if name == 'SPD': return "red"
    if name == 'CDU' or name == 'CSU': return "black"
    if name == 'FDP': return "yellow"
    if name == 'Grüne': return "green"
    if name == 'AFD': return "blue"
    if name == 'Die Linke':
        return "magenta"
    # todo: color remaining factions
    else:
        return "grey"


def parse_json_mandates(json_file):
    data = json.load(json_file)  # change to loads for testing with string
    factions = {}
    mandates = []
    for faction in data['factions']:
        id = faction['id']
        name = faction['name']
        # print("Id: ", id, " name: ", name)
        # print("{} - {}".format(id, name))
        factions[id] = (name, get_fraction_color(name))
    for mandate in data['mandates']:
        id, name, f_id = mandate['id'], mandate['name'], mandate['faction_id']
        fr, c = factions[f_id]
        mandates.append((name, fr, id, c))
    return factions, mandates  # factions is not needed rn, perhaps we can use later


# TODO: add further info to node than just name, fraction?
# mandate should be a tuple of (name, fraction, mandate_id, color)
def write_mandates_as_nodes(file_name, mandates):
    file = open(file_name, "a")
    file.write("*vertices " + str(len(mandates)) + "\n")
    for index, mandate in enumerate(mandates):
        name, fraction, id, color = mandate
        file.write(
            str(index + 1) + " " + f"\"{name}\"" + f" \"{fraction}\" \" {id}\" \"{color}\" \n")  # further
        # info should be put before \n
    file.close()

# test = {"factions": [{"id": 234, "name": 'DIE LINKE'}, {"id": 345, "name": 'SPD'}, ],
#         "mandates": [{"id": 54325, "name": 'Peter Müller', "faction_id": 234},
#                      {"id": 53264, "name": 'Angela Angel', "faction_id": 345}, ]}
# test = str(test)
# js = json.dumps(test)
# f, m = parse_json_mandates(js)
# write_mandates_as_nodes(" test", m)
