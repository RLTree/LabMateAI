# labmateai/models.py
"""
This module defines the SQLAlchemy models for the LabMateAI application.

The models include User, Tool, and Interaction classes to represent users, tools, and interactions between users and tools.

The User class represents a user in the system, including their name, email, department, and role.

The Tool class represents a tool in the system, including its name, category, features, cost, description, URL, language, and platform.

The Interaction class represents an interaction between a user and a tool, including the user ID, tool ID, rating, usage frequency, and timestamp.

These models are used to interact with the database and perform CRUD operations on user, tool, and interaction data.
"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Represents a user in the LabMateAI system.

    Attributes:
        user_id (int): The unique identifier for the user.
        user_name (str): The name of the user.
        email (str): The email address of the user.
        department (str): The department or group the user belongs to.
        role (str): The role or position of the user in the organization.
    """

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department = Column(String(100))
    role = Column(String(50))

    # Relationships
    interactions = relationship("Interaction", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, user_name='{self.user_name}', email='{self.email}')>"


class Tool(Base):
    """
    Represents a tool in the LabMateAI system.

    Attributes:
        tool_id (int): The unique identifier for the tool.
        name (str): The name of the tool.
        category (str): The category or type of the tool.
        features (str): A description of the features or capabilities of the tool.
        cost (str): The cost or pricing model of the tool.
        description (str): A detailed description of the tool.
        url (str): The URL or link to the tool's website or documentation.
        language (str): The programming language(s) the tool is written in or supports.
        platform (str): The operating system or platform the tool is compatible with.
    """

    __tablename__ = 'tools'

    tool_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100))
    features = Column(Text)
    cost = Column(String(50))
    description = Column(Text)
    url = Column(String(255))
    language = Column(String(50))
    platform = Column(String(50))

    # Relationships
    interactions = relationship("Interaction", back_populates="tool")

    def __repr__(self):
        return f"<Tool(tool_id={self.tool_id}, name='{self.name}', category='{self.category}')>"


class Interaction(Base):
    """
    Represents an interaction between a user and a tool in the LabMateAI system.

    Attributes:
        interaction_id (int): The unique identifier for the interaction.
        user_id (int): The ID of the user involved in the interaction.
        tool_id (int): The ID of the tool involved in the interaction.
        rating (int): The user's rating or feedback for the tool.
        usage_frequency (str): The frequency with which the user interacts with the tool.
        timestamp (datetime): The timestamp of the interaction.
    """

    __tablename__ = 'interactions'

    interaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    tool_id = Column(Integer, ForeignKey('tools.tool_id'), nullable=False)
    rating = Column(Integer)
    usage_frequency = Column(String(50))
    timestamp = Column(DateTime, nullable=False)

    # Relationships
    user = relationship("User", back_populates="interactions")
    tool = relationship("Tool", back_populates="interactions")

    def __repr__(self):
        """
        Return a string representation of the Interaction object.
        """
        return f"<Interaction(interaction_id={self.interaction_id}, user_id={self.user_id}, tool_id={self.tool_id}, rating={self.rating})>"
