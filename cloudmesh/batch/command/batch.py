from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from datetime import datetime
from  cloudmesh.cm4.batch.Batch import SlurmCluster

# from cloudmesh.batch.api.manager import Manager

class BatchCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_batch(self, args, arguments):
        """
        ::

          Usage:
            batch create-job JOB_NAME --slurm-script=SLURM_SCRIPT_PATH --input-type=INPUT_TYPE --slurm-cluster=SLURM_CLUSTER_NAME --job-script-path=SCRIPT_PATH --remote-path=REMOTE_PATH --local-path=LOCAL_PATH [--argfile-path=ARGUMENT_FILE_PATH] [--outfile-name=OUTPUT_FILE_NAME] [--suffix=SUFFIX] [--overwrite]
            batch run-job JOB_NAME
            batch fetch JOB_NAME
            batch test-connection SLURM_CLUSTER_NAME
            batch set-param slurm-cluster CLUSTER_NAME PARAMETER VALUE
            batch set-param job-metadata JOB_NAME PARAMETER VALUE
            batch list slurm-clusters [DEPTH [default:1]]
            batch list jobs [DEPTH [default:1]]
            batch remove slurm-cluster CLUSTER_NAME
            batch remove job JOB_NAME
            batch clean-remote JOB_NAME

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        arguments.FILE = arguments['--file'] or None

        print(arguments)


        debug = arguments["--debug"]

        if arguments.get("batch"):

            #
            # create slurm manager so it can be used in all commands
            #
            slurm_manager = SlurmCluster(debug=debug)

            if arguments.get("create-job") and arguments.get("JOB_NAME"):
                job_name = arguments.get("JOB_NAME")
                slurm_script_path = arguments.get("--slurm-script")
                input_type = arguments.get("--input-type")
                assert input_type in ['params', 'params+file'], "Input type can be either params or params+file"
                if input_type == 'params+file':
                    assert arguments.get("--argfile-path") is not None, "Input type is params+file but the input \
                        filename is not specified"
                slurm_cluster_name = arguments.get("--slurm-cluster")
                job_script_path = arguments.get("--job-script-path")
                remote_path = arguments.get("--remote-path")
                local_path = arguments.get("--local-path")
                random_suffix = '_' + str(datetime.now()).replace('-', '').replace(' ', '_').replace(':', '')[
                                      0:str(datetime.now()).replace('-', '').replace(' ', '_').replace(':',
                                                                                                       '').index(
                                          '.') + 3].replace('.', '')
                suffix = random_suffix if arguments.get("suffix") is None else arguments.get("suffix")
                overwrite = False if type(arguments.get("--overwrite")) is None else arguments.get("--overwrite")
                argfile_path = '' if arguments.get("--argfile-path") is None else arguments.get("--argfile-path")
                slurm_manager.create(job_name, slurm_cluster_name, slurm_script_path, input_type,
                                     job_script_path, argfile_path, remote_path, local_path,
                                     suffix, overwrite)

            elif arguments.get("remove"):
                if arguments.get("slurm-cluster"):
                    slurm_manager.remove("slurm-cluster", arguments.get("CLUSTER_NAME"))
                if arguments.get("job"):
                    slurm_manager.remove("job", arguments.get("JOB_NAME"))

            elif arguments.get("list"):
                max_depth = 1 if arguments.get("DEPTH") is None else int(arguments.get("DEPTH"))
                if arguments.get("slurm-clusters"):
                    slurm_manager.list("slurm-clusters", max_depth)
                elif arguments.get("jobs"):
                    slurm_manager.list("jobs", max_depth)

            elif arguments.get("set-param"):
                if arguments.get("slurm-cluster"):
                    cluster_name = arguments.get("CLUSTER_NAME")
                    parameter = arguments.get("PARAMETER")
                    value = arguments.get("VALUE")
                    slurm_manager.set_param("slurm-cluster", cluster_name, parameter, value)

                if arguments.get("job-metadata"):
                    config_name = arguments.get("JOB_NAME")
                    parameter = arguments.get("PARAMETER")
                    value = arguments.get("VALUE")
                    slurm_manager.set_param("job-metadata", config_name, parameter, value)
            elif arguments.get("run-job"):
                job_name = arguments.get("JOB_NAME")
                slurm_manager.run(job_name)
            elif arguments.get("fetch"):
                job_name = arguments.get("JOB_NAME")
                slurm_manager.fetch(job_name)
            elif arguments.get("test-connection"):
                slurm_cluster_name = arguments.get("SLURM_CLUSTER_NAME")
                slurm_manager.connection_test(slurm_cluster_name)
            elif arguments.get("clean-remote"):
                job_name = arguments.get("JOB_NAME")
                slurm_manager.clean_remote(job_name)