"""
Created on: 6-8-2021 15:38

@author: IvS
"""

from pydsol.model.basic_logger import get_module_logger

logger = get_module_logger(__name__)

__all__ = ["QueueModel"]

class QueueModel(object):
    """This class defines a basic queue attached to a specific object for a discrete event simulation model,
    and keeps track of the objects in the queue with a contents list."""
    def __init__(self, attached_to):
        """

        Parameters
        ----------
        attached_to: object
            object where the queue is attached to, for example a Server.
        """
        self.attached_to = attached_to
        self.contents = []
