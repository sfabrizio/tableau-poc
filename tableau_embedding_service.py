from tableau_api_lib.Controller.TableauServerConnection import TableauServerConnection
from tableau_api_lib.Models.EndpointModel import EndpointModel

class TableauEmbeddingService:
    def __init__(self, server_url, api_secret):
        self.connection = TableauServerConnection(
            server_address=server_url,
            api_version='3.16',
            personal_access_token_name='Embedded App',
            personal_access_token_value=api_secret
        )
        self.connection.sign_in()

    def get_embed_url(self, workbook_id, view_id):
        embed_endpoint = EndpointModel(
            api_name='embedViews',
            url_suffix=f'workbooks/{workbook_id}/views/{view_id}',
            request_object=None
        )
        embed_url = self.connection.get_url_for_embedding(embed_endpoint)
        return embed_url