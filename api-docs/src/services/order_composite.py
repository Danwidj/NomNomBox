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
                                        'customerId': {
                                            'type': 'string',
                                            'description': 'Customer ID'
                                        },
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
                                    'required': ['customerId', 'items', 'totalPrice']
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
                                    'code': {
                                        'type': 'integer',
                                        'example': 201
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Order placed, payment completed, and numAvailable updated'
                                    },
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
                        '400': error_response(
                            'Error in checkout process (inventory/order/payment)',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 400
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Error fetching inventory for {item name}'
                                    }
                                }
                            }
                        ),
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
                                            'description': 'Authentication token for accessing customer service'
                                        }
                                    },
                                    'required': ['orderId', 'session_id', 'user_id', 'token']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Payment confirmed, order updated, and stock adjusted',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Payment confirmed, order updated, and stock adjusted'
                                    }
                                }
                            }
                        ),
                        '400': error_response(
                            'Error in payment verification or updating order/inventory',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 400
                                    },
                                    'message': {
                                        'type': 'string',
                                        'examples': [
                                            'Error verifying payment status',
                                            'Payment not completed',
                                            'Error updating order payment status',
                                            'Error fetching order details',
                                            'Invalid order data received',
                                            'Error updating stock for {item name}'
                                        ]
                                    }
                                }
                            }
                        ),
                        '500': error_response(
                            'Internal server error',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 500
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Error processing payment success: {error details}'
                                    }
                                }
                            }
                        )
                    }
                })
            ])
        }
    }