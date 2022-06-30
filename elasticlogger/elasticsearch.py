import logging
from datetime import datetime

import boto3

from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection


class AWSSigner:
    session = boto3.Session()
    credentials = session.get_credentials()
    region = session.region_name

    @classmethod
    def signer(cls):
        if cls.credentials and cls.region:
            return AWSV4SignerAuth(cls.credentials, cls.region)
        else:
            return None


class ElasticsearchLogger(AWSSigner):
    """
    Class describing how to connect to ES ou Amazon Elasticsearch Service
    """

    RESOURCE_ALREADY_EXISTS = 'resource_already_exists_exception'

    client = None

    def __init__(self, host: str, port: str, service_name: str, simulate: bool = True):
        if not ElasticsearchLogger.client:
            self.auth = None if simulate else ElasticsearchLogger.signer()
            ElasticsearchLogger.client = OpenSearch(
                hosts=[
                    {
                        "host": host,
                        "port": port,
                    }
                ],
                use_ssl=True,
                verify_certs=True,
                http_auth=self.auth,
                connection_class=RequestsHttpConnection,
            )
        self.index_name = "{service_name}-{month}-{year}".format(service_name=service_name,
                                                                 month=datetime.now().month,
                                                                 year=datetime.now().year)
        self.index = self._create_index()

    def _create_index(self):
        """
        Tries to create the index
        """
        try:
            ElasticsearchLogger.client.indices.create(index=self.index_name, body={})
        except Exception as e:
            if not e.error == ElasticsearchLogger.RESOURCE_ALREADY_EXISTS:
                logging.error(e)
                return False
        return True

    def create_document(self, document_dict):
        self.client.index(index=self.index_name,
                          body=document_dict,
                          refresh=True)

    @staticmethod
    async def set_body(request: any, body: bytes):
        """Set body from RequestArgs:
        request (Request)
        body (bytes)
        """

        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive

    @staticmethod
    async def get_body(request: any) -> bytes:
        """Get body from request
        Args:
            request (Request)
        Returns:
            bytes
        """
        body = await request.body()
        await ElasticsearchLogger.set_body(request, body)
        return body
