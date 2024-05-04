from dataclasses import dataclass
from enum import Enum, auto



class Grouping(Enum):
    FILELIST = auto()
    LIST = auto()
    DATASET = auto()

@dataclass
class User:
    username: str
    password: str
    # Add more fields as needed

