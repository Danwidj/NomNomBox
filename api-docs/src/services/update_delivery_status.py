"""Update Delivery Status Service API specification."""

def get_specification():
    """Return the OpenAPI specification for the Update Delivery Status service."""
    return {
        'tags': [
            {
                'name': 'DeliveryStatus',
                'description': 'Operations for updating delivery status',
                'x-displayName': 'Delivery Status Service'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Update Delivery Status Service',
                'tags': ['DeliveryStatus']
            }
        ],
        'paths': {
            '/deliveries/{delivery_id}': {
                'patch': {
                    'tags': ['DeliveryStatus'],
                    'operationId': 'updateDeliveryStatus',
                    'summary': 'Update delivery status',
                    'description': 'Update the status of a delivery and trigger notifications',
                    'parameters': [
                        {
                            'name': 'delivery_id',
                            'in': 'path',
                            'required': True,
                            'schema': {
                                'type': 'integer'
                            },
                            'description': 'ID of the delivery to update'
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
                                            'description': 'ID of the associated order'
                                        },
                                        'status': {
                                            'type': 'string',
                                            'enum': [
                                                'Pending Cancellation',
                                                'Picked up by Driver',
                                                'Delivered by Driver',
                                                'Received by Customer'
                                            ],
                                            'description': 'New status of the delivery'
                                        },
                                        'timeslot': {
                                            'type': 'integer',
                                            'format': 'int64',
                                            'description': 'Delivery timeslot (Unix timestamp)'
                                        }
                                    },
                                    'required': ['order_id', 'status', 'timeslot']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': {
                            'description': 'Delivery status updated successfully',
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
                                                'example': 'Delivery status updated'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        '400': {
                            'description': 'Invalid request format',
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
                                                'example': 'Invalid JSON input'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        '401': {
                            'description': 'Unauthorized - Invalid Firebase credentials',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'code': {
                                                'type': 'integer',
                                                'example': 401
                                            },
                                            'message': {
                                                'type': 'string',
                                                'example': 'Invalid credentials while connecting to firebase for auth token'
                                            },
                                            'error': {
                                                'type': 'object',
                                                'description': 'Error details from Firebase'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        '404': {
                            'description': 'Order or customer not found',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'code': {
                                                'type': 'integer',
                                                'example': 404
                                            },
                                            'message': {
                                                'type': 'string',
                                                'example': 'Order not found'
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        '500': {
                            'description': 'Internal server error',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'code': {
                                                'type': 'integer',
                                                'example': 500
                                            },
                                            'message': {
                                                'type': 'string',
                                                'example': 'Failed to update delivery status'
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'components': {
            'schemas': {
                'DeliveryStatusUpdate': {
                    'type': 'object',
                    'properties': {
                        'order_id': {'type': 'string'},
                        'status': {
                            'type': 'string',
                            'enum': [
                                'Pending Cancellation',
                                'Picked up by Driver',
                                'Delivered by Driver',
                                'Received by Customer'
                            ]
                        },
                        'timeslot': {'type': 'integer', 'format': 'int64'}
                    },
                    'required': ['order_id', 'status', 'timeslot']
                },
                'NotificationMessage': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string'},
                        'delivery_id': {'type': 'integer'},
                        'email': {'type': 'string'},
                        'name': {'type': 'string'},
                        'order_id': {'type': 'string'}
                    }
                }
            }
        }
    }