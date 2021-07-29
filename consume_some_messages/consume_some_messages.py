import kafka
import json
import base64
import jwt


def endpoint_consume_some_messages(event, context):
    try:
        token = (event.get('headers')['Authorization']).replace("Bearer ", "")
        bodyevent = json.loads(str(event.get('body')))
        first_offset = bodyevent.get('firstOffset')
        last_offset = bodyevent.get('lastOffset')

        topic = (jwt.decode(token, verify=False)['cognito:username']) + "_OUT"

        consumer = kafka.KafkaConsumer(
            bootstrap_servers='b-1.msk-uat-kafka-cluster.pwmgpt.c6.kafka.us-east-1.amazonaws.com:9092,'
                              'b-2.msk-uat-kafka-cluster.pwmgpt.c6.kafka.us-east-1.amazonaws.com:9092',
            enable_auto_commit=False,
            auto_offset_reset='none',
            group_id=topic)

        topic_partition = kafka.TopicPartition(topic=topic, partition=0)

        consumer.assign([topic_partition])

        consumer.seek(topic_partition, int(first_offset))

        msgs = {}

        records = consumer.poll(1000)

        for topicPartition in records:
            if topicPartition.topic == topic:
                for consumerRecord in records[topicPartition]:
                    if consumerRecord.offset <= int(last_offset):
                        msgs[consumerRecord.offset] = (base64.b64encode(consumerRecord.value)).decode('utf-8', 'ignore')
                    else:
                        break

        consumer.close()

        body = {
            "message": msgs
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
