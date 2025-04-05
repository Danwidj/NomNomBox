"""Common schema definitions for API documentation."""

def error_response(description="Error response", custom_schema=None):
    """Return a standard error response schema."""
    schema = {
        'type': 'object',
        'properties': {
            'code': {
                'type': 'integer',
                'example': 400
            },
            'message': {
                'type': 'string',
                'description': 'Error message'
            }
        }
    }
    
    # If a custom schema is provided, use it instead of the default
    if custom_schema:
        schema = custom_schema
        
    return {
        'description': description,
        'content': {
            'application/json': {
                'schema': schema
            }
        }
    }

def success_response(description="Success response", example_data=None):
    """Return a standard success response schema."""
    schema = {
        'type': 'object',
        'properties': {
            'code': {
                'type': 'integer',
                'example': 200
            },
            'message': {
                'type': 'string',
                'description': 'Success message'
            }
        }
    }
    
    # Add example_data to schema if provided
    if example_data:
        schema['properties']['data'] = example_data
        
    return {
        'description': description,
        'content': {
            'application/json': {
                'schema': schema
            }
        }
    }