import boto3
import urllib.parse


s3 = boto3.client('s3')
sns = boto3.client('sns')


def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        print("Using waiter to waiting for object to persist through s3 service")
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket=source_bucket, Key=object_key)
        ssn_response = sns.publish(TopicArn='arn:aws:sns:ap-south-1:xxxxxxxxxxxx:Sam-Intro-Topic',
                                   Message= "A new file '" + object_key + "' has been added",
                                   Subject='Message from SAM INTRO')
    except Exception as err:
        print("Error -" + str(err))
        return err