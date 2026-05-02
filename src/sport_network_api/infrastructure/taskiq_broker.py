from taskiq import InMemoryBroker
from taskiq_aio_pika import AioPikaBroker
from taskiq.middlewares import SmartRetryMiddleware

from sport_network_api.config.app import APPConfig
from sport_network_api.config.rabbitmq import RabbitMQConfig

app_config = APPConfig()
rabbitmq_config = RabbitMQConfig()

if app_config.MODE == "tests":
    broker = InMemoryBroker()
else:
    broker = AioPikaBroker(url=rabbitmq_config.URL).with_middlewares(
    SmartRetryMiddleware(
        default_retry_count=3,
        default_delay=10,
        use_jitter=True,
        use_delay_exponent=True,
        max_delay_exponent=120
    ),
)

import sport_network_api.infrastructure.tasks.notification.email
