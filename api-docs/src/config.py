"""Configuration settings for API documentation."""

# Service URLs and ports
SERVICES = {
    'chat_history': {
        'url': 'http://localhost:5012',
        'description': 'Chat History Service'
    },
    'customer': {
        'url': 'http://localhost:5002',
        'description': 'Customer Service'
    },
    'delivery': {
        'url': 'http://localhost:5000',
        'description': 'Delivery Service'
    },
    'gemini': {
        'url': 'http://localhost:5009',
        'description': 'Gemini AI Recommendation Service'
    },
    'inventory': {
        'url': 'http://localhost:5006',
        'description': 'Inventory Management Service'
    },
    'manage_deliveries': {
        'url': 'http://localhost:5000',
        'description': 'Manage Deliveries Service'
    },
    'notifications': {
        'url': 'http://localhost:9000',
        'description': 'Notifications Service'
    },
    'order': {
        'url': 'http://localhost:5003',
        'description': 'Order Service'
    },
    'order_composite': {
        'url': 'http://localhost:5005',
        'description': 'Order Composite Service'
    },
    'payment': {
        'url': 'http://localhost:5004',
        'description': 'Payment Service'
    },
    'schedule': {
        'url': 'http://localhost:5001',
        'description': 'Schedule Service'
    },
    'send_query': {
        'url': 'http://localhost:5100',
        'description': 'Send Query Service'
    }
}

# Swagger UI settings
SWAGGER_UI_CONFIG = {
    'app_name': 'NomNomBox API Documentation',
    'docExpansion': 'list',
    'defaultModelsExpandDepth': 3,
    'defaultModelExpandDepth': 3,
    'supportedSubmitMethods': ['get', 'post', 'put', 'delete'],
    'deepLinking': True,
    'displayOperationId': True
}

# Base OpenAPI specification
BASE_SPEC = {
    'openapi': '3.0.0',
    'info': {
        'title': 'NomNomBox API Documentation',
        'version': '1.0.0',
        'description': '''
API documentation for all NomNomBox microservices.

Available Services (alphabetically):
- Chat History Service (port 5012)
- Customer Service (port 5002)
- Delivery Service (port 5000)
- Gemini AI Service (port 5009)
- Inventory Service (port 5006)
- Manage Deliveries Service (port 5000)
- Notifications Service (port 9000)
- Order Service (port 5003)
- Order Composite Service (port 5005)
- Payment Service (port 5004)
- Schedule Service (port 5001)
- Send Query Service (port 5100)
'''
    },
    'servers': [
        # Servers listed in alphabetical order
        {
            'url': SERVICES['chat_history']['url'],
            'description': SERVICES['chat_history']['description']
        },
        {
            'url': SERVICES['customer']['url'],
            'description': SERVICES['customer']['description']
        },
        {
            'url': SERVICES['delivery']['url'],
            'description': SERVICES['delivery']['description']
        },
        {
            'url': SERVICES['gemini']['url'],
            'description': SERVICES['gemini']['description']
        },
        {
            'url': SERVICES['inventory']['url'],
            'description': SERVICES['inventory']['description']
        },
        {
            'url': SERVICES['manage_deliveries']['url'],
            'description': SERVICES['manage_deliveries']['description']
        },
        {
            'url': SERVICES['notifications']['url'],
            'description': SERVICES['notifications']['description']
        },
        {
            'url': SERVICES['order']['url'],
            'description': SERVICES['order']['description']
        },
        {
            'url': SERVICES['order_composite']['url'],
            'description': SERVICES['order_composite']['description']
        },
        {
            'url': SERVICES['payment']['url'],
            'description': SERVICES['payment']['description']
        },
        {
            'url': SERVICES['schedule']['url'],
            'description': SERVICES['schedule']['description']
        },
        {
            'url': SERVICES['send_query']['url'],
            'description': SERVICES['send_query']['description']
        }
    ],
    'components': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'Firebase Authentication token'
            }
        }
    },
    'security': [
        {'BearerAuth': []}
    ]
} 