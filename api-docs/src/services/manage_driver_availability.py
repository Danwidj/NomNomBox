"""Manage Driver Availability Service API specification."""

def get_specification():
    """Return the OpenAPI specification for the Manage Driver Availability service."""
    return {
        'openapi': '3.0.0',  # Required OpenAPI version
        'info': {
            'title': 'Manage Driver Availability Service',
            'version': '1.0.0',
            'description': 'API for managing driver availability timeslots'
        },
        'tags': [
            {
                'name': 'Availability',  # Changed to match usage in paths
                'description': 'Operations for managing driver availability',
                'x-displayName': 'Manage Driver Availability Service'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Manage Driver Availability Service',
                'tags': ['Availability']  # Now matches the tag name
            }
        ],
        'paths': {
            '/availability': {
                'post': {
                    'tags': ['Availability'],  # Now consistent
                    'operationId': 'updateAvailability',
                    'summary': 'Update driver availability',
                    'description': 'Update a driver\'s available timeslots and check for conflicts',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'driver_id': {
                                            'type': 'integer',
                                            'description': 'ID of the driver'
                                        },
                                        'changes': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'change_type': {
                                                        'type': 'string',
                                                        'enum': ['add', 'delete'],
                                                        'description': 'Type of change to make (add or remove timeslot)'
                                                    },
                                                    'timeslot': {
                                                        'type': 'integer',
                                                        'format': 'int64',
                                                        'description': 'Unix timestamp of the timeslot'
                                                    }
                                                },
                                                'required': ['change_type', 'timeslot']
                                            },
                                            'description': 'List of timeslot changes to apply'
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
                                            'code': {
                                                'type': 'integer',
                                                'example': 200,
                                                'description': 'Status code'
                                            },
                                            'message': {  # Added this required field
                                                'type': 'string',
                                                'example': 'Availability updated successfully'
                                            },
                                            'results': {
                                                'type': 'object',
                                                'description': 'Results from the availability update',
                                                'properties': {
                                                    'updated_slots': {
                                                        'type': 'integer',
                                                        'description': 'Number of timeslots updated'
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        '400': {
                            'description': 'Invalid request or timeslot conflict',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'code': {
                                                'type': 'integer',
                                                'example': 400,
                                                'description': 'Error code'
                                            },
                                            'message': {
                                                'type': 'string',
                                                'example': 'Driver is already assigned to a delivery in the occupied timeslot',
                                                'description': 'Error message'
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
                                                'example': 500,
                                                'description': 'Error code'
                                            },
                                            'message': {
                                                'type': 'string',
                                                'example': 'Internal server error',
                                                'description': 'Error message'
                                            },
                                            'error_details': {
                                                'type': 'string',
                                                'nullable': True,
                                                'description': 'Detailed error information for debugging'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'components': {  # Added components section
            'schemas': {
                'AvailabilityUpdate': {
                    'type': 'object',
                    'properties': {
                        'driver_id': {'type': 'integer'},
                        'changes': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'change_type': {'type': 'string', 'enum': ['add', 'delete']},
                                    'timeslot': {'type': 'integer', 'format': 'int64'}
                                },
                                'required': ['change_type', 'timeslot']
                            }
                        }
                    },
                    'required': ['driver_id', 'changes']
                }
            }
        }
    }