"""
doubly_linked_list.py

This module provides the implementation of a doubly linked list data structure. 
It includes the following classes:

Classes:
    Node: A class representing a node in the doubly linked list, which stores 
          a value and references to the next and previous nodes.
    DoublyLinkedList: A class representing the doubly linked list, with methods 
                      for adding and removing nodes from the head and tail, 
                      removing nodes by value, and creating a string 
                      representation of the list.

Usage:
    # Example of creating a doubly linked list and performing operations
    dll = DoublyLinkedList()
    dll.add_to_head(1)
    dll.add_to_tail(2)
    dll.add_to_head(0)
    print(dll.stringify_list())  # Output: "0\n1\n2\n"
    dll.remove_by_value(1)
    print(dll.stringify_list())  # Output: "0\n2\n"
    
This module demonstrates key concepts of linked lists, including traversal, 
node insertion, and node deletion.

"""


class Node:
    """
    Represents a node in a doubly linked list.

    Attributes:
        value: The value stored in the node.
        next_node: Reference to the next node in the list.
        prev_node: Reference to the previous node in the list.
    """

    def __init__(self, value, next_node=None, prev_node=None):
        """
        Initializes a new node with a value, and optional references to the next and previous nodes.

        Args:
            value: The value to store in the node.
            next_node: Reference to the next node in the list (default is None).
            prev_node: Reference to the previous node in the list (default is None).
        """
        self.value = value
        self.next_node = next_node
        self.prev_node = prev_node

    def set_next_node(self, next_node):
        """
        Sets the reference to the next node.

        Args:
            next_node: The node to set as the next node.
        """
        self.next_node = next_node

    def get_next_node(self):
        """
        Returns the next node in the list.

        Returns:
            The next node in the list.
        """
        return self.next_node

    def set_prev_node(self, prev_node):
        """
        Sets the reference to the previous node.

        Args:
            prev_node: The node to set as the previous node.
        """
        self.prev_node = prev_node

    def get_prev_node(self):
        """
        Returns the previous node in the list.

        Returns:
            The previous node in the list.
        """
        return self.prev_node

    def get_value(self):
        """
        Returns the value stored in the node.

        Returns:
            The value stored in the node.
        """
        return self.value


class DoublyLinkedList:
    """
    Represents a doubly linked list.

    Attributes:
        head_node: The head node of the list.
        tail_node: The tail node of the list.
    """

    def __init__(self):
        """
        Initializes an empty doubly linked list.
        """
        self.head_node = None
        self.tail_node = None

    def add_to_head(self, new_value):
        """
        Adds a new node with the given value to the head of the list.

        Args:
            new_value: The value to add to the head of the list.
        """
        new_head = Node(new_value)
        current_head = self.head_node

        if current_head is not None:
            current_head.set_prev_node(new_head)
            new_head.set_next_node(current_head)

        self.head_node = new_head

        if self.tail_node is None:
            self.tail_node = new_head

    def add_to_tail(self, new_value):
        """
        Adds a new node with the given value to the tail of the list.

        Args:
            new_value: The value to add to the tail of the list.
        """
        new_tail = Node(new_value)
        current_tail = self.tail_node

        if current_tail is not None:
            current_tail.set_next_node(new_tail)
            new_tail.set_prev_node(current_tail)

        self.tail_node = new_tail

        if self.head_node is None:
            self.head_node = new_tail

    def remove_head(self):
        """
        Removes the head node of the list.

        Returns:
            The value of the removed head node, or None if the list is empty.
        """
        removed_head = self.head_node

        if removed_head is None:
            return None

        self.head_node = removed_head.get_next_node()

        if self.head_node is not None:
            self.head_node.set_prev_node(None)

        if removed_head == self.tail_node:
            self.remove_tail()

        return removed_head.get_value()

    def remove_tail(self):
        """
        Removes the tail node of the list.

        Returns:
            The value of the removed tail node, or None if the list is empty.
        """
        removed_tail = self.tail_node

        if removed_tail is None:
            return None

        self.tail_node = removed_tail.get_prev_node()

        if self.tail_node is not None:
            self.tail_node.set_next_node(None)

        if removed_tail == self.head_node:
            self.remove_head()

        return removed_tail.get_value()

    def remove_by_value(self, value_to_remove):
        """
        Removes the first node in the list that has the given value.

        Args:
            value_to_remove: The value to remove from the list.

        Returns:
            The value of the removed node, or None if the value was not found.
        """
        node_to_remove = None
        current_node = self.head_node

        while current_node:
            if current_node.get_value() == value_to_remove:
                node_to_remove = current_node
                break

            current_node = current_node.get_next_node()

        if node_to_remove is None:
            return None

        if node_to_remove == self.head_node:
            self.remove_head()

        elif node_to_remove == self.tail_node:
            self.remove_tail()

        else:
            next_node = node_to_remove.get_next_node()
            prev_node = node_to_remove.get_prev_node()

            next_node.set_prev_node(prev_node)
            prev_node.set_next_node(next_node)

        return node_to_remove.get_value()

    def stringify_list(self):
        """
        Creates a string representation of the list.

        Returns:
            A string containing the values of the list, separated by newlines.
        """
        string_list = ""
        current_node = self.head_node

        while current_node:
            if current_node.get_value() is not None:
                string_list += str(current_node.get_value()) + "\n"

            current_node = current_node.get_next_node()

        return string_list
