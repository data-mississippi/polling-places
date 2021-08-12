raw/PollingPlaceChanges.txt : raw/PollingPlaceChanges.pdf
	pdftotext $^ $@ -x 36 -y 96 -W 936 -H 516

raw/PollingPlaceChanges.pdf :
	curl -o $@ 'https://www.sos.ms.gov/content/documents/elections/PollingPlaceChanges.pdf'
