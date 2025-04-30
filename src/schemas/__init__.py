__all__ = [
    'UserRegister',
    'TokenResponse',
    'RefreshTokenRequest',
    'ChangePasswordRequest',
    'TopicBlockResponse',
    'ShortMaterialResponse',
    'MaterialVideoResponse',
    'MaterialTextResponse',
    'MaterialTasksResponse',
    'CreateFeedback',
    'ShortVariantResponse',
    'VariantListResponse',
    'VariantResponse',
    'VariantForActiveTask',
    'TaskResponse',
    'TaskSubmit',
    'TaskHomeworkSubmit',
    'TaskForLastHomework',
    'TaskAnswer',
    'ShortActiveHomework',
    'ShortLastHomework',
    'ActiveHomework',
    'LastHomework',
    'EditHomework',
    'TeacherHomework',
    'CreateHomework',
    'VariantForCreateTask',
    'ShortClassResponse',
    'ClassResponse',
    'ShortLastHWTeacher',
    'ShortActiveHWTeacher',
    'UserStatistic',
    'VariantStatistic',
    'HomeworkStatistic'
]

from .auth import UserRegister, TokenResponse, RefreshTokenRequest, ChangePasswordRequest
from .topic_block import TopicBlockResponse
from .material import ShortMaterialResponse, MaterialVideoResponse, MaterialTextResponse, MaterialTasksResponse
from .feedback import CreateFeedback
from .variant import (
    ShortVariantResponse,
    VariantListResponse,
    VariantForActiveTask,
    VariantResponse,
    VariantForCreateTask,
    VariantStatistic
)
from .task import TaskResponse, TaskSubmit, TaskHomeworkSubmit, TaskForLastHomework, TaskAnswer
from .homework import (
    ShortActiveHomework,
    ShortLastHomework,
    ActiveHomework,
    LastHomework,
    EditHomework,
    TeacherHomework,
    CreateHomework,
    ShortLastHWTeacher,
    ShortActiveHWTeacher,
    HomeworkStatistic
)
from .learning_class import ShortClassResponse, ClassResponse
from .user import UserStatistic
