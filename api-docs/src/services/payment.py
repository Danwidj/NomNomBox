"""Payment Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Payment service."""
    return {
        'tags': [
            {
                'name': 'Payment',
                'description': 'Operations for managing payments using Stripe',
                'x-displayName': 'Payment'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Payment Service',
                'tags': ['Payment']
            }
        ],
        'paths': {
            '/api/payment/create': OrderedDict([
                ('post', {
                    'tags': ['Payment'],
                    'operationId': 'createPayment',
                    'summary': 'Create payment session',
                    'description': 'Create a Stripe Checkout session for payment processing',
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
                                        'amount': {
                                            'type': 'number',
                                            'description': 'Total payment amount'
                                        },
                                        'items': {
                                            'type': 'array',
                                            'description': 'List of items to pay for',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'name': {
                                                        'type': 'string',
                                                        'description': 'Item name'
                                                    },
                                                    'price': {
                                                        'type': 'number',
                                                        'description': 'Item price in dollars'
                                                    },
                                                    'quantity': {
                                                        'type': 'integer',
                                                        'description': 'Item quantity'
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    'required': ['orderId', 'amount', 'items']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response(
                            'Checkout session created',
                            {
                                'type': 'object',
                                'properties': {
                                    'sessionId': {
                                        'type': 'string',
                                        'description': 'Stripe Checkout session ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Missing required fields'),
                        '500': error_response('Error creating payment session')
                    }
                })
            ]),
            '/api/payment/public-key': OrderedDict([
                ('get', {
                    'tags': ['Payment'],
                    'operationId': 'getPublicKey',
                    'summary': 'Get Stripe public key',
                    'description': 'Get the Stripe public key for client-side integration',
                    'responses': {
                        '200': success_response(
                            'Public key retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'publicKey': {
                                        'type': 'string',
                                        'description': 'Stripe public key'
                                    }
                                }
                            }
                        ),
                        '500': error_response('Stripe public key is missing')
                    }
                })
            ]),
            '/api/payment/status': OrderedDict([
                ('get', {
                    'tags': ['Payment'],
                    'operationId': 'getPaymentStatus',
                    'summary': 'Get payment status',
                    'description': 'Check the status of a payment session',
                    'parameters': [
                        {
                            'name': 'session_id',
                            'in': 'query',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Stripe Checkout session ID'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Payment status retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'status': {
                                        'type': 'string',
                                        'description': 'Payment status (complete)',
                                        'enum': ['complete']
                                    },
                                    'orderId': {
                                        'type': 'string',
                                        'description': 'Associated order ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Missing session_id or payment not completed'),
                        '500': error_response('Error fetching payment status')
                    }
                })
            ])
        }
    } 