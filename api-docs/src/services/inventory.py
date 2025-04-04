"""Inventory Service API specification."""

from collections import OrderedDict
from schemas.common import error_response, success_response

def get_specification():
    """Return the OpenAPI specification for the Inventory service."""
    return {
        'tags': [
            {
                'name': 'Inventory',
                'description': 'Operations for managing meal kit inventory',
                'x-displayName': 'Inventory'
            }
        ],
        'x-tagGroups': [
            {
                'name': 'Inventory Service',
                'tags': ['Inventory']
            }
        ],
        'paths': {
            '/inventory': OrderedDict([
                ('post', {
                    'tags': ['Inventory'],
                    'operationId': 'addMealKit',
                    'summary': 'Add meal kit',
                    'description': 'Add a new meal kit to the inventory',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {
                                            'type': 'string',
                                            'description': 'Name of the meal kit'
                                        },
                                        'ingredients': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string'
                                            },
                                            'description': 'List of ingredients'
                                        },
                                        'stock': {
                                            'type': 'integer',
                                            'description': 'Available stock quantity'
                                        },
                                        'price': {
                                            'type': 'number',
                                            'format': 'float',
                                            'description': 'Price of the meal kit'
                                        }
                                    },
                                    'required': ['name', 'ingredients', 'stock', 'price']
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response('Meal kit added successfully'),
                        '400': error_response('Missing required fields'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('get', {
                    'tags': ['Inventory'],
                    'operationId': 'getInventory',
                    'summary': 'List meal kits',
                    'description': 'Get a list of all meal kits in the inventory',
                    'responses': {
                        '200': success_response(
                            'Meal kits retrieved successfully',
                            {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {
                                            'type': 'string',
                                            'description': 'Meal kit ID'
                                        },
                                        'name': {
                                            'type': 'string',
                                            'description': 'Name of the meal kit'
                                        },
                                        'description': {
                                            'type': 'string',
                                            'description': 'Description of the meal kit'
                                        },
                                        'dietaryTags': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string'
                                            },
                                            'description': 'Dietary tags (e.g., vegetarian, gluten-free)'
                                        },
                                        'imageURL': {
                                            'type': 'string',
                                            'description': 'URL of the meal kit image'
                                        },
                                        'ingredients': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'string'
                                            },
                                            'description': 'List of ingredients'
                                        },
                                        'isAvailable': {
                                            'type': 'boolean',
                                            'description': 'Whether the meal kit is available'
                                        },
                                        'numAvailable': {
                                            'type': 'integer',
                                            'description': 'Number of units available'
                                        },
                                        'nutritionalInfo': {
                                            'type': 'object',
                                            'description': 'Nutritional information'
                                        },
                                        'preparationTime': {
                                            'type': 'integer',
                                            'description': 'Preparation time in minutes'
                                        },
                                        'price': {
                                            'type': 'number',
                                            'format': 'float',
                                            'description': 'Price of the meal kit'
                                        },
                                        'servings': {
                                            'type': 'integer',
                                            'description': 'Number of servings'
                                        }
                                    }
                                }
                            }
                        ),
                        '404': error_response('No meal kits available'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/inventory/mass_upload': OrderedDict([
                ('post', {
                    'tags': ['Inventory'],
                    'operationId': 'massUpload',
                    'summary': 'Mass upload meal kits',
                    'description': 'Upload multiple meal kits using a CSV or Excel file',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'multipart/form-data': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'file': {
                                            'type': 'string',
                                            'format': 'binary',
                                            'description': 'CSV or Excel file containing meal kit data'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'responses': {
                        '201': success_response('Meal kits uploaded successfully'),
                        '400': error_response('Invalid file format or missing file'),
                        '500': error_response('Internal server error')
                    }
                })
            ]),
            '/inventory/{kit_id}': OrderedDict([
                ('get', {
                    'tags': ['Inventory'],
                    'operationId': 'getMealKit',
                    'summary': 'Get meal kit',
                    'description': 'Get details of a specific meal kit',
                    'parameters': [
                        {
                            'name': 'kit_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Meal kit ID'
                        }
                    ],
                    'responses': {
                        '200': success_response(
                            'Meal kit retrieved successfully',
                            {
                                'type': 'object',
                                'properties': {
                                    'id': {
                                        'type': 'string',
                                        'description': 'Meal kit ID'
                                    },
                                    'name': {
                                        'type': 'string',
                                        'description': 'Name of the meal kit'
                                    },
                                    'description': {
                                        'type': 'string',
                                        'description': 'Description of the meal kit'
                                    },
                                    'dietaryTags': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'string'
                                        },
                                        'description': 'Dietary tags (e.g., vegetarian, gluten-free)'
                                    },
                                    'imageURL': {
                                        'type': 'string',
                                        'description': 'URL of the meal kit image'
                                    },
                                    'ingredients': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'string'
                                        },
                                        'description': 'List of ingredients'
                                    },
                                    'isAvailable': {
                                        'type': 'boolean',
                                        'description': 'Whether the meal kit is available'
                                    },
                                    'numAvailable': {
                                        'type': 'integer',
                                        'description': 'Number of units available'
                                    },
                                    'nutritionalInfo': {
                                        'type': 'object',
                                        'description': 'Nutritional information'
                                    },
                                    'preparationTime': {
                                        'type': 'integer',
                                        'description': 'Preparation time in minutes'
                                    },
                                    'price': {
                                        'type': 'number',
                                        'format': 'float',
                                        'description': 'Price of the meal kit'
                                    },
                                    'servings': {
                                        'type': 'integer',
                                        'description': 'Number of servings'
                                    }
                                }
                            }
                        ),
                        '404': error_response('Meal kit not found'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('put', {
                    'tags': ['Inventory'],
                    'operationId': 'updateStock',
                    'summary': 'Update stock',
                    'description': 'Update the stock quantity of a meal kit',
                    'parameters': [
                        {
                            'name': 'kit_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Meal kit ID'
                        }
                    ],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'stock': {
                                            'type': 'integer',
                                            'description': 'New stock quantity'
                                        }
                                    },
                                    'required': ['stock']
                                }
                            }
                        }
                    },
                    'responses': {
                        '200': success_response('Stock updated successfully'),
                        '400': error_response('Missing stock field'),
                        '404': error_response('Meal kit not found'),
                        '500': error_response('Internal server error')
                    }
                }),
                ('delete', {
                    'tags': ['Inventory'],
                    'operationId': 'deleteMealKit',
                    'summary': 'Delete meal kit',
                    'description': 'Delete a meal kit from the inventory',
                    'parameters': [
                        {
                            'name': 'kit_id',
                            'in': 'path',
                            'required': True,
                            'schema': {'type': 'string'},
                            'description': 'Meal kit ID'
                        }
                    ],
                    'responses': {
                        '200': success_response('Meal kit deleted successfully'),
                        '404': error_response('Meal kit not found'),
                        '500': error_response('Internal server error')
                    }
                })
            ])
        }
    } 