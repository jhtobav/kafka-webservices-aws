import kafka
import json
import base64


def endpoint_produce_message(event, context):
    try:
        bodyevent = json.loads(str(event.get('body')))

        producer = kafka.KafkaProducer(bootstrap_servers='b-1.msk-uat-kafka-cluster.pwmgpt.c6.kafka.us-east-1.amazonaws.com:9092,b-2.msk-uat-kafka-cluster.pwmgpt.c6.kafka.us-east-1.amazonaws.com:9092')

        producer.send(bodyevent.get('msgType'),
                      base64.b64encode(base64.b64decode(bodyevent.get('msg').encode('utf-8', 'ignore'))))

        body = {
            "message": bodyevent.get('msg')
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response

    except Exception as e:

        body = {
            "message": str(e)
        }

        response = {
            "statusCode": 500,
            "body": json.dumps(body)
        }

        return response
