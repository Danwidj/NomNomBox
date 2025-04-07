"""Update Driver Schedule Service API specification."""

def get_specification():
    """Return the OpenAPI specification for the Update Schedule service."""
    return {
        'tags': [
            {
                'name': 'DriverSchedule',
                'description': 'Operations for managing driver schedule and availability',
                'x-displayName': 'Driver Schedule'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Driver Schedule Management',
                'tags': ['DriverSchedule']
            }
        ],
        'paths': {
            '/availability': {
                'post': {
                    'tags': ['DriverSchedule'],
                    'operationId': 'updateDriverAvailability',
                    'summary': 'Update driver availability schedule',
                    'description': 'Update a driver\'s availability. Prevents schedule changes if driver has delivery assignments in requested timeslots.',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'driver_id': {
                                            'type': 'string',
                                            'description': 'ID of the driver'
                                        },
                                        'changes': {
                                            'type': 'array',
                                            'description': 'List of timeslot changes',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'timeslot': {
                                                        'type': 'integer',
                                                        'format': 'int64',
                                                        'description': 'Timeslot timestamp (Unix)'
                                                    },
                                                    'change_type': {
                                                        'type': 'string',
                                                        'enum': ['add', 'delete'],
                                                        'description': 'Type of change to timeslot'
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
                        '200': {
                            'description': 'Availability updated successfully',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'code': {'type': 'integer', 'example': 200},
                                            'results': {'type': 'array', 'items': {'type': 'object'}}
                                        }
                                    }
                                }
                            }
                        },
                        '400': {
                            'description': 'Invalid input or scheduling conflict',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'code': {'type': 'integer', 'example': 400},
                                            'message': {'type': 'string', 'example': 'Driver is already assigned to a delivery in the occupied timeslot'}
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
                                            'code': {'type': 'integer', 'example': 500},
                                            'message': {'type': 'string', 'example': 'Internal server error: ...'}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
