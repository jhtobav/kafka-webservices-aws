import kafka
import json
import base64
import jwt


def endpoint_consume_all_messages(event, context):
    try:
        token = (event.get('headers')['Authorization']).replace("Bearer ", "")
        topic = (jwt.decode(token, verify=False)['cognito:username']) + "_OUT"

        # consumer = kafka.KafkaConsumer(bootstrap_servers='172.16.0.13:9092',
        #                                enable_auto_commit=False,
        #                                group_id=topic)
        #
        # topic_partition = kafka.TopicPartition(topic=topic, partition=0)
        #
        # consumer.assign([topic_partition])
        # consumer.seek_to_beginning()

        consumer = kafka.KafkaConsumer(
            bootstrap_servers='b-1.msk-uat-kafka-cluster.pwmgpt.c6.kafka.us-east-1.amazonaws.com:9092'
                              ',b-2.msk-uat-kafka-cluster.pwmgpt.c6.kafka.us-east-1.amazonaws.com:9092',
            enable_auto_commit=False,
            group_id=topic)

        topic_partition = kafka.TopicPartition(topic=topic, partition=0)

        consumer.assign([topic_partition])

        consumer.seek_to_beginning(topic_partition)

        msgs = {}

        records = consumer.poll(1000)

        for topicPartition in records:
            if topicPartition.topic == topic:
                for consumerRecord in records[topicPartition]:
                    msgs[consumerRecord.offset] = (base64.b64encode(consumerRecord.value)).decode('utf-8', 'ignore')

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
