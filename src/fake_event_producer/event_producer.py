import csv
import pathlib
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Iterator, List, Optional
from uuid import uuid4

from faker import Faker

fake = Faker()


class UserType(Enum):
    HONEST = auto()
    FRAUDULENT = auto()


@dataclass
class LessonCompletedEvent:
    """
    Basic lesson completion event.
    """

    event_id: uuid4
    user_email: str
    created_at: str
    lesson_id: int
    course_id: int = 42
    name: str = "LessonCompleted"


def get_event_timestamps(
    interval_length: float, amount: int, from_time: Optional[datetime] = None
) -> List[datetime]:
    """
    Generate given amount of events at specified interval length (+ small randomness for microseconds).
    """
    if from_time is None:
        from_time = datetime.utcnow()
    intervals = [from_time]
    for _ in range(amount - 1):
        intervals.append(
            intervals[-1]
            + timedelta(seconds=interval_length, milliseconds=random.randint(0, 200))
        )
    return intervals


def produce_user_lesson_completed_event_series(
    user_type: UserType = UserType.HONEST,
    user_email: Optional[str] = None,
    lessons_completed_amount: Optional[int] = None,
    course_id: int = 42,
) -> List[LessonCompletedEvent]:
    """
    Produces series of events that simulate a user completing random amount of lessons for course.
    user_type determines the interval between consecutive events (~1 second for fraudulent ones,
    ~5 seconds for honest ones).
    """
    if lessons_completed_amount is None:
        lessons_completed_amount = random.randint(1, 7)

    if user_email is None:
        user_email = fake.email()

    interval_length = 5 if user_type == UserType.HONEST else 1
    events_timestamps = get_event_timestamps(
        from_time=datetime.utcnow(),
        interval_length=interval_length,
        amount=lessons_completed_amount,
    )

    return [
        LessonCompletedEvent(
            event_id=str(uuid4()),
            user_email=user_email,
            created_at=event_timestamp.isoformat(),
            lesson_id=lesson_id,
            course_id=course_id,
        )
        for lesson_id, event_timestamp in enumerate(events_timestamps, start=1)
    ]


def produce_lessons_completed_events_batch(
    unique_users: int,
) -> Iterator[LessonCompletedEvent]:
    for _ in range(unique_users):
        user_events = produce_user_lesson_completed_event_series()
        for user_event in user_events:
            yield user_event


def produce_lessons_completed_events_csv_batch(
    unique_users: int,
    filepath: pathlib.Path,
) -> None:
    events = produce_lessons_completed_events_batch(unique_users=unique_users)
    header = ("event_id", "created_at", "user_email", "lesson_id", "course_id")

    with open(filepath, "wt") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for event in events:
            writer.writerow(
                (
                    event.event_id,
                    event.created_at,
                    event.user_email,
                    event.lesson_id,
                    event.course_id,
                )
            )
