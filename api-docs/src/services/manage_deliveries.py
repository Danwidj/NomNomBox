"""Manage Deliveries Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Manage Deliveries service."""
    return {
        'tags': [
            {
                'name': 'Manage Deliveries',
                'description': 'Operations for managing delivery assignments and driver schedules',
                'x-displayName': 'Manage Deliveries'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Manage Deliveries Service',
                'tags': ['Manage Deliveries']
            }
        ],
        'paths': {
            '/message': OrderedDict([
                ('post', {
                    'tags': ['Manage Deliveries'],
                    'operationId': 'postMessage',
                    'summary': 'Post driver schedule message',
                    'description': 'Send a message to update driver schedules via Kafka',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'description': 'Driver schedule update message'
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Message sent successfully'),
                        '400': error_response('Invalid message format'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/availability': OrderedDict([
                ('post', {
                    'tags': ['Manage Deliveries'],
                    'operationId': 'updateAvailability',
                    'summary': 'Update driver availability',
                    'description': 'Update a driver\'s availability and check for conflicts with existing deliveries',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'driver_id': {
                                            'type': 'string',
                                            'description': 'Driver ID'
                                        },
                                        'changes': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'timeslot': {
                                                        'type': 'integer',
                                                        'description': 'Timeslot (Unix timestamp)'
                                                    },
                                                    'change_type': {
                                                        'type': 'string',
                                                        'enum': ['add', 'delete'],
                                                        'description': 'Type of availability change'
                                                    }
                                                },
                                                'required': ['timeslot', 'change_type']
                                            }
                                        }
                                    },
                                    'required': ['driver_id', 'changes']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Driver availability updated successfully'),
                        '400': error_response('Invalid request or driver has existing deliveries'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/place_delivery_request': OrderedDict([
                ('post', {
                    'tags': ['Manage Deliveries'],
                    'operationId': 'placeDeliveryRequest',
                    'summary': 'Place delivery request',
                    'description': 'Create a new delivery request with driver assignment and notifications',
                    'security': [{'BearerAuth': []}],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'user_id': {
                                            'type': 'string',
                                            'description': 'Customer ID'
                                        },
                                        'order_id': {
                                            'type': 'string',
                                            'description': 'Order ID'
                                        },
                                        'delivery_time': {
                                            'type': 'integer',
                                            'description': 'Desired delivery time (Unix timestamp)'
                                        }
                                    },
                                    'required': ['user_id', 'order_id', 'delivery_time']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Delivery request placed successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'deliveryId': {
                                        'type': 'string',
                                        'description': 'Assigned delivery ID'
                                    },
                                    'driverId': {
                                        'type': 'string',
                                        'description': 'Assigned driver ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Invalid request format'),
                        '401': error_response('Missing or invalid authorization token'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/deliveries': OrderedDict([
                ('get', {
                    'tags': ['Manage Deliveries'],
                    'operationId': 'getAssignedDeliveries',
                    'summary': 'Get assigned deliveries',
                    'description': 'Get all deliveries assigned to a specific driver with order status',
                    'parameters': [
                        {
                            'name': 'driver_id',
                            'in': 'query',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Driver ID'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Deliveries retrieved successfully',
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'delivery_id': {
                                            'type': 'string',
                                            'description': 'Delivery ID'
                                        },
                                        'timeslot': {
                                            'type': 'integer',
                                            'description': 'Delivery timeslot (Unix timestamp)'
                                        },
                                        'location': {
                                            'type': 'string',
                                            'description': 'Delivery location'
                                        },
                                        'order_id': {
                                            'type': 'string',
                                            'description': 'Associated order ID'
                                        },
                                        'status': {
                                            'type': 'string',
                                            'description': 'Delivery status',
                                            'enum': [
                                                'Assigned to Driver',
                                                'Picked up by Driver',
                                                'Delivered by Driver',
                                                'Received by Customer'
                                            ]
                                        }
                                    }
                                }
                            }
                        ),
                        '400': error_response('Missing driver_id parameter'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/deliveries/{delivery_id}': OrderedDict([
                ('patch', {
                    'tags': ['Manage Deliveries'],
                    'operationId': 'updateDeliveryStatus',
                    'summary': 'Update delivery status',
                    'description': 'Update delivery status and send notifications via RabbitMQ',
                    'parameters': [
                        {
                            'name': 'delivery_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'integer'},
                            'description': 'Delivery ID'
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'order_id': {
                                            'type': 'integer',
                                            'description': 'Order ID'
                                        },
                                        'status': {
                                            'type': 'string',
                                            'description': 'New delivery status',
                                            'enum': [
                                                'Picked up by Driver',
                                                'Delivered by Driver',
                                                'Received by Customer'
                                            ]
                                        }
                                    },
                                    'required': ['order_id', 'status']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Delivery status updated successfully'),
                        '400': error_response('Invalid request format'),
                        '404': error_response('Delivery or order not found'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    } 