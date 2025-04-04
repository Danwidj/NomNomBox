"""
API Documentation Service for NomNomBox

This service provides a Swagger UI interface for all NomNomBox microservices.
It serves as a central documentation hub for API endpoints.
"""

# Standard library imports
import logging
import importlib
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Third party imports
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Local imports
from config import BASE_SPEC, SWAGGER_UI_CONFIG

# ===== App Configuration =====
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Swagger UI configuration
SWAGGER_URL = '/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config=SWAGGER_UI_CONFIG
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def load_service_specs():
    """Load all service specifications from the services directory."""
    specs = []
    services_dir = Path(__file__).parent / 'services'
    
    if not services_dir.exists():
        logging.error(f"Services directory not found: {services_dir}")
        return specs
    
    # List all Python files in the services directory
    service_files = sorted(services_dir.glob('*.py'))  # Sort files alphabetically
    
    for service_file in service_files:
        if service_file.name.startswith('__'):
            continue
            
        try:
            # Import the module
            module_name = service_file.stem
            module = importlib.import_module(f'services.{module_name}')
            
            # Get the specification
            if hasattr(module, 'get_specification'):
                spec = module.get_specification()
                if spec:
                    specs.append(spec)
                    logging.info(f"Successfully loaded specification from {module_name}")
                else:
                    logging.warning(f"Empty specification returned from {module_name}")
            else:
                logging.warning(f"Module {module_name} has no get_specification function")
        except ImportError as e:
            logging.error(f"Failed to import {module_name}: {str(e)}")
        except Exception as e:
            logging.error(f"Error loading specification from {module_name}: {str(e)}")
    
    if not specs:
        logging.warning("No service specifications were loaded")
    else:
        logging.info(f"Loaded {len(specs)} service specifications")
    
    return specs

# ===== Routes =====
@app.route('/')
def index():
    """Redirect root to API documentation."""
    return redirect('/docs')

@app.route('/swagger.json')
def serve_swagger_spec():
    """Serve the OpenAPI specification."""
    try:
        # Get base specification
        spec = BASE_SPEC.copy()
        
        # Load and merge all service specifications
        service_specs = load_service_specs()
        
        if not service_specs:
            logging.error("No service specifications were loaded")
            return jsonify({'error': 'No service specifications found'}), 500
        
        # Initialize empty lists/dicts for merging
        all_tags = []
        all_tag_groups = []
        all_paths = {}
        
        # Merge specifications
        for service_spec in service_specs:
            if not isinstance(service_spec, dict):
                logging.warning(f"Invalid specification format: {type(service_spec)}")
                continue
                
            all_tags.extend(service_spec.get('tags', []))
            all_tag_groups.extend(service_spec.get('x-tagGroups', []))
            all_paths.update(service_spec.get('paths', {}))
        
        # Sort tags and tag groups alphabetically
        all_tags.sort(key=lambda x: x.get('name', '').lower())
        all_tag_groups.sort(key=lambda x: x.get('name', '').lower())
        
        # Update the final specification
        spec.update({
            'tags': all_tags,
            'x-tagGroups': all_tag_groups,
            'paths': all_paths
        })
        
        return jsonify(spec)
    except Exception as e:
        logging.error(f"Error serving swagger spec: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

# ===== Main Entry Point =====
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 