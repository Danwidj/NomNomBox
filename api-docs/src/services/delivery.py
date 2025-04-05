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
            '/delivery': OrderedDict([
                ('get', {
                    'tags': ['Delivery'],
                    'operationId': 'getDeliveries',
                    'summary': 'Get deliveries',
                    'description': 'Get deliveries based on provided query parameters',
                    'parameters': [
                        {
                            'name': 'driver_id',
                            'in': 'query',
                            'required': False,
                            'schema': {'type': 'string'},
                            'description': 'Driver ID to filter deliveries by driver'
                        },
                        {
                            'name': 'order_id',
                            'in': 'query',
                            'required': False,
                            'schema': {'type': 'string'},
                            'description': 'Order ID to filter deliveries by order'
                        },
                        {
                            'name': 'start_time',
                            'in': 'query',
                            'required': False,
                            'schema': {'type': 'integer'},
                            'description': 'Start time (Unix timestamp) for time range filtering'
                        },
                        {
                            'name': 'end_time',
                            'in': 'query',
                            'required': False,
                            'schema': {'type': 'integer'},
                            'description': 'End time (Unix timestamp) for time range filtering'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Deliveries retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'deliveries': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'id': {
                                                            'type': 'integer',
                                                            'description': 'Delivery ID'
                                                        },
                                                        'order_id': {
                                                            'type': 'string',
                                                            'description': 'Associated order ID'
                                                        },
                                                        'timeslot': {
                                                            'type': 'string',
                                                            'format': 'date-time',
                                                            'description': 'Delivery timeslot'
                                                        },
                                                        'driver_id': {
                                                            'type': 'integer',
                                                            'description': 'Driver ID'
                                                        },
                                                        'location': {
                                                            'type': 'string',
                                                            'description': 'Delivery location'
                                                        },
                                                        'cancellation_status': {
                                                            'type': 'string',
                                                            'nullable': True,
                                                            'description': 'Cancellation status'
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '404': error_response('No deliveries found for the specified criteria'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('post', {
                    'tags': ['Delivery'],
                    'operationId': 'createDelivery',
                    'summary': 'Create delivery',
                    'description': 'Create a new delivery',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'order_id': {
                                            'type': 'string',
                                            'description': 'Order ID'
                                        },
                                        'timeslot': {
                                            'type': 'integer',
                                            'description': 'Delivery timeslot (Unix timestamp)'
                                        },
                                        'location': {
                                            'type': 'string',
                                            'description': 'Delivery location'
                                        },
                                        'driver_id': {
                                            'type': 'integer',
                                            'description': 'Driver ID'
                                        },
                                        'cancellation_status': {
                                            'type': 'string',
                                            'nullable': True,
                                            'description': 'Cancellation status'
                                        }
                                    },
                                    'required': ['order_id', 'timeslot', 'location', 'driver_id']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response(
                            'Delivery created successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 201
                                    },
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {
                                                'type': 'integer',
                                                'description': 'Delivery ID'
                                            },
                                            'order_id': {
                                                'type': 'string',
                                                'description': 'Order ID'
                                            },
                                            'timeslot': {
                                                'type': 'string',
                                                'format': 'date-time',
                                                'description': 'Delivery timeslot'
                                            },
                                            'driver_id': {
                                                'type': 'integer',
                                                'description': 'Driver ID'
                                            },
                                            'location': {
                                                'type': 'string',
                                                'description': 'Delivery location'
                                            },
                                            'cancellation_status': {
                                                'type': 'string',
                                                'nullable': True,
                                                'description': 'Cancellation status'
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/delivery/{id}': OrderedDict([
                ('get', {
                    'tags': ['Delivery'],
                    'operationId': 'getDeliveryById',
                    'summary': 'Get delivery by ID',
                    'description': 'Get a delivery by its ID',
                    'parameters': [
                        {
                            'name': 'id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'integer'},
                            'description': 'Delivery ID'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Delivery retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {
                                                'type': 'integer',
                                                'description': 'Delivery ID'
                                            },
                                            'order_id': {
                                                'type': 'string',
                                                'description': 'Order ID'
                                            },
                                            'timeslot': {
                                                'type': 'string',
                                                'format': 'date-time',
                                                'description': 'Delivery timeslot'
                                            },
                                            'driver_id': {
                                                'type': 'integer',
                                                'description': 'Driver ID'
                                            },
                                            'location': {
                                                'type': 'string',
                                                'description': 'Delivery location'
                                            },
                                            'cancellation_status': {
                                                'type': 'string',
                                                'nullable': True,
                                                'description': 'Cancellation status'
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '404': error_response('Delivery not found'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('put', {
                    'tags': ['Delivery'],
                    'operationId': 'updateDelivery',
                    'summary': 'Update delivery',
                    'description': 'Update all fields of a delivery',
                    'parameters': [
                        {
                            'name': 'id',
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
                                            'type': 'string',
                                            'description': 'Order ID'
                                        },
                                        'timeslot': {
                                            'type': 'integer',
                                            'description': 'Delivery timeslot (Unix timestamp)'
                                        },
                                        'location': {
                                            'type': 'string',
                                            'description': 'Delivery location'
                                        },
                                        'driver_id': {
                                            'type': 'integer',
                                            'description': 'Driver ID'
                                        },
                                        'cancellation_status': {
                                            'type': 'string',
                                            'nullable': True,
                                            'description': 'Cancellation status'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Delivery updated successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {
                                                'type': 'integer',
                                                'description': 'Delivery ID'
                                            },
                                            'order_id': {
                                                'type': 'string',
                                                'description': 'Order ID'
                                            },
                                            'timeslot': {
                                                'type': 'string',
                                                'format': 'date-time',
                                                'description': 'Delivery timeslot'
                                            },
                                            'driver_id': {
                                                'type': 'integer',
                                                'description': 'Driver ID'
                                            },
                                            'location': {
                                                'type': 'string',
                                                'description': 'Delivery location'
                                            },
                                            'cancellation_status': {
                                                'type': 'string',
                                                'nullable': True,
                                                'description': 'Cancellation status'
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '404': error_response('Delivery not found'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('patch', {
                    'tags': ['Delivery'],
                    'operationId': 'patchDelivery',
                    'summary': 'Partially update delivery',
                    'description': 'Update specific fields of a delivery',
                    'parameters': [
                        {
                            'name': 'id',
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
                                            'type': 'string',
                                            'description': 'Order ID'
                                        },
                                        'timeslot': {
                                            'type': 'integer',
                                            'description': 'Delivery timeslot (Unix timestamp)'
                                        },
                                        'location': {
                                            'type': 'string',
                                            'description': 'Delivery location'
                                        },
                                        'driver_id': {
                                            'type': 'integer',
                                            'description': 'Driver ID'
                                        },
                                        'cancellation_status': {
                                            'type': 'string',
                                            'description': 'Cancellation status'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Delivery updated successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {
                                                'type': 'integer',
                                                'description': 'Delivery ID'
                                            },
                                            'order_id': {
                                                'type': 'string',
                                                'description': 'Order ID'
                                            },
                                            'timeslot': {
                                                'type': 'string',
                                                'format': 'date-time',
                                                'description': 'Delivery timeslot'
                                            },
                                            'driver_id': {
                                                'type': 'integer',
                                                'description': 'Driver ID'
                                            },
                                            'location': {
                                                'type': 'string',
                                                'description': 'Delivery location'
                                            },
                                            'cancellation_status': {
                                                'type': 'string',
                                                'nullable': True,
                                                'description': 'Cancellation status'
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '404': error_response('Delivery not found'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    }