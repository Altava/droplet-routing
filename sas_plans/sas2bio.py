import pandas as pd
import os

parentname = os.path.dirname(__file__)
cgc_file = open(os.path.join(parentname, 'cgc_p9x9d5b3n001.1'), 'r')
bio_file = open(os.path.join(parentname, 'p9x9d5b3n001.bio'), 'r')
bio_raw = bio_file.read()
bio_file.close()
bio_out = open(os.path.join(parentname, 'cgc_p9x9d5b3n001.bio'), 'w')
bio_out.write(bio_raw)
bio_out.write("\n\n")
cgc_data = pd.read_csv(cgc_file, sep='[ \-\_]', header=None, names=["type", "x1", "y1", "x2", "y2", "droplet"], engine='python')
cgc_moves = cgc_data[cgc_data.loc[:, 'type'].str.contains("move")]
cgc_moves = cgc_moves.sort_values("droplet", kind='stable')

fluids = "fluids\n"
droplets = "droplets\n"
routes = "routes"

dropletcounter = 0
last_droplet = None
for index, row in cgc_moves.iterrows():
    if "move" in row[0]:
        current_droplet = row[5].replace(")", "")
        if current_droplet == last_droplet:
            routes += "(%s,%s) " % (row[3], row[4])
        else:
            last_droplet = current_droplet
            dropletcounter += 1
            fluids += "%i %s\n" % (dropletcounter, chr(ord('`') + dropletcounter))
            droplets += "%i %i\n" % (dropletcounter, dropletcounter)
            routes += "\n%i (%s,%s) (%s,%s) " % (dropletcounter, row[1], row[2], row[3], row[4])

fluids += "end\n\n"
droplets += "end\n\n"
routes += "\nend\n\n"

bio_out.write(routes)
bio_out.write(fluids)
bio_out.write(droplets)
bio_out.close()