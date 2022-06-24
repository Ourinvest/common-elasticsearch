import logging
from datetime import datetime

import boto3

from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection


class AWSSigner:
    client = None
    session = boto3.Session().get_credentials()
    credentials = session.get_credentials()
    region = session.region_name
    if credentials and region:
        signer = AWSV4SignerAuth(credentials, region)
    else:
        signer = None


class ElasticsearchLogger(AWSSigner):
    """
    Class describing how to connect to ES ou Amazon Elasticsearch Service
    """

    RESOURCE_ALREADY_EXISTS = 'resource_already_exists_exception'

    client = None

    def __init__(self, host: str, port: str, service_name: str):
        if not ElasticsearchLogger.client:
            ElasticsearchLogger.client = OpenSearch(
                hosts=[
                    {
                        "host": host,
                        "port": port,
                    }
                ],
                use_ssl=True,
                verify_certs=True,
                http_auth=ElasticsearchLogger.signer,
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
