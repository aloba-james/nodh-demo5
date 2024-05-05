from dataclasses import dataclass, field
from enum import auto, Enum
from typing import List

ID = int

class Grouping(Enum):
    FILELIST = auto()
    LIST = auto()
    DATASET = auto()

class Action(Enum):
    ADD = auto()
    DELETE = auto()

class AuditAction(Enum):
    ACCESS = auto()
    MUTATE = auto()

class ObjectType(Enum):
    RECORDING = auto()
    FILELIST = auto()
    LIST = auto()
    DATASET = auto()

class Mode(Enum):
    FRONTEND = auto()
    LIBRARY = auto()
    CODE = auto()

@dataclass
class User:
    username: str
    password: str

@dataclass
class Group:
    name: str

@dataclass
class EntVersion:
    id: ID
    version_number: int
    grouping: Grouping  # DATASET, FILELIST or LIST
    object_id: ID  # EntDataset, EntFileList or EntList
    created_by: ID
    last_accessed: int
    last_accessed_by: ID
    created_at: int
    description: str
    published: bool

    file_list_tags: List["EntFilelistVersionTag"] = field(default_factory=list, init=False, repr=False)

@dataclass
class EntTag:
    id: ID
    value: str
    description: str
    created_by: ID
    created_at: int

@dataclass
class EntRecording:
    id: ID
    dataset_id: ID  # EntDataset
    parent_id: ID  # EntRecording, this can be None, all augmented recordings will have this field set
    name: str
    description: str
    created_by: ID
    created_at: int
    location: str
    scene: str
    device_type: str
    duration: float
    augmented: bool
    muted: bool
    path: str

    tags: List["EntRecordingTag"] = field(default_factory=list, init=False, repr=False)

@dataclass
class EntRecordingTag:
    recording_id: ID  # EntRecording
    tag_id: ID  # EntTag
    created_by: ID
    created_at: int

@dataclass
class EntDataset:
    id: ID
    name: str
    description: str
    created_by: ID
    created_at: int

@dataclass
class EntDatasetVersion:
    id: ID
    dataset_id: ID  # EntDataset, this could be removed as EntVersion already contains it, but left it for easy reference
    recording_id: ID  # EntRecording
    version_id: ID  # EntVersion
    action: Action  # ADD or DELETE, as database will only contain diff between versions
    created_by: ID
    created_at: int
    description: str

@dataclass
class EntDatasetVersionTag:
    dataset_version_id: ID  # EntVersion
    tag_id: ID  # EntTag
    created_by: ID
    created_at: int

@dataclass
class EntFilelist:
    id: ID
    name: str
    description: str
    created_by: ID
    created_at: int
    latest_version: int

@dataclass
class EntFilelistVersion:
    id: ID
    filelist_id: ID  # EntFileList, this could be removed as EntVersion already contains it, but left it for easy reference
    recording_id: ID  # EntRecording
    version_id: ID  # EntVersion
    action: Action  # ADD or DELETE, as database will only contain diff between versions
    created_by: ID
    created_at: int
    description: str

@dataclass
class EntFilelistVersionTag:
    filelist_version_id: ID  # EntVersion
    tag_id: ID  # EntTag
    created_by: ID
    created_at: int

@dataclass
class EntList:
    id: ID
    name: str
    description: str
    created_by: ID
    created_at: int
    latest_version: int

@dataclass
class EntListVersion:
    id: ID
    list_id: ID  # EntList, this could be removed as EntVersion already contains it, but left it for easy reference
    file_list_id: ID  # EntFileList
    version_id: ID  # EntVersion
    action: Action  # ADD or DELETE, as database will only contain diff between versions
    created_by: ID
    created_at: int
    description: str

@dataclass
class EntListVersionTag:
    list_version_id: ID  # EntVersion
    tag_id: ID  # EntTag
    created_by: ID
    created_at: int

@dataclass
class Model:
    id: ID
    name: str
    description: str
    created_by: ID
    created_at: int
    train_file_list_v: ID  # EntVersion
    test_file_list_v: ID  # EntVersion

@dataclass
class EntLexieAudit:
    id: ID
    object_type: ObjectType  # RECORDING, FILELIST, LIST or DATASET
    object_id: ID  # EntRecording, EntFileList, EntList or EntDataset
    version_id: ID  # EntVersion
    created_by: ID
    created_at: int
    action: AuditAction  # ACCESS or MUTATE
    mode: Mode  # FRONTEND, LIBRARY or CODE

@dataclass
class Annotations:
    id: ID
    recording_id: ID  # EntRecording
    start_time: float
    end_time: float
    description: str
    created_by: ID
    created_at: float
