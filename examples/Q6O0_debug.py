from nipype.interfaces import spm
import narps_open
from narps_open import pipelines
from importlib import *
from narps_open.pipelines import *
from os.path import join as opj
import os
import json
import pickle


def main():

    matlab_cmd = '/opt/spm12-r7219/run_spm12.sh /opt/matlabmcr-2010a/v713/ script'
    spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=True)
    team_ID = "Q6O0"
    # Important directories
    ## exp_dir : where the data are stored
    exp_dir = '/home/tritbool/workspace/narps_open_pipelines/data/original/ds001734/'

    ## result_dir : where the intermediate and final results will be store
    result_dir = "/home/tritbool/workspace/narps_open_pipelines/data/reproduced/"

    ## working_dir : where the intermediate outputs will be store
    working_dir = result_dir + f"NARPS-{team_ID}-reproduced/intermediate_results/"

    ## output_dir : where the final results will be store
    output_dir = result_dir + f"NARPS-{team_ID}-reproduced/"
    dir_list = os.listdir(exp_dir)

    # Subject list (to which we will do the analysis)
    subject_list = []
    for dirs in dir_list:
        if dirs[0:3] == 'sub':
            subject_list.append(dirs[-3:])
    # Run to use for this analysis
    run_list = ['01', '02', '03', '04']

    n_sub = len(subject_list)

    # TR
    with open(opj(exp_dir, 'task-MGT_bold.json'), 'rt') as fp:
        task_info = json.load(fp)
    TR = task_info['RepetitionTime']

    # FWHM to smooth (team chose a kernel of 8mm for smoothing)
    fwhm = 8
    subject_list = ['001']
    n_sub = 1

    from narps_open.pipelines import team_Q6O0

    class_type = getattr(
        import_module('narps_open.pipelines.team_' + team_ID),
        implemented_pipelines[team_ID])

    pipe = team_Q6O0.PipelineTeamQ6O0()
    pipe.directories.dataset_dir = exp_dir
    pipe.directories.results_dir = result_dir
    pipe.directories.output_dir = output_dir
    pipe.directories.working_dir = working_dir
    pipe.subject_list = subject_list
    pipe.run_list = run_list

    print(pipe.directories.working_dir)

    l1_analysis = pipe.get_subject_level_analysis()

    l1_analysis.run('MultiProc', plugin_args={'n_procs': 16})

    l2_analysis = pipe.get_group_level_analysis_sub_workflow("groupComp")
    l2_analysis.run('MultiProc', plugin_args={'n_procs': 16})

if __name__ == "__main__":
     main()