from config.settings import conf


broker_url = conf.broker_url
result_backend = conf.result_backend

accept_content = ["application/json"]
task_serializer = "json"
result_serializer = "json"
broker_connection_retry_on_startup = True
enable_utc = True
broker_connection_timeout = 2
broker_pool_limit = None
