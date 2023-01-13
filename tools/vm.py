import sys, pathlib
outside_dir = pathlib.Path(__file__).resolve().parent.parent.parent 
working_dir = pathlib.Path(__file__).resolve().parent.parent 
current_dir = pathlib.Path(__file__).resolve().parent 
sys.path.append(str(working_dir))
sys.path.append(f"{str(working_dir)}/config")
sys.path.append(f"{str(working_dir)}/tools")
import os
from googleapiclient.discovery import build, Resource
from oauth2client.client import GoogleCredentials
import logging, time
import boto3
import discorder
import config

logging.basicConfig(level=logging.INFO,format="%(asctime)s : %(message)s")

#_______________________________________________________________________
# GCP #
GCP_project  = "september-362116"
GCP_zone     = "us-west1-a"
GCP_instance = "bt-24cpu-us-west1-a"

# AWS # Expired # FIXME:
AWS_access_key_id       = config.AWS_access_key_id
AWS_secret_access_key   = config.AWS_secret_access_key
AWS_region              = config.AWS_region
AWS_instance            = config.AWS_instance
#_______________________________________________________________________
# CODE SAMPLE

# if Platform == "AWS":
#     disco.send("Backtest ERROR", f"{strategy}{ActivationTime}", "ERROR---- Stopping Instance Because of System ERROR -----", name = f"{vm.AWS_instance}")
#     vm.AWS_stop(vm.AWS_instance)

# ---------  GCP  ----------

def GCP_start(project, zone, instance_name):
    credentials: GoogleCredentials = GoogleCredentials.get_application_default()
    compute: Resource = build('compute', 'v1', credentials=credentials)
    instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
    result: dict = compute.instances().start(project=project, zone=zone, instance=instance['name']).execute()
    # Wait Running
    while True:
        instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
        logging.info(instance["status"])
        # TERMINATED -> STAGING -> RUNNING
        if instance["status"] == "RUNNING":
            break
        time.sleep(5)


def GCP_stop(Platform, project, zone, instance_name):

    if Platform == "LOCAL":
        print("This is LOCAL MACHINE. NO INSTANCE TO STOP... good bye.")
    
    else:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{working_dir}/config/GCP_september.json"

        try:
            logging.warning(f"\n----- Trying to Stop Instance {instance_name}-----")

            discorder.send(f"STOPPING...", 
                        "VM stop automatically.", 
                        f"Going to try to Stop...", 
                        username = instance_name,
                        server = "vm")

            credentials: GoogleCredentials = GoogleCredentials.get_application_default()
            compute: Resource = build('compute', 'v1', credentials=credentials)
            instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
            result: dict = compute.instances().stop(project=project, zone=zone, instance=instance['name']).execute()

            # Wait Terminated
            while True:
                instance: dict = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
                logging.info(instance["status"])
                #  RUNNING -> STOPPING -> TERMINATED
                if instance["status"] == "TERMINATED":
                    break
                time.sleep(5)

            logging.warning(f"\n----- Stopped -----")

            discorder.send(f"STOPPED", 
                        "VM STOPPED automatically.", 
                        f"Stopped Successfully", 
                        username = instance_name,
                        server = "vm")

        except Exception as e:
            logging.warning(f"\n----- FAILD to Stop Instance -----")

            discorder.send(f"Virtual Machine STOPPING ERROR!...", 
                        "VM FAILD to STOP automatically.", 
                        f"FAILD to Stop... reason -> {e}", 
                        username = instance_name,
                        server = "error")


# ---------  AWS  ----------

def AWS_start(instance_id):
    AWS_client = boto3.client(  'ec2',
                                aws_access_key_id     = AWS_access_key_id,
                                aws_secret_access_key = AWS_secret_access_key,
                                region_name           = AWS_region)
    AWS_client.start_instances(InstanceIds=[instance_id])
    logging.info("stopping AWS Instances now")


def AWS_stop(instance_id):
    AWS_client = boto3.client(  'ec2',
                                aws_access_key_id     = AWS_access_key_id,
                                aws_secret_access_key = AWS_secret_access_key,
                                region_name           = AWS_region)
    AWS_client.stop_instances(InstanceIds=[instance_id])
    logging.info("stopping AWS Instances now")


#------------------------------------
if __name__ == "__main__":
    AWS_stop(AWS_instance)