import datetime
import traceback
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from tableau_embedding_service import TableauEmbeddingService
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


# Initialize the Tableau service with your credentials
tableau_service = TableauEmbeddingService(
    server_url='https://prod-uk-a.online.tableau.com',
    site_id="",
    secret_id='',
    secret_value='',  
    client_id='',
)


@app.route('/api/tableau/workbooks', methods=['GET'])
def list_workbooks():
    try:
        logger.info("Received request to list workbooks")
        workbooks = tableau_service.list_workbooks_and_views()
        logger.info("Successfully retrieved workbooks")
        return jsonify(workbooks)
    except Exception as e:
        logger.error(f"Error in list_workbooks endpoint: {str(e)}")
        error_message = str(e)
        return jsonify({
            'error': error_message,
            'details': {
                'message': 'Failed to retrieve workbooks',
                'timestamp': datetime.datetime.now().isoformat()
            }
        }), 500

@app.route('/api/tableau/embed', methods=['GET'])
def get_embed_url():
    try:
        workbook_id = request.args.get('workbookId')
        view_id = request.args.get('viewId')
        
        logger.info(f"Received request for embed URL - workbook: {workbook_id}, view: {view_id}")
        
        if not workbook_id or not view_id:
            logger.error("Missing required parameters")
            return jsonify({
                'error': 'Missing parameters',
                'details': {
                    'message': 'workbookId and viewId are required',
                    'timestamp': datetime.datetime.now().isoformat()
                }
            }), 400
            
        embed_url = tableau_service.get_embed_url(workbook_id, view_id)
        logger.info("Successfully generated embed URL")
        return jsonify({'embedUrl': embed_url})
        
    except Exception as e:
        logger.error(f"Error in get_embed_url endpoint: {str(e)}")
        error_message = str(e)
        return jsonify({
            'error': error_message,
            'details': {
                'message': 'Failed to generate embed URL',
                'timestamp': datetime.datetime.now().isoformat()
            }
        }), 500

@app.route('/api/tableau/status', methods=['GET'])
def get_status():
    """Simple endpoint to test the connection to Tableau Server"""
    try:
        logger.info("Checking Tableau Server connection status")
        headers = tableau_service._get_server_connection()  # Get JWT headers
        
        # Use an API endpoint to test the connection
        status_url = f"{tableau_service.server_url}/api/3.15/sites/{tableau_service.site_id}"
        response = requests.get(status_url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Full content response: {response.content}")  # Log full error details
            logger.error(f"Full error response: {response.json()}")  # Log full error details
        response.raise_for_status()

        return jsonify({
            'status': 'success',
            'message': 'Successfully connected to Tableau Server',
            'server_url': tableau_service.server_url
        })
    except Exception as e:
       
        logger.error(f"Error checking server status: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'server_url': tableau_service.server_url
        }), 500

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    print('http://localhost:5000/api/tableau/status')
    print('http://localhost:5000/api/tableau/workbooks')
    print('http://localhost:5000/api/tableau/embed?workbookId=WorldIndicators&viewId=Population')
    app.run(debug=True, port=5000)