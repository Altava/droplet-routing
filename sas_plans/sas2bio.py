from ossaudiodev import openmixer
import pandas as pd
import os

parentname = os.path.dirname(__file__)
cgc_file = open(os.path.join(parentname, 'cgc_p9x9d5b3n001.1'), 'r')
bio_file = open(os.path.join(parentname, 'p9x9d5b3n001.bio'), 'r')
bio_raw = bio_file.read()
bio_file.close()
bio_out = open(os.path.join(parentname, 'cgc_p9x9d5b3n001.bio'), 'w')
bio_out.write(bio_raw)
bio_out.close()
cgc_data = pd.read_csv(cgc_file, sep='[ \-\_]', header=None, engine='python')
cgc_data = cgc_data.sort_values(5)
print(cgc_data)