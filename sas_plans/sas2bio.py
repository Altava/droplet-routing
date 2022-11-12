import pandas as pd
import os
import re
from pathlib import Path

def getNum(str):
    return int(re.findall("\d+", str)[0])

home = Path("/home/altava/droplet-routing")
parentname = os.path.dirname(__file__)
cgc_file = open(os.path.join(parentname, 'extensions_data/00014/sas_plan.1'), 'r')
bio_file = open(os.path.join(home, 'benchmarks/PCR.bio'), 'r')
bio_raw = bio_file.read()
bio_file.close()
bio_out = open(os.path.join(parentname, 'PCR.bio'), 'w')
bio_out.write(bio_raw)
bio_out.write("\n\n")
cgc_data = pd.read_csv(cgc_file, sep='[ \-\_]', header=None, names=["type1", "type2", "p1", "p2", "p3", "p4", "p5", "p6", "p7"], engine='python')
# cgc_moves = cgc_data[cgc_data.loc[:, 'type'].str.contains("move")]
# cgc_moves = cgc_moves.sort_values("droplet", kind='stable')

droplets = "droplets\n"
routes = []
fluids = {
    "hcl": 11,
    "kcl": 12,
    "BovineSerum": 13,
    "bovine": 13,
    "Gelatin": 14,
    "gelatin": 14,
    "Primer": 15,
    "primer": 15,
    "Beosynucleotide": 16,
    "beosynucleotide": 16,
    "AmpliTag": 17,
    "amplitag": 17,
    "LamdaDNA": 18,
    "lamdadna": 18,
    "firstmix1": 1,
    "firstmix2": 2,
    "firstmix3": 3,
    "firstmix4": 4,
    "secondmix1": 5,
    "secondmix2": 6,
    "finalmix": 7
}
spawns = {
    "hcl": "(1,7)",
    "kcl": "(2,8)",
    "BovineSerum": "(7,8)",
    "bovine": "(7,8)",
    "Gelatin": "(8,7)",
    "gelatin": "(8,7)",
    "Primer": "(1,2)",
    "primer": "(1,2)",
    "Beosynucleotide": "(2,1)",
    "beosynucleotide": "(2,1)",
    "AmpliTag": "(7,1)",
    "amplitag": "(7,1)",
    "LamdaDNA": "(8,2)",
    "lamdadna": "(8,2)"
}
positions = {}

counter = 1
dropletcounter = 0
last_droplet = None
for index, row in cgc_data.iterrows():
    if "spawn" in row[0]:
        fluidtype = row[1]
        fluidnumber = fluids.get(fluidtype)
        dropletcounter += 1
        targetPosition = spawns.get(fluidtype)
        droplets += "%i %i\n"% (dropletcounter, fluidnumber)
        routes.append("%i [%i] %s" % (dropletcounter, counter, targetPosition))
        positions.update({targetPosition: dropletcounter})
        counter += 1
    if "merge" in row[0]:
        if "x" in row[1]:
            xt = getNum(row[7])
            x1 = getNum(row[5])
            x2 = getNum(row[6])
            yt = getNum(row[8])
            y1 = yt
            y2 = yt
        if "y" in row[1]:
            xt = getNum(row[5])
            x1 = xt
            x2 = xt
            yt = getNum(row[8])
            y1 = getNum(row[6])
            y2 = getNum(row[7])
        targetPosition = "(%i,%i)" % (xt, yt)
        p1 = "(%i,%i)" % (x1, y1)
        p2 = "(%i,%i)" % (x2, y2)
        fluidtype = row[4]
        fluidnumber = fluids.get(fluidtype)
        dropletcounter += 1
        droplets += "%i %i\n"% (dropletcounter, fluidnumber)
        routes.append("%i [%i] %s" % (dropletcounter, counter, targetPosition))
        positions.update({targetPosition: dropletcounter})
        positions.pop(p1)
        positions.pop(p2)
        counter += 1
    if "move" in row[0]:
        fluidtype = row[2]
        if "north" in row[1] or "south" in row[1]:
            xo = getNum(row[3])
            yo = getNum(row[4])
            xt = xo
            yt = getNum(row[5])
        if "west" in row[1] or "east" in row[1]:
            xo = getNum(row[3])
            yo = getNum(row[5])
            xt = getNum(row[4])
            yt = yo
        originPosition = "(%i,%i)" % (xo, yo)
        targetPosition = "(%i,%i)" % (xt, yt)
        fluidnumber = positions.pop(originPosition)
        positions.update({targetPosition: fluidnumber})
        routes[fluidnumber - 1] += " " + targetPosition
        counter += 1
    if "split" in row[0]:
        fluidtype = row[2]
        fluidnumber = fluids.get(fluidtype)
        if "x" in row[1]:
            xo = getNum(row[3])
            x1 = getNum(row[4])
            x2 = getNum(row[5])
            yo = getNum(row[6])
            y1 = yo
            y2 = yo
        if "y" in row[1]:
            xo = getNum(row[3])
            x1 = xo
            x2 = xo
            yo = getNum(row[4])
            y1 = getNum(row[5])
            y2 = getNum(row[6])
        originPosition = "(%i,%i)" % (xo, yo)
        targetPosition = "(%i,%i)" % (x1, y1)
        p2 = "(%i,%i)" % (x2, y2)
        dropletnumber = positions.pop(originPosition)
        positions.update({targetPosition: dropletnumber})
        dropletcounter += 1
        positions.update({p2: dropletcounter})
        routes[dropletnumber - 1] += " " + targetPosition
        routes.append("%i [%i] %s" % (dropletcounter, counter, p2))
        droplets += "%i %i\n"% (dropletcounter, fluidnumber)
        counter += 1
    
    for pos in positions:
        if pos != targetPosition:
            routes[positions.get(pos) - 1] += " " + pos

routesString = "routes\n"
for r in routes:
    routesString += r + "\n"
            
    # if "move" in row[0]:
    #     current_droplet = row[5].replace(")", "")
    #     if current_droplet == last_droplet:
    #         routes += "(%s,%s) " % (row[3], row[4])
    #     else:
    #         last_droplet = current_droplet
    #         dropletcounter += 1
    #         fluids += "%i %s\n" % (dropletcounter, chr(ord('`') + dropletcounter))
    #         droplets += "%i %i\n" % (dropletcounter, dropletcounter)
    #         routes += "\n%i (%s,%s) (%s,%s) " % (dropletcounter, row[1], row[2], row[3], row[4])

droplets += "end\n\n"
routesString += "\nend\n\n"

bio_out.write(routesString)
bio_out.write(droplets)
bio_out.close()