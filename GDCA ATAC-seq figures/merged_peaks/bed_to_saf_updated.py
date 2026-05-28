with open('All_Samples.fwp.filter.non_overlapping.bed', 'r') as infile:
    with open('All_Samples.fwp.filter.non_overlapping.saf', 'w') as outfile:
        header = ['GeneID', 'Chr', 'Start', 'End', 'Strand']
        outfile.write('\t'.join(header) + '\n')
        for line in infile:
            line = line.rstrip('\n').split('\t')
            new_line = [line[3], line[0], str(int(line[1])+1), line[2], line[5]]
            outfile.write('\t'.join(new_line) + '\n')