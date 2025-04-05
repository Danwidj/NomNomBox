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
            },
            {
                'name': 'Authentication',
                'description': 'Operations for user authentication',
                'x-displayName': 'Authentication'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Customer Service',
                'tags': ['Customer', 'Authentication']
            }
        ],
        'paths': {
            '/register': {
                'post': {
                    'tags': ['Authentication'],
                    'operationId': 'registerUser',
                    'summary': 'Register user',
                    'description': 'Register a new user account',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'email': {
                                            'type': 'string',
                                            'format': 'email',
                                            'description': 'User email address'
                                        },
                                        'password': {
                                            'type': 'string',
                                            'format': 'password',
                                            'description': 'User password'
                                        },
                                        'name': {
                                            'type': 'string',
                                            'description': 'User full name'
                                        },
                                        'address': {
                                            'type': 'string',
                                            'description': 'User address'
                                        },
                                        'phone': {
                                            'type': 'string',
                                            'description': 'User phone number'
                                        },
                                        'dietary_preferences': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string'
                                            },
                                            'description': 'User dietary preferences'
                                        }
                                    },
                                    'required': ['email', 'password', 'name']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response(
                            'User registered successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 201
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'User registered'
                                    },
                                    'uid': {
                                        'type': 'string',
                                        'description': 'Firebase user ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Missing required fields or email already exists'),
                        '500': error_response('Internal server error')
                    }
                }
            },
            '/login': {
                'post': {
                    'tags': ['Authentication'],
                    'operationId': 'loginUser',
                    'summary': 'Login user',
                    'description': 'Authenticate user and return access token',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'email': {
                                            'type': 'string',
                                            'format': 'email',
                                            'description': 'User email address'
                                        },
                                        'password': {
                                            'type': 'string',
                                            'format': 'password',
                                            'description': 'User password'
                                        }
                                    },
                                    'required': ['email', 'password']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Login successful',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Login successful'
                                    },
                                    'token': {
                                        'type': 'string',
                                        'description': 'Firebase ID token'
                                    },
                                    'id': {
                                        'type': 'string',
                                        'description': 'Firebase user ID'
                                    }
                                }
                            }
                        ),
                        '400': error_response('Email and password required'),
                        '401': error_response('Invalid credentials'),
                        '500': error_response('Internal server error')
                    }
                },
                'options': {
                    'tags': ['Authentication'],
                    'operationId': 'loginOptions',
                    'summary': 'CORS preflight for login',
                    'description': 'Handles CORS preflight OPTIONS request for the login endpoint',
                    'responses': {
                        '200': success_response('OK')
                    }
                }
            },
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
            '/customer': {
                'get': {
                    'tags': ['Customer'],
                    'operationId': 'getAllCustomers',
                    'summary': 'Get all customers',
                    'description': 'Get a list of all customers without pagination',
                    'responses': {
                        '200': success_response(
                            'Customers retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'data': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {
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
                                                'address': {
                                                    'type': 'string',
                                                    'description': 'Customer address'
                                                },
                                                'phone': {
                                                    'type': 'string',
                                                    'description': 'Customer phone'
                                                },
                                                'dietary_preferences': {
                                                    'type': 'array',
                                                    'items': {
                                                        'type': 'string'
                                                    },
                                                    'description': 'Customer dietary preferences'
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '404': error_response('No customers found'),
                        '500': error_response('Internal server error')
                    }
                }
            },
            '/customer/{customer_id}': {
                'get': {
                    'tags': ['Customer'],
                    'operationId': 'getCustomerById',
                    'summary': 'Get customer',
                    'description': 'Get customer details by ID (requires authentication)',
                    'security': [
                        {
                            'bearerAuth': []
                        }
                    ],
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
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'customerId': {
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
                                            'dietary_preferences': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'string'
                                                },
                                                'description': 'Customer dietary preferences'
                                            }
                                        }
                                    }
                                }
                            }
                        ),
                        '401': error_response('Unauthorized - Invalid or missing token'),
                        '404': error_response('Customer not found'),
                        '500': error_response('Internal server error')
                    }
                },
                'put': {
                    'tags': ['Customer'],
                    'operationId': 'updateCustomer',
                    'summary': 'Update customer',
                    'description': 'Update customer details (requires authentication)',
                    'security': [
                        {
                            'bearerAuth': []
                        }
                    ],
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
                                        },
                                        'dietary_preferences': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string'
                                            },
                                            'description': 'Customer dietary preferences'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response(
                            'Customer updated successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Customer updated'
                                    }
                                }
                            }
                        ),
                        '401': error_response('Unauthorized - Invalid or missing token'),
                        '404': error_response('Customer not found'),
                        '500': error_response('Internal server error')
                    }
                },
                'delete': {
                    'tags': ['Customer'],
                    'operationId': 'deleteCustomer',
                    'summary': 'Delete customer',
                    'description': 'Delete a customer account (requires authentication)',
                    'security': [
                        {
                            'bearerAuth': []
                        }
                    ],
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
                            'Customer deleted successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'code': {
                                        'type': 'integer',
                                        'example': 200
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Customer deleted'
                                    }
                                }
                            }
                        ),
                        '401': error_response('Unauthorized - Invalid or missing token'),
                        '404': error_response('Customer not found'),
                        '500': error_response('Internal server error')
                    }
                }
            }
        },
        'components': {
            'securitySchemes': {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT',
                    'description': 'Firebase Authentication JWT token'
                }
            }
        }
    }