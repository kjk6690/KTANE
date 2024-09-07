import csv 
suspects = "Sc,Pl,Pe,Gr,Mu,Wh".split(",")
weapons = "Ca,Da,Pi,Re,Ro,Sp".split(",")



def get_possible_matches(table, s_idx, w_idx):
    ret = [(s_idx, w_idx)]
    s_set = set(table[s_idx])
    w_set = set(table[w_idx])
    rooms = s_set.intersection(w_set)
    for room in rooms:
        suspect = suspects[table[s_idx].index(room)]
        weapon  = weapons[table[w_idx].index(room)]
        ret.append((suspect, weapon, room))
    return ret

def create_murder_easy_lookup(table):
    ret = []
    for s_idx in range(len(table)):
        for w_idx in range(len(table)):
            ret.append(get_possible_matches(table, s_idx, w_idx))
    return ret

  
if __name__ == "__main__":
    with open('murder_rooms.csv', 'r') as read_obj: 
        csv_reader = csv.reader(read_obj) 
        table = list(csv_reader)
    matches = create_murder_easy_lookup(table)
    for line in matches:
        print(line)

    with open('out.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(matches)