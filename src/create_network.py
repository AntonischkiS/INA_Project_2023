import json
from collections import defaultdict
import os
import sys
from tqdm import tqdm
import utils

# mandate = abgeordneter in 1 legislatur period

def get_fraction_color(name):
    if name == 'SPD': return "red"
    if name == 'CDU/CSU': return "black"
    if name == 'FDP': return "yellow"
    if name in ['BÜNDNIS 90/DIE GRÜNEN', 'DIE GRÜNEN', 'Greens']: return "green"
    if name == 'AfD': return "blue"
    if name == 'DIE LINKE.' or name == 'DIE LINKE' or 'Left' in name:
        return "magenta"
    # todo: color remaining fractions
    else:
        return "grey"


def parse_json_mandates(json_file):
    with open(json_file) as f:
        data = json.load(f)  # change to loads for testing with string
    factions = {}
    mandates = []
    for faction in data['fractions']:
        id = faction['id']
        name = faction['name']
        # print("Id: ", id, " name: ", name)
        # print("{} - {}".format(id, name))
        factions[id] = (name, get_fraction_color(name))
    for mandate in data['mandates']:
        id, name, f_id = mandate['id'], mandate['name'], mandate['fraction_id']
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
            str(index + 1) + " " + f"\"{name}\"" + f" \"{fraction}\" \"{id}\" \"{color}\" \n")  # further
        # info should be put before \n
    file.close()

# test = {"factions": [{"id": 234, "name": 'DIE LINKE'}, {"id": 345, "name": 'SPD'}, ],
#         "mandates": [{"id": 54325, "name": 'Peter Müller', "faction_id": 234},
#                      {"id": 53264, "name": 'Angela Angel', "faction_id": 345}, ]}
# test = str(test)
# js = json.dumps(test)
# f, m = parse_json_mandates(js)
# write_mandates_as_nodes(" test", m)


def generate_edges(path, mandate_ids):
    """
    generates a list of edges between mandate ids with a weight
    input: 
    path: to legislature period
    mandate_ids: list of mandate ids
    output:
    list of tuples of the form (id, id, weight)
    """
    VOTE_OPTIONS = ['yes', 'no', 'abstain', 'no_show'] 
    SV = {id: defaultdict(int) for id in mandate_ids}  # Same Votes count
    poll_file_names = list(filter(lambda p: p.startswith('poll'), os.listdir(path)))
    #error_cnt=set()
    for pfname in tqdm(poll_file_names):
        with open(path+'/'+pfname) as f:
            pdata = json.load(f)
        # go through poll data and create a list for each vote option
        # that holds all mandate ids that voted this way
        VC = {vo: [] for vo in VOTE_OPTIONS}  # vote clusters
        for vote in pdata['votes']:
            VC[vote['vote']].append(vote['mandate_id'])


        # do +1 in SV for each pair of mandate ids within each of the lists
        for voters in VC.values():
            #print(voters)
            lnv = len(voters)
            for i in range(lnv):
                vo1 = voters[i] 
                if vo1 not in mandate_ids: #this excludes everybody who left during a legislature period
                    #error_cnt.add(vo1)
                    continue
                for j in range(i+1, lnv):
                    vo2 = voters[j]
                    if vo2 not in mandate_ids:
                        #error_cnt.add(vo2)
                        continue
                    #assert vo1 in mandate_ids
                    SV[vo1][vo2] += 1
                    SV[vo2][vo1] += 1
                  
    #print(len(error_cnt))
    E = set()
    n_polls = len(poll_file_names)
    for midx, row in SV.items():
        for midy, cnt in row.items():
            if cnt == 0:
                continue
            E.add((min(midx, midy), max(midx, midy), round(cnt / n_polls, 3)))
    return list(E)


