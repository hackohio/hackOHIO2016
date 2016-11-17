import argparse
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import glob, os

parser = argparse.ArgumentParser(description = "Generate sponsor pages")
parser.add_argument("sponsor_file", type = str, help = "Csv file containing sponsors and assigned page codes")
parser.add_argument("-n","--fullnamecol", type = int, default = 1, help = "Column of file containing sponsor full names")
parser.add_argument("-c","--codecol", type = int, default = 2, help = "Column of file containing sponsor directory codes")
parser.add_argument("-d","--coordcol", type = int, default = 3, help = "Column of file containing sponsor coordinator name")
parser.add_argument("coord_file", type = str, help = "Csv file containing names of coordinators")
args = parser.parse_args()

# parse coordinator file
coords = {}
cf = open(args.coord_file,'r')
for line in cf:
	line = line.strip().split(',')
	name = line[0]
	phone = line[1]
	email = line[2]
	
	coords[name]={'phone':phone,'email':email}



f = open(args.sponsor_file,'r')

for i,line in enumerate(f):
	line = line.strip().split(',')
	sponsor = line[args.fullnamecol]
	code = line[args.codecol]
	coordinator = line[args.coordcol]

	print code
	index_file = code+"/index.html"

	fout = open(index_file,'w')


	print code
	schedule = glob.glob(code+"/*Schedule*.pdf")
	if len(schedule) > 1:
		raise ImportError
	else:
		schedule = schedule[0]
		schedule = schedule[schedule.find('/')+1:]
		
	logistics = glob.glob(code+"/*Logistics*.pdf")
	if len(logistics) > 1:
		raise ImportError
	else:
		logistics = logistics[0]
		logistics = logistics[logistics.find('/')+1:]
		

	# html tag
	top = Element('html')
	comment = Comment('Sponsor page: ' + sponsor)
	top.append(comment)

	# Head tag
	head = SubElement(top,"head")
	
	# Head content
	
	# Title
	title = SubElement(head, 'title')
	title.text = sponsor

	# Add style sheets. Needt attributes as in; <link href="../dist/css/bootstrap.min.css" rel="stylesheet">
	d = {'href':'../../style/css/main.css','rel':'stylesheet'}
	link = SubElement(head, 'link',d)
	d = {'href':'../../style/bootstrap/bootstrap.min.css','rel':'stylesheet'}
	link = SubElement(head, 'link',d)

	# Body tag
	body = SubElement(top,'body')#,{'style':'background-image:url("../../images/layout/HackOHIO-logo-with-date.png");background-repeat:no-repeat;background-size:cover;'})
	
	# Body content
	
	# Page header design 
	divtop = SubElement(body,'div',{'id':'triangle-header'})
	
	# Main div in which all content will be placed
	div_main = SubElement(body,'div',{'class':'container'})	

	# div_main - In page title
	h1 = SubElement(div_main, 'h1',{'class':'j'})
	h1.text = sponsor + " HackOHI/O 2016 Sponsor Portal"
	
	# div_main - Page description
	p1 = SubElement(div_main, 'p')
	p1.text = "We are excited to have you on board for HackOHI/O 2016. Here is all of the information that you will need for event day."
	
	contact_div = SubElement(div_main,'div',{'class':'jumbotron'})
	cheader = SubElement(contact_div,'h2')
	cheader.text = "Your HackOHIO point of contact:"
	br = SubElement(contact_div,'br')
	cname = SubElement(contact_div,'p')
	cname.text = "Name: " + coordinator
	cnum = SubElement(contact_div,'p')
	cnum.text = "Phone: " + coords[coordinator]['phone']
	cemail = SubElement(contact_div,'p')
	cemail.text = "Email: " + coords[coordinator]['email']

	# div_main - first row div for pdf description
	div1 = SubElement(div_main,'div',{'class':'row'})

	# div1 - div to contain column 1 description
	col1 = SubElement(div1,'div',{'class':'col-md-6'})
	# col1 - column 1 description
	p = SubElement(col1,'p')
	# download link for perks pdf. Needs attributes as in:  <a href="http://example.com/files/myfile.pdf" target="_blank">Download</a>
	a = SubElement(p,'a',{'href':'test.pdf','target':'_blank'})
	a.text = "Schedule (pdf)"




	# div_main - second row div for embedded pdfs
	#div2 = SubElement(div_main,'div',{'class':'row'})
	
	# Create the attribute dict for embed tag as in: 
	# <embed src="http://example.com/the.pdf" width="500" height="375" type='application/pdf'>
	d = {'src':schedule,'width':'500','height':'500','type':'application/pdf'}
	# div2 - div to contain column 1 embedded pdf
	#col1 = SubElement(col1,'div',{'class':'col-md-6'})
	# Embed pdf
	embed_perks = SubElement(col1,'embed',d)
	
		# div1 - div to contain column 2 description
	col2 = SubElement(div1,'div', {'class':'col-md-6'})
	# col2 - column 2 description
	p = SubElement(col2,'p')
	# download link for schedule pdf
	a = SubElement(p,'a',{'href':'test.pdf','target':'_blank'})
	a.text = "Logistics (pdf)"

	# Create the attribute dict for embed tag
	d = {'src':logistics,'width':'500','height':'500','type':'application/pdf'}
	# div2 - div to contain column 1 embedded pdf
	#col2 = SubElement(div1,'div',{'class':'col-md-6'})
	# Embedded pdf
	embed_schedule = SubElement(col2,'embed',d)

	# padd the bottom of the page
	p_footer = SubElement(body,'p')
	br_footer = SubElement(body, 'br')

	#export to html file
	print >> fout, tostring(top, method="html")
	fout.close() 

f.close()
