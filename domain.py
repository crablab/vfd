import boto3
import logging 

def update_display_record(name, value):
    try:
        client = boto3.client(
                "route53",
                aws_access_key_id=os.environ['aws_access_key_id'],
                aws_secret_access_key=os.environ['aws_secret_access_key']
                )

        response = client.change_resource_record_sets(
            HostedZoneId="Z093312912USRZWYPJ91W",
            ChangeBatch={
                "Comment": "add %s -> %s" % (name, value),
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": f'{name}.display.crablab.uk',
                            "Type": "A",
                            "TTL": 300,
                            "ResourceRecords": [{"Value": value}],
                        },
                    }
                ],
            },
        )
    except Exception as e:
        logging.error(e)
        return False

    return True
