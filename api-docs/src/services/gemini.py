"""Gemini Wrapper Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Gemini wrapper service."""
    return {
        'tags': [
            {
                'name': 'Gemini',
                'description': 'Operations for meal-kit recommendations using Gemini AI',
                'x-displayName': 'Gemini'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Gemini Service',
                'tags': ['Gemini']
            }
        ],
        'paths': {
            '/generate-recommendation': OrderedDict([
                ('post', {
                    'tags': ['Gemini'],
                    'operationId': 'generateRecommendation',
                    'summary': 'Generate meal-kit recommendations',
                    'description': 'Generate personalized meal-kit recommendations using Gemini AI based on user preferences and chat history',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'prompt': {
                                            'type': 'string',
                                            'description': 'User query or request for meal-kit recommendations'
                                        },
                                        'chat_history': {
                                            'type': 'array',
                                            'description': 'Previous chat messages between user and model',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'type': {
                                                        'type': 'string',
                                                        'enum': ['user', 'model'],
                                                        'description': 'Type of message (user or model)'
                                                    },
                                                    'prompt': {
                                                        'type': 'string',
                                                        'description': 'User message content'
                                                    },
                                                    'response': {
                                                        'type': 'string',
                                                        'description': 'Model response content'
                                                    }
                                                }
                                            }
                                        },
                                        'dietary_preferences': {
                                            'type': 'array',
                                            'description': 'List of user dietary preferences',
                                            'items': {
                                                'type': 'string'
                                            }
                                        },
                                        'order_history': {
                                            'type': 'array',
                                            'description': 'List of previous orders',
                                            'items': {
                                                'type': 'object'
                                            }
                                        },
                                        'inventory': {
                                            'type': 'array',
                                            'description': 'Current warehouse inventory',
                                            'items': {
                                                'type': 'object'
                                            }
                                        }
                                    },
                                    'required': ['prompt']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Recommendations generated successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'prompt': {
                                        'type': 'string',
                                        'description': 'Original user prompt'
                                    },
                                    'response': {
                                        'type': 'string',
                                        'description': 'Natural language response explaining the recommendations'
                                    },
                                    'recommended meal-kit': {
                                        'type': 'array',
                                        'description': 'List of recommended meal-kit IDs',
                                        'items': {
                                            'type': 'string',
                                            'enum': ['MK001', 'MK002', 'MK004', 'MK005', 'MK006', 'MK008', 'MK009']
                                        },
                                        'maxItems': 3,
                                        'minItems': 0
                                    }
                                }
                            }
                        ),
                        '400': error_response('Invalid request data or missing prompt'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    } 