"""Delivery Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Delivery service."""
    return {
        'tags': [
            {
                'name': 'Delivery',
                'description': 'Operations for managing deliveries',
                'x-displayName': 'Delivery'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Delivery Service',
                'tags': ['Delivery']
            }
        ],
        'paths': {
            '/place_delivery_request': OrderedDict([
                ('post', {
                    'tags': ['Delivery'],
                    'operationId': 'placeDeliveryRequest',
                    'summary': 'Place delivery request',
                    'description': 'Create a new delivery request and assign a driver',
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
                    'tags': ['Delivery'],
                    'operationId': 'getAssignedDeliveries',
                    'summary': 'Get assigned deliveries',
                    'description': 'Get all deliveries assigned to a specific driver',
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
                    'tags': ['Delivery'],
                    'operationId': 'updateDeliveryStatus',
                    'summary': 'Update delivery status',
                    'description': 'Update the status of a delivery',
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
            ]),
            '/availability': OrderedDict([
                ('post', {
                    'tags': ['Delivery'],
                    'operationId': 'updateDriverAvailability',
                    'summary': 'Update driver availability',
                    'description': 'Update a driver\'s availability for specific timeslots',
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
                        '400': error_response('Invalid request or driver already assigned to deliveries'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    } 