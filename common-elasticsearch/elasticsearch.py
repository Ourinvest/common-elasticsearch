import logging
import os
from typing import Dict

from datetime import datetime

from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


class ElasticsearchLogger:
    """
    Class describing how to connect to ES ou Amazon Elasticsearch Service
    """
    if os.environ.get('ENVIRONMENT', 'local') != "local":
        AWS_CREDENTIALS = AWSV4SignerAuth((os.environ.get('ACCESS_KEY'),
                                           os.environ.get('SECRET_KEY')), os.environ.get('REGION'))
    else:
        AWS_CREDENTIALS = None
    RESOURCE_ALREADY_EXISTS = 'resource_already_exists_exception'

    def __init__(self, service_name):
        self.index_name = f'{service_name}-{datetime.now().month}-{datetime.now().year}'
        self.client = OpenSearch(
            hosts=[{'host': os.environ.get('ELASTICSEARCH_HOST', 'localhost'),
                    'port': os.environ.get('ELASTICSEARCH_PORT', '9200')}],
            http_auth=ElasticsearchLogger.AWS_CREDENTIALS,
            connection_class=RequestsHttpConnection
        )
        self.index = self._create_index()

    def _create_index(self):
        """
        Tries to create the index, if it already exists will return an exception,
        for that reason we need to use a try/except clause.

        :return: bool (if the problem is ok True, else false)
        """
        try:
            self.client.indices.create(index=self.index_name, body={})
        except Exception as e:
            logging.error(e)
            if not e.error == ElasticsearchLogger.RESOURCE_ALREADY_EXISTS:
                return False
            else:
                return True
        return True

    def create_document(self, document_dict):
        try:
            self.client.index(index=self.index_name,
                              body=document_dict,
                              refresh=True)
        except Exception as e:
            logging.error(e)
            return False
        return True


async def send_logs(document: Dict):
    if not ElasticsearchLogger(service_name="operations").create_document(document_dict=document):
        logging.warning("Failed to log")