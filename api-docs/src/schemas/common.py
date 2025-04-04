"""Common schema definitions for API documentation."""

def error_response(description="Error response"):
    """Return a standard error response schema."""
    return {
        'description': description,
        'content': {
            'application/json': {
                'schema': {
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
            }
        }
    }

def success_response(description="Success response", example_data=None):
    """Return a standard success response schema."""
    return {
        'description': description,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'code': {
                            'type': 'integer',
                            'example': 200
                        },
                        'message': {
                            'type': 'string',
                            'description': 'Success message'
                        },
                        'data': example_data
                    }
                }
            }
        }
    } 