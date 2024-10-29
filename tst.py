import json


def read_flags(flag=False):
    with open('memory_flags.json', 'r') as openfile:
        # if a flag as is specified return only that flag
        if flag:
            flags = json.load(openfile)
            return  flags[f'{flag}']
        
        # otherwise return all flags
        return json.load(openfile) 

def write_flag(flag):
    flags_json = read_flags()
    flags_json[f'{flag}'] = True

    with open("memory_flags.json", "w") as outfile:
        json.dump(flags_json, outfile)


write_flag('flag_night_1')
print(read_flags('flag_night_1'))