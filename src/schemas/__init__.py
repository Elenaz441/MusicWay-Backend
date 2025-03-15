__all__ = [
    'UserRegister',
    'TokenResponse',
    'RefreshTokenRequest',
    'ChangePasswordRequest',
    'TopicBlockResponse',
    'ShortMaterialResponse',
    'MaterialVideoResponse',
    'MaterialTextResponse',
    'CreateFeedback',
    'ShortVariantResponse',
    'VariantResponse',
    'VariantForActiveTask',
    'TaskResponse',
    'TaskSubmit',
    'TaskHomeworkSubmit',
    'TaskForLastHomework',
    'ShortActiveHomework',
    'ShortLastHomework',
    'ActiveHomework',
    'LastHomework',
    'EditHomework',
    'TeacherHomework',
    'CreateHomework'
]

from .auth import UserRegister, TokenResponse, RefreshTokenRequest, ChangePasswordRequest
from .topic_block import TopicBlockResponse
from .material import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse
from .feedback import CreateFeedback
from .variant import ShortVariantResponse, VariantResponse, VariantForActiveTask
from .task import TaskResponse, TaskSubmit, TaskHomeworkSubmit, TaskForLastHomework
from .homework import (
    ShortActiveHomework,
    ShortLastHomework,
    ActiveHomework,
    LastHomework,
    EditHomework,
    TeacherHomework,
    CreateHomework
)
