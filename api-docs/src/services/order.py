"""Order Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Order service."""
    return {
        'tags': [
            {
                'name': 'Order',
                'description': 'Operations for managing orders',
                'x-displayName': 'Order'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Order Service',
                'tags': ['Order']
            }
        ],
        'paths': {
            '/api/orders/inventory': OrderedDict([
                ('get', {
                    'tags': ['Order'],
                    'operationId': 'getInventory',
                    'summary': 'Get inventory',
                    'description': 'Fetch inventory data from the Inventory Microservice',
                    'responses': {
                        '200': success_response('Inventory data retrieved successfully'),
                        '500': error_response('Error fetching inventory')
                    }
                })
            ]),
            '/api/orders/place': OrderedDict([
                ('post', {
                    'tags': ['Order'],
                    'operationId': 'placeOrder',
                    'summary': 'Place order',
                    'description': 'Create a new order in the system',
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
                                            'description': 'List of items in the order',
                                            'items': {
                                                'type': 'object'
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
                            'Order placed successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'orderId': {
                                        'type': 'string',
                                        'description': 'Created order ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Missing required fields'),
                        '500': error_response('Error placing order')
                    }
                })
            ]),
            '/api/orders/update-payment': OrderedDict([
                ('post', {
                    'tags': ['Order'],
                    'operationId': 'updatePayment',
                    'summary': 'Update payment',
                    'description': 'Update order with payment intent ID and mark as paid',
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
                                        'paymentIntentId': {
                                            'type': 'string',
                                            'description': 'Stripe payment intent ID'
                                        }
                                    },
                                    'required': ['orderId', 'paymentIntentId']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Order updated as paid'),
                        '400': error_response('Missing required fields'),
                        '500': error_response('Error updating order')
                    }
                })
            ]),
            '/api/orders/{order_id}': OrderedDict([
                ('get', {
                    'tags': ['Order'],
                    'operationId': 'getOrder',
                    'summary': 'Get order',
                    'description': 'Get order details by ID',
                    'parameters': [
                        {
                            'name': 'order_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Order ID'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Order details retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'data': {
                                        'type': 'object',
                                        'description': 'Order details'
                                    }
                                }
                            }
                        ),
                        '404': error_response('Order not found'),
                        '500': error_response('Error fetching order')
                    }
                }),
                ('patch', {
                    'tags': ['Order'],
                    'operationId': 'updateOrder',
                    'summary': 'Update order',
                    'description': 'Update order details',
                    'parameters': [
                        {
                            'name': 'order_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Order ID'
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'description': 'Fields to update'
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response('Order updated successfully'),
                        '404': error_response('Order not found'),
                        '500': error_response('Error updating order')
                    }
                })
            ]),
            '/api/orders': OrderedDict([
                ('post', {
                    'tags': ['Order'],
                    'operationId': 'getOrders',
                    'summary': 'Get multiple orders',
                    'description': 'Get multiple orders by their IDs',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'order_ids': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string'
                                            },
                                            'description': 'List of order IDs'
                                        }
                                    },
                                    'required': ['order_ids']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Orders retrieved successfully',
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'order_id': {
                                            'type': 'string',
                                            'description': 'Order ID'
                                        },
                                        'data': {
                                            'type': 'object',
                                            'description': 'Order details'
                                        }
                                    }
                                }
                            }
                        ),
                        '400': error_response('No order_ids provided'),
                        '500': error_response('Error fetching orders')
                    }
                })
            ]),
            '/api/orders/{order_id}/update-status': OrderedDict([
                ('put', {
                    'tags': ['Order'],
                    'operationId': 'updateOrderStatus',
                    'summary': 'Update order status',
                    'description': 'Update the status of an order',
                    'parameters': [
                        {
                            'name': 'order_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Order ID'
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'status': {
                                            'type': 'string',
                                            'description': 'New order status'
                                        }
                                    },
                                    'required': ['status']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Order status updated successfully'),
                        '400': error_response('Missing status field'),
                        '404': error_response('Order not found'),
                        '500': error_response('Error updating order status')
                    }
                })
            ]),
            '/api/orders/customer/{customer_id}': OrderedDict([
                ('get', {
                    'tags': ['Order'],
                    'operationId': 'getOrdersByCustomer',
                    'summary': 'Get customer orders',
                    'description': 'Get all orders for a specific customer',
                    'parameters': [
                        {
                            'name': 'customer_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Customer ID'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Orders retrieved successfully',
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'description': 'Order details'
                                }
                            }
                        ),
                        '404': error_response('No orders found for this customer'),
                        '500': error_response('Error fetching orders')
                    }
                })
            ]),
            '/api/orders/cleanup': OrderedDict([
                ('delete', {
                    'tags': ['Order'],
                    'operationId': 'cleanupUnpaidOrders',
                    'summary': 'Cleanup unpaid orders',
                    'description': 'Delete pending orders older than 3 minutes',
                    'responses': {
                        '200': success_response(
                            'Cleanup completed successfully',
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'description': 'Deleted order ID'
                                }
                            }
                        ),
                        '500': error_response('Error during cleanup')
                    }
                })
            ])
        }
    } 