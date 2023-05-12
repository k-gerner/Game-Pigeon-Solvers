def isValid(line, upper, lower):
	invalidChars = "1234567890-_=+!?/',.$#%*@"
	line = line.rstrip()
	if len(line) < lower or len(line) > upper:
		return False
	for char in invalidChars:
		if char in line:
			return False
	return True

infile = open("2of12.txt", "r")
outfile_name = input("Name of output file: ")
outfile = open(outfile_name, "w")
upperLim = input("Max number of letters? ")
lowerLim = input("Min number of letters? ")
for line in infile:
	if isValid(line, int(upperLim), int(lowerLim)):
		outfile.write(line)
print("Done.")




