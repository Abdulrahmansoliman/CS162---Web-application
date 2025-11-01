"""
Authentication service module
Implements Strategy pattern for different authentication strategies
"""

from abc import ABC, abstractmethod
from models import db, User
from flask import session


class AuthenticationStrategy(ABC):
    """
    Abstract base class for authentication strategies.
    
    Strategy Pattern: Defines different ways to authenticate users.
    This allows different authentication methods without changing client code.
    """
    
    @abstractmethod
    def authenticate(self, **kwargs):
        """Authenticate user based on strategy"""
        pass


class LocalAuthStrategy(AuthenticationStrategy):
    """
    Local authentication strategy (username/password).
    
    Implements local user authentication with database lookup
    and password verification.
    """
    
    def authenticate(self, username, password):
        """
        Authenticate user with username and password.
        
        Args:
            username: User's username
            password: User's password (plaintext)
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            return None
        
        if not user.check_password(password):
            return None
        
        return user


class AuthenticationService:
    """
    Authentication service using Strategy pattern.
    
    Delegates authentication to different strategies based on method.
    This allows easy addition of new authentication methods (OAuth, LDAP, etc).
    """
    
    def __init__(self, strategy: AuthenticationStrategy):
        """
        Initialize service with authentication strategy.
        
        Args:
            strategy: AuthenticationStrategy implementation
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: AuthenticationStrategy):
        """
        Change authentication strategy at runtime.
        
        Args:
            strategy: New AuthenticationStrategy implementation
        """
        self._strategy = strategy
    
    def authenticate(self, **kwargs):
        """
        Authenticate user using current strategy.
        
        Args:
            **kwargs: Strategy-specific parameters
            
        Returns:
            User object if successful, None otherwise
        """
        return self._strategy.authenticate(**kwargs)
    
    def register_user(self, username, email, password):
        """
        Register a new user.
        
        Args:
            username: Unique username
            email: User email
            password: Password (will be hashed)
            
        Returns:
            User object if successful, None if user exists
        """
        # Check if user already exists
        existing = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing:
            return None
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def create_session(self, user):
        """
        Create session for authenticated user.
        
        Args:
            user: User object
        """
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = True
    
    def destroy_session(self):
        """Destroy current user session"""
        session.clear()
    
    @staticmethod
    def get_current_user():
        """
        Get currently authenticated user from session.
        
        Returns:
            User object or None if not authenticated
        """
        user_id = session.get('user_id')
        
        if user_id is None:
            return None
        
        return User.query.get(user_id)


# Create default authentication service
auth_service = AuthenticationService(LocalAuthStrategy())
