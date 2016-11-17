import argparse
import os

parser = argparse.ArgumentParser(description = "Generate sponsor codes")
parser.add_argument("sponsor_file", type = str, help = "Csv file containing sponsors on new lines")
parser.add_argument("-n", "--namecol", default = 0, type = str, help = "Column of file containing well-formed (linux) sponsor names")
args = parser.parse_args()


f = open(args.sponsor_file,'r')
fout = open("sponsor_file_out.csv",'w')

for i,line in enumerate(f):
	line = line.strip().split(',')
	code = str((i * 13 + 6) % ((i+1)*100))
	disdir = line[0] + "-" + code
	print disdir
	
	if not os.path.exists(disdir):
		os.makedirs(disdir)
	print >> fout, ",".join(line + [disdir])

	
fout.close()
f.close()
