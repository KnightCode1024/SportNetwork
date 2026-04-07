from taskiq import InMemoryBroker
from taskiq_aio_pika import AioPikaBroker

from sport_network_api.config.app import APPConfig
from sport_network_api.config.rabbitmq import RabbitMQConfig

app_config = APPConfig()
rabbitmq_config = RabbitMQConfig()

if app_config.MODE == "tests":
    broker = InMemoryBroker()
else:
    broker = AioPikaBroker(url=rabbitmq_config.URL)

# Import tasks to register them with the broker
import sport_network_api.infrastructure.tasks  # noqa: E402, F401