import os

def preproc_option():

    # Initialize options dictionary
    opt = {}
    
    # I like chatty outputs
    opt['verbosity'] = 2
    
    # task to analyze
    opt['taskName'] = 'alphabetLearning'
    
    # PATHS
    # The directory where the data are located
    opt['dir'] = {}
    opt['dir']['root'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
    opt['dir']['raw'] = os.path.join(opt['dir']['root'], 'inputs')
    opt['dir']['derivatives'] = os.path.join(opt['dir']['root'], 'outputs', 'derivatives')
    opt['dir']['extracted'] = os.path.join(opt['dir']['root'], 'outputs', 'derivatives', 'extracted-data')
    opt['dir']['stats'] = os.path.join(opt['dir']['root'], 'outputs', 'derivatives', 'stats')
    opt['dir']['input'] = opt['dir']['raw']
    # opt['dir']['stats'] = os.path.join(opt['dir']['root'], 'outputs', 'derivatives', 'analyses')
    
    # directory for the saved jobs
    opt['dir']['jobs'] = os.path.join(opt['dir']['derivatives'], 'jobs', opt['taskName'])
    
    # Type of pipeline
    opt['pipeline'] = {}
    opt['pipeline']['type'] = 'cleaning'
    
    # ASSIGN SUBJECTS AND SCRIPTS
    # Load from participants.tsv 
    with open(os.path.join(opt['dir']['raw'], 'participants.tsv'), 'r') as f:

        lines = f.readlines()
        
        # Extract subjects and scripts
        opt['subList'] = [line.split('\t')[0].strip() for line in lines[1:]]
        opt['scriptList'] = [line.split('\t')[1].strip() for line in lines[1:]]
    
    return opt
