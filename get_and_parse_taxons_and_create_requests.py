
import requests
import io

# for Coronaviridae
r = requests.get('https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=11118&lvl=30')
# You can try replacing Coronaviridae by for example Filoviridae
# In the xml requests I am avoiding the SRA whose organism is a certain species (SARS-CoV-2) you may need to change it


res = r.text

f = io.StringIO(res)# open("cov_taxons.txt","r")
r = f.readline()
while len(r)>0:
	if "<STRONG>Coronaviridae</STRONG>" in r:
		break
	r = f.readline()
	
taxons = []
tab = []
while len(r)>0:
	if "<UL " in r:
		tab.append(" ")
	if "</UL>" in r:
		if len(tab)==0:
			break
		tab.pop()
	if "<LI " in r:
		t = r.split("<STRONG>")[1].split("</STRONG>")[0]
		taxons.append([t,"".join(tab)])
	r = f.readline()

f = open("cov_taxons_parsed.txt","w")
for j in taxons:
	f.write(j[1]+"$"+j[0]+"\n")
f.close()


f = open("request1.txt","w")
f.write('SELECT acc,bioproject,releasedate,assay_type,center_name FROM `nih-sra-datastore.sra.metadata` WHERE organism <> "Severe acute respiratory syndrome coronavirus 2" AND acc IN (SELECT acc FROM `nih-sra-datastore.sra_tax_analysis_tool.tax_analysis` WHERE name= "Coronaviridae")\n\n')
f.close()

f = open("request2.txt","w")
f.write('SELECT * FROM `nih-sra-datastore.sra_tax_analysis_tool.tax_analysis` WHERE  acc IN (SELECT acc FROM `nih-sra-datastore.sra.metadata` WHERE organism <> "Severe acute respiratory syndrome coronavirus 2" AND acc IN (SELECT acc FROM `nih-sra-datastore.sra_tax_analysis_tool.tax_analysis` WHERE name= "Coronaviridae")) AND name IN (\n')
c = 0
for j in taxons:
	if c == 1:
		f.write(",")
	f.write("'"+j[0]+"'")
	c = 1
f.write(")")
f.close()