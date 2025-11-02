"""
Request validation helpers
Implements validation logic separate from routes
Improves code reusability and testability
"""

from typing import Optional, Tuple, Any
from flask import Request


class RequestValidator:
    """
    Validates HTTP request data.
    Centralizes validation logic for reusability.
    """
    
    @staticmethod
    def validate_json(request: Request) -> Tuple[Optional[dict], Optional[str]]:
        """
        Validate that request contains JSON data.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (data, error_message)
            If error_message is not None, validation failed
        """
        data = request.get_json()
        
        if not data:
            return None, 'No JSON data provided'
        
        return data, None
    
    @staticmethod
    def validate_required_fields(data: dict, *fields: str) -> Optional[str]:
        """
        Validate that required fields are present in data.
        
        Args:
            data: Dictionary to validate
            *fields: Field names to check
            
        Returns:
            Error message if validation fails, None otherwise
        """
        missing = [f for f in fields if not data.get(f)]
        
        if missing:
            return f'Missing required field(s): {", ".join(missing)}'
        
        return None
    
    @staticmethod
    def validate_optional_field(
        data: dict,
        field: str,
        valid_values: list
    ) -> Tuple[Any, Optional[str]]:
        """
        Validate an optional field against a list of valid values.
        
        Args:
            data: Dictionary containing the field
            field: Field name to validate
            valid_values: List of acceptable values
            
        Returns:
            Tuple of (value, error_message)
        """
        if field not in data:
            return None, None
        
        value = data[field]
        
        if value not in valid_values:
            return None, f'Invalid {field}. Must be one of: {", ".join(map(str, valid_values))}'
        
        return value, None


class ErrorResponse:
    """
    Standardized error response builder.
    Ensures consistent error formatting across the API.
    """
    
    @staticmethod
    def unauthorized(message: str = 'Unauthorized') -> Tuple[dict, int]:
        """Return 403 Unauthorized response"""
        return {'error': message}, 403
    
    @staticmethod
    def not_authenticated(message: str = 'Not authenticated') -> Tuple[dict, int]:
        """Return 401 Not Authenticated response"""
        return {'error': message}, 401
    
    @staticmethod
    def not_found(message: str = 'Resource not found') -> Tuple[dict, int]:
        """Return 404 Not Found response"""
        return {'error': message}, 404
    
    @staticmethod
    def bad_request(message: str) -> Tuple[dict, int]:
        """Return 400 Bad Request response"""
        return {'error': message}, 400
    
    @staticmethod
    def success(data: Any, status_code: int = 200) -> Tuple[Any, int]:
        """Return success response with data"""
        return data, status_code


class SuccessResponse:
    """
    Standardized success response builder.
    """
    
    @staticmethod
    def created(data: Any) -> Tuple[Any, int]:
        """Return 201 Created response"""
        return data, 201
    
    @staticmethod
    def ok(data: Any) -> Tuple[Any, int]:
        """Return 200 OK response"""
        return data, 200
    
    @staticmethod
    def message(text: str, status_code: int = 200) -> Tuple[dict, int]:
        """Return simple message response"""
        return {'message': text}, status_code
