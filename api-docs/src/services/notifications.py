"""Notifications Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Notifications service."""
    return {
        'tags': [
            {
                'name': 'Notifications',
                'description': 'Operations for managing user notifications',
                'x-displayName': 'Notifications'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Notifications Service',
                'tags': ['Notifications']
            }
        ],
        'paths': {
            '/notify': OrderedDict([
                ('post', {
                    'tags': ['Notifications'],
                    'operationId': 'sendNotification',
                    'summary': 'Send payment success notification',
                    'description': 'Send a payment success notification via RabbitMQ',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'orderId': {
                                            'type': 'string',
                                            'description': 'Order ID'
                                        },
                                        'session_id': {
                                            'type': 'string',
                                            'description': 'Session ID'
                                        },
                                        'customer_id': {
                                            'type': 'string',
                                            'description': 'Customer ID'
                                        },
                                        'customer_email': {
                                            'type': 'string',
                                            'description': 'Customer email address'
                                        }
                                    },
                                    'required': ['orderId', 'session_id', 'customer_id', 'customer_email']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Payment success notification queued for delivery',
                            {
                                'type': 'object',
                                'properties': {
                                    'success': {
                                        'type': 'boolean',
                                        'description': 'Operation success status'
                                    },
                                    'message': {
                                        'type': 'string',
                                        'description': 'Success message'
                                    },
                                    'orderId': {
                                        'type': 'string',
                                        'description': 'Order ID'
                                    },
                                    'customer_email': {
                                        'type': 'string',
                                        'description': 'Customer email address'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Missing required fields'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/notifications/{user_id}': OrderedDict([
                ('get', {
                    'tags': ['Notifications'],
                    'operationId': 'getUserNotifications',
                    'summary': 'Get user notifications',
                    'description': 'Retrieve notifications for a specific user',
                    'parameters': [
                        {
                            'name': 'user_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'User ID'
                        },
                        {
                            'name': 'limit',
                            'in': 'query',
                            'required': False,
                            'schema': {
                                'type': 'integer',
                                'default': 10
                            },
                            'description': 'Maximum number of notifications to return'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'User notifications retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'notifications': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'description': 'Notification details'
                                        }
                                    }
                                }
                            }
                        ),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/health': OrderedDict([
                ('get', {
                    'tags': ['Notifications'],
                    'operationId': 'healthCheck',
                    'summary': 'Health check',
                    'description': 'Check if the notifications service is healthy',
                    'responses': {
                        '200': success_response(
                            'Health check successful',
                            {
                                'type': 'object',
                                'properties': {
                                    'status': {
                                        'type': 'string',
                                        'description': 'Service health status'
                                    },
                                    'service': {
                                        'type': 'string',
                                        'description': 'Service name'
                                    }
                                }
                            }
                        )
                    }
                })
            ]),
            '/': OrderedDict([
                ('get', {
                    'tags': ['Notifications'],
                    'operationId': 'index',
                    'summary': 'Root endpoint',
                    'description': 'Check if the notifications service is running',
                    'responses': {
                        '200': success_response(
                            'Service status check successful',
                            {
                                'type': 'object',
                                'properties': {
                                    'message': {
                                        'type': 'string',
                                        'description': 'Service status message'
                                    }
                                }
                            }
                        )
                    }
                })
            ])
        }
    } 