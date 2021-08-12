from pyPdf import PdfFileWriter, PdfFileReader

infile = 'raw/PollingPlaceChanges.pdf'
outfile = ''

with open(infile, 'rb') as f:
    pdf = PdfFileReader(f)
    
    page_count = pdf.getNumPages()
