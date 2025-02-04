from .compatibility import UserCompatibilityViewSet
from .gym import GymsAPIView, GymAPIView
from .muscle_group import MuscleGroupsAPIView
from .week_routine import WeekRoutineAPIView, WeekRoutinesAPIView
from .exercice import (
    ExercisesAPIView,
    ExerciseAPIView,
    ExercisesRankingAPIView,
)
from .day_training import (
    DayTrainingsAPIView,
    DayTrainingAPIView,
    DayTrainingCreateAPIView,
    DaytrainingByWeekdayAPIView
)
