# This is BOTO3 module project
# Learn boto3 

import boto3

def lambda_handler(events, contexts):
    # get the client
    client = boto3.client('ec2')

    # get the snapshots
    response = client.describe_snapshots(OwnerIds=['self'])
    
    #get all 'running' instnances
    instance_response = client.describe_instances(Filters=[ {'Name': 'instance-state-name','Values': ['running']}])
    
    # set for storing active instance ids
    active_instance_ids = set()
    
    # get the ids of all the active instances
    for reservation in instance_response["Reservations"]:
        for instance in reservation["Instances"]:
            active_instance_ids.add(instance["InstanceId"])

    # get the Snapshot ids and delete all snapshots which are not 1 and 2
    
 
    for snapshots in response["Snapshots"]:
        snapshot_id = snapshots["SnapshotId"]
        vol_id = snapshots["VolumeId"]

    # 1. volume not attahed to any EBS
        if not vol_id:
            client.delete_snapshot(SnapshotId=snapshot_id)
            print(f"deleted snpshot {snapshot_id} it was not associated with any Volume")

     # 2. EBS is not attached to running EC2
        else:
            try:    
                response_vol = client.describe_volumes( VolumeIds=[vol_id])
                if not response_vol["Volumes"][0]["Attachments"]:
                    client.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot {snapshot_id} as it was taken from a volume not attached to any running instance.")
            
            except client.exceptions.ClientError as err:
                if err.response["Error"]["Code"] == "InvalidVolume.NotFound":
                    print(f"volume associated with snashot{snapshot_id} in not found it might have been deleted")
               
                # The volume associated with the snapshot is not found (it might have been deleted)
               
                    client.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot {snapshot_id} as its associated volume was not found.")




lambda_handler("events", "contexts")


    
