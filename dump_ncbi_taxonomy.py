# on a SRR, click on all Study ... all runs, to get there https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP429329&o=acc_s%3Aa where we can download metadata linking SRR and SAMN and a bit of metadata
# put this metadata in metadata.csv

import requests
import json
import os
f = open("metadata.csv")
r = f.readline()
r = f.readline()

# some SRR accessions to exclude, if run_taxonomy doesn't work for it
excl=[]

h = open("tax_analysis.txt","w")
while len(r) > 0:
	acc = r.split(",")[0]
	# some SRR accession
		
	if not os.path.exists("tax_"+acc+".json") and not acc in excl :
		print(acc,"run_taxonomy")
		req = requests.get("https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/run_taxonomy?acc="+acc+"&cluster_name=public")
		g = open("tax_"+acc+".json","wb")
		g.write(req.content)
		print(r)
		print(req.content[:100])
		print()
		req.close()
		g.close()
	
	if os.path.exists("tax_"+acc+".json"):
		print(acc,"write")
		g = open("tax_"+acc+".json","r")
		o = json.load(g)[0]
		g.close()
		h.write(r)
		h.write("  "+json.dumps(o["tax_totals"]))
		levels = {}
		for t in o["tax_table"]:
			if not "parent" in t or not t["parent"] in levels:
				levels.update({t["tax_id"]:"  "})
			else:
				levels.update({t["tax_id"]:" "+levels[t["parent"]]})
			h.write(levels[t["tax_id"]]+t["org"]+" "+str(t["total_count"])+"\n")
	r = f.readline()
			
