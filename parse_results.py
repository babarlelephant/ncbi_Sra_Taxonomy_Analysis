request1resultName = "acc_to_bioproject_and_date_bq-results-20210801-203436-f8ioshrwj1uc.json"
request2resultName = "tax_bq-results-20210801-201603-sq60z8rji1f5.json"
bigNCBIbioprojectMetadataXmlFile = "bioproject.xml"




#bigNCBIbioprojectMetadataXmlFile =  "C:\\Downloads\\bioproject.xml.bin"

import json




f = open("cov_taxons_parsed.txt","r")
r = f.readline()
TAX = []
while len(r)>0:
	t = r.split("\n")[0].split("$")
	t[0]="\t"+t[0].replace(" ","\t")
	TAX.append(t)
	r = f.readline()
f.close()

Acc_To_Bioproject=dict()
BioprojectList=dict()
f = open(request1resultName,"r",encoding="utf-8")
r = f.readline()
while len(r)>0:
	o = json.loads(r)
	if not "bioproject" in o:
		o.update({"bioproject":"NA"})
	if not "center_name" in o:
		o.update({"center_name":""})
	if not "assay_type" in o:
		o.update({"assay_type":""})
	Acc_To_Bioproject.update({o["acc"]:[o["bioproject"],o["releasedate"].split(" ")[0],o["assay_type"],o["center_name"]]})
	BioprojectList.update({o["bioproject"]:1})
	r = f.readline()
f.close()

if 1:
	def prXML(r,o,isProjectDescr=0):
		if r.tag == "ProjectDescr":
			isProjectDescr = 1
		if isProjectDescr == 1 and r.tag == "Name" and not r.tag in o:
			o.update({r.tag:r.text.replace("\r","").replace("\n"," ")})
		if isProjectDescr == 1 and r.tag == "Title"  and not r.tag in o:
			o.update({r.tag:r.text.replace("\r","").replace("\n"," ")})
		if isProjectDescr == 1 and r.tag == "Description"  and not r.tag in o:
			o.update({r.tag:r.text.replace("\r","").replace("\n"," ")})
		if r.tag == "OrganismName" and not r.tag in o:
			o.update({r.tag:r.text})
		if r.tag == "ProjectReleaseDate" and not r.tag in o:
			d = r.text.split(":")[0].split("T")[0]
			o.update({"ProjectReleaseDate":d})
		#print("".join(tab),"<",r.tag,r.attrib,r.text,">")
		for child in r:
			prXML(child,o,isProjectDescr)
		

	import xml.etree.ElementTree as ET

	f = open(bigNCBIbioprojectMetadataXmlFile,"r",encoding="utf-8")
	r = f.readline()

	C = 0
	while len(r)>0:
		if r.startswith("    <Project>"):
			s = []
			while not r.startswith("        <ArchiveID "):	
				s.append(r)
				if r.startswith("    </Project>"):
					print("bug")
					quit()
				r = f.readline()
			acc = r.split('accession=\"')[1].split('"')[0]
			C+=1
			if C%1000 == 0 and 0:
				print(acc)
			if not acc in BioprojectList:
				s = []
				while not r.startswith("    </Project>"):
					r = f.readline()
			else:
				while not r.startswith("    </Project>"):
					s.append(r)
					r = f.readline()
				s.append(r)
				
				root = ET.fromstring("".join(s))
				o = {}
				prXML(root,o)
				BioprojectList.update({acc:o})
				if not "ProjectReleaseDate" in o:
					h = open("lala.txt","w")
					h.write("".join(s))
					h.close()
					h = open("lala2.txt","w")
					h.write(json.dumps(o))
					h.close()
					quit()
		r = f.readline()

	f.close()

	f = open("BioprojectList.txt","w",encoding="utf-8")
	f.write(json.dumps(BioprojectList))
	f.close()

f=open("BioprojectList.txt","r",encoding="utf-8")
BioprojectList = json.load(f)
f.close()

f = open(request2resultName,"r")

r = f.readline()

ACC = dict()
while len(r)>0:
	o = json.loads(r)
	acc = o["acc"]
	tax = o["name"]
	count = o["total_count"]
	r = f.readline()
	if not acc in ACC:
		ACC[acc]={}
	ACC[acc].update({tax:count})
	
g = open("RESULT.txt","w",encoding="utf-8")
for a in ACC:
	g.write("$ "+a+"\t"+Acc_To_Bioproject[a][1]+"\t"+Acc_To_Bioproject[a][2]+"\t"+Acc_To_Bioproject[a][3]+"\n")
	metadata = None
	if not a in Acc_To_Bioproject:
		print(a,"not in Acc_To_Bioproject")
	else:
		b = Acc_To_Bioproject[a][0]
		if BioprojectList[b] == 1:
			#print(a,b,"not bioprojects metadata")
			lll=0
		else:
			metadata = BioprojectList[b]
	if not metadata == None:
		for m in metadata:
			g.write("       "+m+":"+metadata[m].replace("\n"," ")+"\n")
	o = ACC[a]
	for t in TAX:
		if t[1] in o:
			g.write(t[0]+t[1]+"\t"+o[t[1]]+"\n")
	#g.write(j+" "+json.dumps(ACC[j])+"\n")