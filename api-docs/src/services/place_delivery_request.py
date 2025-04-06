"""Place a Delivery Request Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Delivery Request service."""
    return {
        'tags': [
            {
                'name': 'DeliveryRequest',
                'description': 'Operations for placing delivery requests',
                'x-displayName': 'Delivery Request Service'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Place a Delivery Request Service',
                'tags': ['DeliveryRequest']
            }
        ],
        'paths': OrderedDict([
            ('/', {
                'post': {
                    'tags': ['DeliveryRequest'],
                    'operationId': 'placeDeliveryRequest',
                    'summary': 'Submit delivery request',
                    'description': 'Create a new delivery request and assign a driver',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'user_id': {
                                            'type': 'string',
                                            'description': 'ID of the user placing the request'
                                        },
                                        'delivery_time': {
                                            'type': 'integer',
                                            'format': 'int64',
                                            'description': 'Desired delivery time (Unix timestamp)'
                                        },
                                        'order_id': {
                                            'type': 'string',
                                            'description': 'ID of the associated order'
                                        }
                                    },
                                    'required': ['user_id', 'delivery_time', 'order_id']
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
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Delivery request placed successfully'
                                    },
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'deliveryId': {
                                                'type': 'string',
                                                'description': 'Unique identifier for the created delivery'
                                            },
                                            'driverId': {
                                                'type': 'string',
                                                'description': 'ID of the assigned driver'
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '400': error_response('Invalid request format'),
                        '500': error_response('Internal server error')
                    }
                }
            })
        ]),
        'components': {
            'schemas': {
                'DeliveryRequest': {
                    'type': 'object',
                    'properties': {
                        'user_id': {'type': 'string'},
                        'delivery_time': {'type': 'integer', 'format': 'int64'},
                        'order_id': {'type': 'string'}
                    },
                    'required': ['user_id', 'delivery_time', 'order_id']
                },
                'DeliveryConfirmation': {
                    'type': 'object',
                    'properties': {
                        'deliveryId': {'type': 'string'},
                        'driverId': {'type': 'string'},
                        'estimatedArrival': {'type': 'integer', 'format': 'int64'}
                    }
                }
            }
        }
    }