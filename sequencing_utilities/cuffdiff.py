﻿from pandas import read_table
import os

def load_cuffdiff(filename):
    if os.path.isdir(filename):
        filename = os.path.join(filename, "isoform_exp.diff")
    table = read_table(filename, index_col="test_id",
        true_values=["yes"], false_values=["no"])
    table = table.rename(columns={"log2(fold_change)": "fold_change"})
    
    return table

def run_cuffdiff(samples_dir_1,samples_dir_2,sample_name_1,sample_name_2,organism,output_dir,
                   cuffdiff='cuffdiff',indexes_dir='../indexes/', threads = 1,
                   library_norm_method = 'quartile', fdr = 0.05,
                   library_type ='fr-firststrand',
                   index_type='.gtf',
                   more_options=None):
    '''Run cuffdiff from the commandline

    Input:
    samples_dir_1 = list of sample directories for each replicate in sample 1
    samples_dir_2 = list of sample directories for each replicate in sample 2
    samples_name_1 = sample name for sample 1
    samples_name_1 = sample name for sample 2
    organism = organism name
    output_dir = directory of cuffdiff output
    cuffdiff = string to run cuffdiff (give the absolute directory of cuffdiff.exe if cuffdiff is not in PATH)
    indexes_dir = directory where indexes are located
    library_type = string indicating the library type (e.g. fr-first-strand)
    more_options = other options not specified (e.g. '--library-type fr-firststrand)

    Output:
    
    Example usage:
    directories for this example: 
          /home/douglas/Documents/RNA_sequencing/fastq
          /home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4 (sample 1 .bam file locations)
          /home/douglas/Documents/RNA_sequencing/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1 (sample 2 .bam file locations)
          /home/douglas/Documents/RNA_sequencing/indexes (.gtf file location)
          /home/douglas/Documents/RNA_sequencing/fastq/ (output directory) 
    
    at the terminal:
    cd /home/douglas/Documents/RNA_sequencing/fastq
    python3

    at the python command line:
    from resequencing_utilities.cuffdiff import run_cuffdiff
    run_cuffdiff(['/home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/140818_11_OxicEvo04EcoliGlcM9_Broth-4.bam'],
        ['/home/douglas/Documents/RNA_sequencing/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1.bam'],
        '140818_11_OxicEvo04EcoliGlcM9_Broth-4','140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1',
        'ecoli_mg1655',
        '/home/douglas/Documents/RNA_sequencing/fastq/',
        threads = 48)

    '''
    
    # parse input into string values
    sample_1=','.join(samples_dir_1);
    sample_2=','.join(samples_dir_2);
    
    if index_type in ['.gtf','.gff']:
        gff_index = indexes_dir + organism + index_type
    else:
        print('index_type not recognized.')

    cuffdiff_options = "--library-type %s --library-norm-method %s --FDR %s --num-threads %s" % \
        (library_type,library_norm_method,fdr,threads);
    if more_options:
        cuffdiff_options = cuffciff_options + ' ' + more_options;

    samples_message = sample_name_1 + "_vs_" + sample_name_2;

    # make the cuffdiff_command
    #cuffdiff [options] <transcripts.gtf> <sample1_replicate1.bam,...> <sample2_replicate1.bam,...> 
    cuffdiff_command = "%s %s -o %s -L %s,%s %s %s %s " % \
        (cuffdiff, cuffdiff_options, output_dir, sample_name_1,sample_name_2,gff_index, sample_1,sample_2);

    # execute the command
    print(cuffdiff_command)
    os.system(cuffdiff_command)

def run_cuffnorm(samples_dirs,samples_names,organism,output_dir,
                   cuffnorm='cuffnorm',indexes_dir='../indexes/', threads = 1,
                   library_norm_method = 'quartile',
                   library_type ='fr-firststrand',
                   index_type='.gtf',
                   more_options=None):
    '''Run cuffnorm from the commandline

    Input:
    samples_dirs = list of strings of sample directories for each replicate in samples 1-N
                use "," to seperate replicates per sample
                use "|" to seperate lists of replicates
        where sample_dirs = s1-r1,s1-r2,s1-r3,...|s2-r1,s2-r2,s2-r3,...|...|sN-r1,sN-r2,sN-r3,...
    samples_names = sample name for sample 1-N
        s1,s2,...,sN,...
    organism = organism name
    output_dir = directory of cuffnorm output
    cuffnorm = string to run cuffnorm (give the absolute directory of cuffnorm.exe if cuffnorm is not in PATH)
    indexes_dir = directory where indexes are located
    library_type = string indicating the library type (e.g. fr-first-strand)
    index_type = string indicating the index file extention (e.g. '.gtf' or '.gff')
    more_options = other options not specified (e.g. '--library-type fr-firststrand)

    Output:
    
    Example usage:
    directories for this example: 
          /home/douglas/Documents/RNA_sequencing/fastq
          /home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4 (sample 1 .bam file locations)
          /home/douglas/Documents/RNA_sequencing/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1 (sample 2 .bam file locations)
          /home/douglas/Documents/RNA_sequencing/indexes (.gtf file location)
          /home/douglas/Documents/RNA_sequencing/fastq/ (output directory) 
    
    at the terminal:
    cd /home/douglas/Documents/RNA_sequencing/fastq
    python3

    at the python command line:
    from resequencing_utilities.cuffdiff import run_cuffnorm
    run_cuffnorm(
        '/home/douglas/Documents/RNA_sequencing/fastq/140818_11_OxicEvo04EcoliGlcM9_Broth-4/140818_11_OxicEvo04EcoliGlcM9_Broth-4.bam,\
            /home/douglas/Documents/RNA_sequencing/fastq/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1/140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1.bam',
        '140818_11_OxicEvo04EcoliGlcM9_Broth-4,140716_0_OxicEvo04pgiEcoliGlcM9_Broth-1',
        'ecoli_mg1655',
        '/home/douglas/Documents/RNA_sequencing/fastq/',
        threads = 48)

    NOTES:
    I apologize in advance for the use of strings to specify sample_dirs/sample_names
    strings are used to avoid errors when pass the arguments in at the command line

    '''
    
    # parse input into string values
    sample_1 = [];
    for sdir in samples_dirs:
        sample_tmp=','.join(sdir);
        sample_1.append(sample_tmp);
        
    if index_type in ['.gtf','.gff']:
        gff_index = indexes_dir + organism + index_type
    else:
        print('index_type not recognized.')

    cuffnorm_options = "--library-type %s --library-norm-method %s --num-threads %s" % \
        (library_type,library_norm_method,threads);
    if more_options:
        cuffnorm_options = cuffciff_options + ' ' + more_options;
    cuffnorm_L = samples_names;
    cuffnorm_samples_1 = samples_dirs.replace("|",' ');

    samples_message = samples_names.split(",")[0] + "_to_" + samples_names.split(",")[-1] + "_cuffnorm";

    # make the cuffnorm_command
    #cuffnorm [options] <transcripts.gtf> <sample1_replicate1.bam,...> <sample2_replicate1.bam,...> ... <sampleN_replicate1.bam,...>
    cuffnorm_command = "%s %s -o %s -L %s %s %s " % \
        (cuffnorm, cuffnorm_options, output_dir, cuffnorm_L,gff_index, cuffnorm_samples_1);

    # execute the command
    print(cuffnorm_command)
    os.system(cuffnorm_command)