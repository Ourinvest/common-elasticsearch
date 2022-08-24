import pytest

from elasticlogger.elasticsearch import ElasticsearchLogger


@pytest.fixture
def logger() -> ElasticsearchLogger:
    """
    Test following docker-compose.yml configuration
    :return: ElasticsearchLogger object
    """

    host = "localhost"
    port = "9200",
    service_name = "eslogger"
    simulate: bool = True
    return ElasticsearchLogger(host=host,
                               port=port,
                               service_name=service_name,
                               simulate=simulate)


def test_document_creation(logger: ElasticsearchLogger):
    test_payload = {"key1": "value1",
                    "key2": "value2",
                    "key3": "value3",
                    "key4": "value4"}
    logger.create_document(document_dict=test_payload)