def generate_edges2(path, mandate_ids):
    """
    generates a list of edges between mandate ids with a weight
    input:
    path: to legislature period
    mandate_ids: list of mandate ids
    output:
    list of tuples of the form (id, id, weight)
    """
    VOTE_OPTIONS = ['yes', 'no', 'abstain']
    SV = {id: defaultdict(int) for id in mandate_ids}  # Same Votes count
    AC = {id: defaultdict(int) for id in mandate_ids}  # Attendance count
    poll_file_names = list(filter(lambda p: p.startswith('poll'), os.listdir(path)))
    # error_cnt=set()
    for pfname in tqdm(poll_file_names):
        with open(path + '/' + pfname) as f:
            pdata = json.load(f)
        # go through poll data and create a list for each vote option
        # that holds all mandate ids that voted this way
        VC = {vo: [] for vo in VOTE_OPTIONS}  # vote clusters
        AV = [] #mandateids that attended vote
        for vote in pdata['votes']:
            if (not vote['vote'] == 'no_show') and ( vote['mandate_id'] in mandate_ids) :
                VC[vote['vote']].append(vote['mandate_id'])
                AV.append(vote['mandate_id'])


        for vo1 in AV:
            for vo2 in AV:
                AC[vo1][vo2] += 1
                # AC[vo2][vo1] += 1

        # do +1 in SV for each pair of mandate ids within each of the lists
        for voters in VC.values():
            # print(voters)
            lnv = len(voters)
            for i in range(lnv):
                vo1 = voters[i]

                for j in range(i + 1, lnv):
                    vo2 = voters[j]

                    # assert vo1 in mandate_ids
                    SV[vo1][vo2] += 1
                    SV[vo2][vo1] += 1

    # print(len(error_cnt))
    E = set()
    n_polls = len(poll_file_names)
    for midx, row in SV.items():
        for midy, cnt in row.items():
            if cnt == 0:
                continue
            E.add((min(midx, midy), max(midx, midy), round(cnt / AC[midy][midx], 3)))
    return list(E)


def create_graph_file_from_legislature_data(leg_year, src_path, dst_path):
    """
    
    input: 
    path: path to a legislature period
    ourput: None
    """
    leg_period = utils.year_to_period(leg_year)
    leg_src_path = src_path + leg_period + '/'
    leg_dst_path = dst_path + leg_period + '/'
    os.makedirs(leg_dst_path, exist_ok=True)

    # nodes generieren
    factions, mandates = parse_json_mandates(leg_src_path+"mandates.json")
    # edges generieren
    print('generating edges')
    #changed to generating edges 2
    e_list = generate_edges2(leg_src_path,list(map(lambda x: x[2], mandates)))
    print('edges generated')
    # graph file erstellen
    file = open(leg_dst_path + f"network{leg_period}.net", "w")
    # nodes reinschreiben
    file.write("*vertices " + str(len(mandates)) + "\n")
    MI_LOOKUP = dict()
    for index, mandate in enumerate(mandates):
        name, fraction, id, color = mandate
        MI_LOOKUP[id] = index
        file.write(
            str(index + 1) + " " + f"\"{name}\"" + f" \"{fraction}\" \"{id}\" \"{color}\" \n")  # further
        # info should be put before \n
    # edges reinschreiben
    file.write("*edges " + str(len(e_list)) + "\n")
    for midx, midy, weight in e_list:
        ix, iy  = MI_LOOKUP[midx], MI_LOOKUP[midy]
        file.write(
            str(ix +1) + " " + str(iy +1) + " " + str(weight)+ "\n") 
    file.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("must specify election year")
        exit()
    if sys.argv[1] not in utils.YEAR_TO_LEG_ID:
        print("invalid election year")
        exit()
    leg_year = sys.argv[1]
    create_graph_file_from_legislature_data(leg_year, utils.BUNDESTAG_DATA_PATH, utils.BUNDESTAG_GRAPH_PATH)
    #generate_edges("../abgeordnetenwatch/data/Bundestag/2021-2025", [1,2,3])
