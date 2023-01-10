from abc import ABC, abstractmethod
from rest_framework.response import Response


class RespnseMessage(ABC):
    def __init__(self, message, status):
        self.message = message
        self.status = status

    @abstractmethod
    def SendResposne(self):
        pass
