"""Chat History Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Chat History service."""
    return {
        'tags': [
            {
                'name': 'Chat History',
                'description': 'Operations for managing chat history',
                'x-displayName': 'Chat History'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Chat History Service',
                'tags': ['Chat History']
            }
        ],
        'paths': {
            '/chat/{customer_id}': OrderedDict([
                ('post', {
                    'tags': ['Chat History'],
                    'operationId': 'addChatMessage',
                    'summary': 'Add chat message',
                    'description': 'Add a new chat message for a customer',
                    'parameters': [
                        {
                            'name': 'customer_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Customer ID'
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'role': {
                                            'type': 'string',
                                            'default': 'model',
                                            'description': 'Role of the message sender'
                                        },
                                        'prompt': {
                                            'type': 'string',
                                            'description': 'User input message'
                                        },
                                        'response': {
                                            'type': 'string',
                                            'description': 'System response message'
                                        },
                                        'recommended_meal_kits': {
                                            'type': 'array',
                                            'items': {'type': 'string'},
                                            'description': 'List of recommended meal kits'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Message added successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'document_id': {
                                        'type': 'string',
                                        'description': 'Created message ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Invalid request'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('get', {
                    'tags': ['Chat History'],
                    'operationId': 'getChatHistory',
                    'summary': 'Get chat history',
                    'description': 'Get chat history for a customer',
                    'parameters': [
                        {
                            'name': 'customer_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Customer ID'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Chat history retrieved successfully',
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'role': {
                                            'type': 'string',
                                            'description': 'Message sender role'
                                        },
                                        'prompt': {
                                            'type': 'string',
                                            'description': 'User input'
                                        },
                                        'response': {
                                            'type': 'string',
                                            'description': 'System response'
                                        },
                                        'recommended_meal_kits': {
                                            'type': 'array',
                                            'items': {'type': 'string'},
                                            'description': 'Recommended meal kits'
                                        },
                                        'created_at': {
                                            'type': 'string',
                                            'format': 'date-time',
                                            'description': 'Message timestamp'
                                        }
                                    }
                                }
                            }
                        ),
                        '404': error_response('Chat history not found'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('delete', {
                    'tags': ['Chat History'],
                    'operationId': 'deleteChatHistory',
                    'summary': 'Delete chat history',
                    'description': 'Delete all chat history for a customer',
                    'parameters': [
                        {
                            'name': 'customer_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Customer ID'
                        }
                    ],
                    'responses': {
                        '200': success_response('Chat history deleted successfully'),
                        '404': error_response('Chat history not found'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    } 