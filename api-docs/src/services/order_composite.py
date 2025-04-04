"""Order Composite Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Order Composite service."""
    return {
        'tags': [
            {
                'name': 'Order Composite',
                'description': 'Operations for managing order workflow across multiple services',
                'x-displayName': 'Order Composite'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Order Composite Service',
                'tags': ['Order Composite']
            }
        ],
        'paths': {
            '/order/checkout': OrderedDict([
                ('post', {
                    'tags': ['Order Composite'],
                    'operationId': 'checkout',
                    'summary': 'Checkout order',
                    'description': 'Process order checkout by checking inventory, creating order, and initiating payment',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'items': {
                                            'type': 'array',
                                            'description': 'List of items to order',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'id': {
                                                        'type': 'string',
                                                        'description': 'Item ID'
                                                    },
                                                    'name': {
                                                        'type': 'string',
                                                        'description': 'Item name'
                                                    },
                                                    'quantity': {
                                                        'type': 'integer',
                                                        'description': 'Quantity to order'
                                                    }
                                                }
                                            }
                                        },
                                        'totalPrice': {
                                            'type': 'number',
                                            'description': 'Total price of the order'
                                        }
                                    },
                                    'required': ['items', 'totalPrice']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response(
                            'Order placed, payment completed, and inventory updated',
                            {
                                'type': 'object',
                                'properties': {
                                    'orderId': {
                                        'type': 'string',
                                        'description': 'Created order ID'
                                    },
                                    'sessionId': {
                                        'type': 'string',
                                        'description': 'Payment session ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Error in checkout process (inventory/order/payment)'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/order/payment-success': OrderedDict([
                ('post', {
                    'tags': ['Order Composite'],
                    'operationId': 'paymentSuccess',
                    'summary': 'Process payment success',
                    'description': 'Handle successful payment by updating order status, adjusting inventory, and sending notifications',
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
                                            'description': 'Payment session ID'
                                        },
                                        'user_id': {
                                            'type': 'string',
                                            'description': 'Customer ID'
                                        },
                                        'token': {
                                            'type': 'string',
                                            'description': 'Authentication token'
                                        }
                                    },
                                    'required': ['orderId', 'session_id', 'user_id', 'token']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Payment confirmed, order updated, and stock adjusted'),
                        '400': error_response('Error in payment verification or updating order/inventory'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    } 