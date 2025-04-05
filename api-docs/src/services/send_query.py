"""Send Query Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Send Query service."""
    return {
        'tags': [
            {
                'name': 'Send Query',
                'description': 'Operations for getting meal recommendations based on customer data and preferences',
                'x-displayName': 'Send Query'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Send Query Service',
                'tags': ['Send Query']
            }
        ],
        'paths': {
            '/api/recommendations/{customer_id}': OrderedDict([
                ('post', {
                    'tags': ['Send Query'],
                    'operationId': 'getMealRecommendations',
                    'summary': 'Get meal recommendations',
                    'description': 'Get personalized meal recommendations based on customer preferences, chat history, and order history',
                    'parameters': [
                        {
                            'name': 'customer_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Customer ID to get recommendations for'
                        }
                    ],
                    'security': [
                        {'BearerAuth': []}
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'prompt': {
                                            'type': 'string',
                                            'description': 'User query for meal recommendations'
                                        }
                                    },
                                    'required': ['prompt']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Recommendations retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'recommended meal-kit': {
                                        'type': 'array',
                                        'description': 'List of recommended meal kits',
                                        'items': {
                                            'type': 'object'
                                        }
                                    },
                                    'response': {
                                        'type': 'string',
                                        'description': 'Chatbot response explaining the recommendations'
                                    }
                                }
                            }
                        ),
                        '400': error_response(
                            'Customer ID is required',
                            {
                                'type': 'object',
                                'properties': {
                                    'error': {
                                        'type': 'string',
                                        'example': 'Customer ID is required'
                                    }
                                }
                            }
                        ),
                        '500': error_response(
                            'Service communication error or unexpected error',
                            {
                                'type': 'object',
                                'properties': {
                                    'error': {
                                        'type': 'string',
                                        'examples': [
                                            'Failed to fetch customer details',
                                            'Failed to fetch order history',
                                            'Failed to fetch available meal kits',
                                            'Failed to get recommendations',
                                            'Service communication error: {error details}',
                                            'Unexpected error: {error details}'
                                        ]
                                    },
                                    'response': {
                                        'type': 'object',
                                        'description': 'Original error response from the service',
                                        'nullable': True
                                    }
                                }
                            }
                        )
                    }
                })
            ])
        },
        'components': {
            'securitySchemes': {
                'BearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT',
                    'description': 'JWT token for authenticating with the Customer service'
                }
            }
        }
    }