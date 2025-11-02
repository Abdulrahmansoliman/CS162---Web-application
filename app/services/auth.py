"""
Authentication Service Module

DESIGN PATTERN: Strategy Pattern
Demonstrates POLYMORPHISM through different authentication strategies.

POLYMORPHISM EXPLANATION:
Different authentication methods (Local, OAuth, LDAP, etc.) can be implemented
as separate strategy classes. All strategies inherit from AuthenticationStrategy
and must implement the authenticate() method.

The AuthenticationService doesn't care WHICH strategy is used - it just calls
authenticate(). This is polymorphism in action: same interface, different behaviors.

BENEFITS:
1. OPEN/CLOSED PRINCIPLE: Open for extension (add new strategies),
   closed for modification (don't change AuthenticationService)
2. SINGLE RESPONSIBILITY: Each strategy handles one authentication method
3. TESTABILITY: Easy to mock strategies for testing
4. FLEXIBILITY: Can switch strategies at runtime

ABSTRACTION:
Routes don't know HOW authentication works, they just call auth_service.authenticate().
The complexity is abstracted away.
"""

from abc import ABC, abstractmethod
from models import db, User
from flask import session


class AuthenticationStrategy(ABC):
    """
    Abstract base class for authentication strategies.
    
    ABSTRACTION: Defines the interface all strategies must implement
    POLYMORPHISM: Different strategies = different implementations
    
    This is an ABSTRACT CLASS because:
    1. It cannot be instantiated directly
    2. Subclasses MUST implement authenticate()
    3. Provides a contract that all strategies follow
    """
    
    @abstractmethod
    def authenticate(self, **kwargs):
        """
        Authenticate user based on strategy-specific parameters.
        
        ABSTRACTION: Caller doesn't need to know implementation details
        POLYMORPHISM: Different strategies implement this differently
        
        Returns:
            User object if successful, None if authentication fails
        """
        pass


class LocalAuthStrategy(AuthenticationStrategy):
    """
    Local authentication strategy (username/password).
    
    POLYMORPHISM EXAMPLE:
    This class INHERITS from AuthenticationStrategy and provides
    its OWN implementation of authenticate().
    
    Other strategies could be:
      - OAuthStrategy: Authenticate via Google/GitHub
      - LDAPStrategy: Authenticate via LDAP server
      - TokenStrategy: Authenticate via JWT token
    
    All would inherit from AuthenticationStrategy and implement authenticate()
    differently, but AuthenticationService treats them all the same way.
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
    
    STRATEGY PATTERN IMPLEMENTATION:
    This class delegates authentication to a strategy object.
    It doesn't know HOW authentication works, just asks the strategy to do it.
    
    POLYMORPHISM IN ACTION:
    self._strategy can be ANY class that inherits from AuthenticationStrategy.
    Could be LocalAuthStrategy, OAuthStrategy, LDAPStrategy, etc.
    The service treats them all the same way.
    
    BENEFITS:
    1. FLEXIBILITY: Change authentication method without changing this class
    2. TESTABILITY: Easy to mock strategies for testing
    3. EXTENSIBILITY: Add new auth methods without modifying existing code
    
    ABSTRACTION:
    Routes call auth_service.authenticate() - they don't know about strategies.
    """
    
    def __init__(self, strategy: AuthenticationStrategy):
        """
        Initialize service with an authentication strategy.
        
        DEPENDENCY INJECTION:
        Strategy is passed in, not created here.
        This makes the class more flexible and testable.
        
        Args:
            strategy: Any object implementing AuthenticationStrategy interface
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: AuthenticationStrategy):
        """
        Change authentication strategy at runtime.
        
        POLYMORPHISM:
        Can swap strategies without changing client code.
        Example: Switch from LocalAuth to OAuth without restarting server.
        
        Args:
            strategy: New authentication strategy to use
        """
        self._strategy = strategy
    
    def authenticate(self, **kwargs):
        """
        Authenticate user using current strategy.
        
        ABSTRACTION:
        This method hides which strategy is being used.
        Caller just passes credentials, doesn't care how they're checked.
        
        POLYMORPHISM:
        self._strategy.authenticate() might call:
          - LocalAuthStrategy.authenticate()
          - OAuthStrategy.authenticate()
          - LDAPStrategy.authenticate()
        But this method treats them all the same.
        
        Args:
            **kwargs: Strategy-specific authentication parameters
            
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
