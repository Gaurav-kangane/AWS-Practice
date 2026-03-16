import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Get instance ID from EventBridge event
    instance_id = event['detail']['instance-id']

    # Get details of that instance
    response = ec2.describe_instances(InstanceIds=[instance_id])

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:

            for device in instance['BlockDeviceMappings']:

                if 'Ebs' in device:
                    volume_id = device['Ebs']['VolumeId']

                    # Create snapshot
                    snapshot = ec2.create_snapshot(
                        VolumeId=volume_id,
                        Description=f"Snapshot for {instance_id} at {datetime.utcnow()}"
                    )

                    snapshot_id = snapshot['SnapshotId']

                    # Add tags
                    ec2.create_tags(
                        Resources=[snapshot_id],
                        Tags=[
                            {"Key": "InstanceId", "Value": instance_id},
                            {"Key": "CreatedBy", "Value": "Lambda"},
                            {"Key": "Date", "Value": datetime.utcnow().strftime("%Y-%m-%d")}
                        ]
                    )

                    print(f"Snapshot {snapshot_id} created for volume {volume_id}")

    return {
        "statusCode": 200,
        "body": f"Snapshots created for instance {instance_id}"
    }
