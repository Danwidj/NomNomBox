"""Schedule Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Schedule service."""
    return {
        'tags': [
            {
                'name': 'Schedule',
                'description': 'Operations for managing driver schedules and timeslot assignments',
                'x-displayName': 'Schedule'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Schedule Service',
                'tags': ['Schedule']
            }
        ],
        'paths': {
            '/schedule': OrderedDict([
                ('post', {
                    'tags': ['Schedule'],
                    'operationId': 'createTimeslotAssignment',
                    'summary': 'Create timeslot assignment',
                    'description': 'Assign a driver to a desired timeslot with Redis-based locking',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'desired_timeslot': {
                                            'type': 'integer',
                                            'description': 'Desired timeslot (Unix timestamp)'
                                        }
                                    },
                                    'required': ['desired_timeslot']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response(
                            'Driver assigned successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'id': {
                                        'type': 'integer',
                                        'description': 'Schedule ID'
                                    },
                                    'driver_id': {
                                        'type': 'integer',
                                        'description': 'Assigned driver ID'
                                    },
                                    'timeslot': {
                                        'type': 'integer',
                                        'description': 'Assigned timeslot (Unix timestamp)'
                                    },
                                    'assigned': {
                                        'type': 'boolean',
                                        'description': 'Assignment status'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Invalid JSON format in the request'),
                        '404': error_response('No drivers available for the desired timeslot'),
                        '500': error_response('Error updating the schedule')
                    }
                })
            ]),
            '/available_slots': OrderedDict([
                ('get', {
                    'tags': ['Schedule'],
                    'operationId': 'getAvailableSlots',
                    'summary': 'Get available timeslots',
                    'description': 'Get all available timeslots within a given time range',
                    'parameters': [
                        {
                            'name': 'start',
                            'in': 'query',
                            'required': True,
                            'schema': {'type': 'integer'},
                            'description': 'Start timestamp (Unix timestamp)'
                        },
                        {
                            'name': 'end',
                            'in': 'query',
                            'required': True,
                            'schema': {'type': 'integer'},
                            'description': 'End timestamp (Unix timestamp)'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Available slots retrieved successfully',
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'integer',
                                    'description': 'Available timeslot (Unix timestamp)'
                                }
                            }
                        ),
                        '400': error_response('Missing start or end timestamp'),
                        '500': error_response('Error retrieving available slots')
                    }
                })
            ]),
            '/message': OrderedDict([
                ('get', {
                    'tags': ['Schedule'],
                    'operationId': 'getMessages',
                    'summary': 'Get Kafka messages',
                    'description': 'Get the last consumed messages from Kafka about driver schedule updates',
                    'responses': {
                        '200': success_response(
                            'Messages retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'messages': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'description': 'Kafka message containing schedule updates'
                                        }
                                    }
                                }
                            }
                        )
                    }
                })
            ])
        }
    } 