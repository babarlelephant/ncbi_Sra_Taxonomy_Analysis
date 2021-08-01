* python get_and_parse_taxons_and_create_requests.py

 (you may need: pip install requests)

* I will produce two files: request1.txt and request2.txt 

* With a free gmail account go into https://console.cloud.google.com/bigquery

run the request1 and click on save, as json on google drive, a box will appear saying it has been saved, click to view the result file and download it

run the request2 and click on save, as json on google drive, a box will appear saying it has been saved, click to view the result file and download it

* Download bioproject.xml the big (1.5GB in 2021) ncbi bioproject metadata xml file from https://ftp.ncbi.nlm.nih.gov/bioproject/

* change the 3 filenames at the beginning of parse_results.py

  and 
  
  python parse_results.py
  
  it will create RESULT.txt