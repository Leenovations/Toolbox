with open('Datalist.txt', 'w') as note01:
    with open('SampleSheet.txt', 'r') as samp:
        for line in samp:
            line = line.strip()
            splitted = line.split('\t')
            R_1 = splitted[1]
            R_2 = splitted[2]
            note01.write(R_1 + '\n' + R_2 + '\n')