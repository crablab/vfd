import boto3

def update_display_record(name, value):
    try:
        client = boto3.client("route53")

        response = client.change_resource_record_sets(
            HostedZoneId="Z093312912USRZWYPJ91W",
            ChangeBatch={
                "Comment": "add %s -> %s" % (name, value),
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": name,
                            "Type": "A",
                            "TTL": "300",
                            "ResourceRecords": [{"Value": value}],
                        },
                    }
                ],
            },
        )
    except Exception as e:
        return False

    return True
