"""Customer Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Customer service."""
    return {
        'tags': [
            {
                'name': 'Customer',
                'description': 'Operations for managing customers',
                'x-displayName': 'Customer'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Customer Service',
                'tags': ['Customer']
            }
        ],
        'paths': {
            '/customers': OrderedDict([
                ('post', {
                    'tags': ['Customer'],
                    'operationId': 'createCustomer',
                    'summary': 'Create customer',
                    'description': 'Create a new customer account',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {
                                            'type': 'string',
                                            'description': 'Customer name'
                                        },
                                        'email': {
                                            'type': 'string',
                                            'format': 'email',
                                            'description': 'Customer email address'
                                        },
                                        'phone': {
                                            'type': 'string',
                                            'description': 'Customer phone number'
                                        },
                                        'address': {
                                            'type': 'string',
                                            'description': 'Customer delivery address'
                                        }
                                    },
                                    'required': ['name', 'email']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response(
                            'Customer created successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'customer_id': {
                                        'type': 'string',
                                        'description': 'Created customer ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Invalid request data'),
                        '409': error_response('Customer with email already exists'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('get', {
                    'tags': ['Customer'],
                    'operationId': 'listCustomers',
                    'summary': 'List customers',
                    'description': 'Get a list of all customers',
                    'parameters': [
                        {
                            'name': 'page',
                            'in': 'query',
                            'schema': {'type': 'integer', 'default': 1},
                            'description': 'Page number for pagination'
                        },
                        {
                            'name': 'limit',
                            'in': 'query',
                            'schema': {'type': 'integer', 'default': 10},
                            'description': 'Number of items per page'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Customers retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'customers': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'customer_id': {
                                                    'type': 'string',
                                                    'description': 'Customer ID'
                                                },
                                                'name': {
                                                    'type': 'string',
                                                    'description': 'Customer name'
                                                },
                                                'email': {
                                                    'type': 'string',
                                                    'description': 'Customer email'
                                                },
                                                'created_at': {
                                                    'type': 'string',
                                                    'format': 'date-time',
                                                    'description': 'Account creation timestamp'
                                                }
                                            }
                                        }
                                    },
                                    'total': {
                                        'type': 'integer',
                                        'description': 'Total number of customers'
                                    },
                                    'page': {
                                        'type': 'integer',
                                        'description': 'Current page number'
                                    },
                                    'total_pages': {
                                        'type': 'integer',
                                        'description': 'Total number of pages'
                                    }
                                }
                            }
                        ),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/customers/{customer_id}': OrderedDict([
                ('get', {
                    'tags': ['Customer'],
                    'operationId': 'getCustomer',
                    'summary': 'Get customer',
                    'description': 'Get customer details by ID',
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
                            'Customer details retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'customer_id': {
                                        'type': 'string',
                                        'description': 'Customer ID'
                                    },
                                    'name': {
                                        'type': 'string',
                                        'description': 'Customer name'
                                    },
                                    'email': {
                                        'type': 'string',
                                        'description': 'Customer email'
                                    },
                                    'phone': {
                                        'type': 'string',
                                        'description': 'Customer phone number'
                                    },
                                    'address': {
                                        'type': 'string',
                                        'description': 'Customer delivery address'
                                    },
                                    'created_at': {
                                        'type': 'string',
                                        'format': 'date-time',
                                        'description': 'Account creation timestamp'
                                    }
                                }
                            }
                        ),
                        '404': error_response('Customer not found'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('put', {
                    'tags': ['Customer'],
                    'operationId': 'updateCustomer',
                    'summary': 'Update customer',
                    'description': 'Update customer details',
                    'parameters': [
                        {
                            'name': 'customer_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Customer ID'
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {
                                            'type': 'string',
                                            'description': 'Customer name'
                                        },
                                        'email': {
                                            'type': 'string',
                                            'format': 'email',
                                            'description': 'Customer email address'
                                        },
                                        'phone': {
                                            'type': 'string',
                                            'description': 'Customer phone number'
                                        },
                                        'address': {
                                            'type': 'string',
                                            'description': 'Customer delivery address'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Customer updated successfully'),
                        '400': error_response('Invalid request data'),
                        '404': error_response('Customer not found'),
                        '409': error_response('Email already in use'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('delete', {
                    'tags': ['Customer'],
                    'operationId': 'deleteCustomer',
                    'summary': 'Delete customer',
                    'description': 'Delete a customer account',
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
                        '200': success_response('Customer deleted successfully'),
                        '404': error_response('Customer not found'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    } 