import os
from datetime import datetime
from fastapi.requests import Request

from opensearchpy import OpenSearch, RequestsHttpConnection


class ElasticsearchLogger:
    """
    Class describing how to connect to ES ou Amazon Elasticsearch Service
    """

    def __init__(self, service_name, credentials=None):
        self.index_name = f"{service_name}-{datetime.now().month}-{datetime.now().year}"
        self.client = OpenSearch(
            hosts=[
                {
                    "host": os.environ.get("ELASTICSEARCH_HOST", "localhost"),
                    "port": os.environ.get("ELASTICSEARCH_PORT", "9200"),
                }
            ],
            use_ssl=True,
            verify_certs=True,
            http_auth=credentials,
            connection_class=RequestsHttpConnection,
        )

    def _create_index(self):
        """
        Tries to create the index
        """
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(index=self.index_name, body={})

    async def create_document(self, document_dict):
        self._create_index()
        self.client.index(index=self.index_name, body=document_dict, refresh=True)


    @staticmethod
    async def set_body(request: Request, body: bytes):
        """Set body from RequestArgs:
        request (Request)
        body (bytes)
        """

        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive

    @staticmethod
    async def get_body(request: Request) -> bytes:
        """Get body from request
        Args:
            request (Request)
        Returns:
            bytes
        """
        body = await request.body()
        await ElasticsearchLogger.set_body(request, body)
        return body
