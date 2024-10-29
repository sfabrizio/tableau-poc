from flask import Flask, jsonify
from tableau_embedding_service import TableauEmbeddingService

app = Flask(__name__)

tableau_service = TableauEmbeddingService(
    server_url='https://your-tableau-server.com',
    api_secret='your-api-secret'
)

@app.route('/api/tableau/embed', methods=['GET'])
def get_embed_url():
    workbook_id = request.args.get('workbookId')
    view_id = request.args.get('viewId')
    embed_url = tableau_service.get_embed_url(workbook_id, view_id)
    return jsonify({'embedUrl': embed_url})

if __name__ == '__main__':
    app.run(debug=True)