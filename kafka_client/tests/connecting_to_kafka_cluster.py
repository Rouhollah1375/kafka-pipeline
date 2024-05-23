from src.kafka_client.kafka_client import KafkaProducerAvro
from src.kafka_client.cluster_admin import ClusterAdmin
from src.kafka_client.schema_registry import SchemaRegisteryTopicClient

config = {
    'kafka-host': 'dev-server.local',
    'sr-url': 'http://dev-server.local:8081',
    'kafka-rest-url': 'http://dev-server.local:8082',
    'topic-name': 'test_topic'
}

# 1. creating the kafka topic
admin = ClusterAdmin(config['kafka-rest-url'])
clusters = admin.get_clusters()
admin.select_cluster(clusters[0])
admin.create_topic(config['topic-name'])

# 2. registering the schema of the data that is passed through that Kafka topic
sr = SchemaRegisteryTopicClient(config['sr-url'], config['topic-name'])
schema = sr.load_json_shcema('./test_topic_shcema.json')
sr.register_schema(schema)

# 3. creating Kafka producer
producer = KafkaProducerAvro(
    topic=config['topic-name'],
    bootstrap_server_host=config['kafka-host'],
    sr_url=config['sr-url']
)

for i in range(100):
    msg = { 'k1': 'hello', 'k2': 'bye' }
    producer.publish(str(i), msg)
