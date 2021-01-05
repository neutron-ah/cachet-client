from datetime import datetime
from cachetclient.v1 import enums
from typing import Generator, Set

from cachetclient.base import Resource, Manager
from cachetclient import utils


class Schedule(Resource):

    @property
    def id(self) -> int:
        return self.get('id')

    @property
    def name(self) -> str:
        return self.get('name')

    @property
    def message(self) -> str:
        return self.get('message')

    @property
    def status(self) -> int:
        return self.get('status')

    @property
    def scheduled_at(self) -> datetime:
        return utils.to_datetime(self.get('scheduled_at'))

    @property
    def completed_at(self) -> datetime:
        return utils.to_datetime(self.get('completed_at'))


class ScheduleManager(Manager):
    path = 'schedules'
    resource_class = Schedule

    def create(
            self,
            *,
            name: str,
            status: int,
            message: str = None,
            scheduled_at: datetime = None):
        """Create a shedule.

        Returns:
            :py:class:`Shedule` instance
        """
        if status not in enums.SCHEDULE_STATUS_LIST:
            raise ValueError("Invalid status id '{}'. Valid values :{}".format(
                status,
                enums.SCHEDULE_STATUS_LIST,
            ))

        return self._create(
            self.path,
            {
                'name': name,
                'message': message,
                'status': status,
                'scheduled_at': scheduled_at.strftime('%Y-%m-%d %H:%M') if scheduled_at else None
            }
        )

    def update(
            self,
            schedule_id: int,
            *,
            name: str,
            status: int,
            message: str = None,
            scheduled_at: datetime = None,
            **kwargs) -> Schedule:
        """Update a Schedule by id.

        Args:
            schedule_id (int): The schedule to update

        Keyword Args:
            status (int): Status of the schedule (see enums)
            name (str): New name
            description (str): New description

        Returns:
            Updated Schedule from server
        """
        return self._update(
            self.path,
            schedule_id,
            self._build_data_dict(
                name=name,
                status=status,
                message=message,
                scheduled_at=scheduled_at.strftime('%Y-%m-%d %H:%M') if scheduled_at else None
            ),
        )


    def list(self, page: int = 1, per_page: int = 20) -> Generator[Schedule, None, None]:
        """List all schedules

        Keyword Args:
            page (int): The page to start listing
            per_page (int): Number of entries per page

        Returns:
            Generator of Schedules instances
        """
        yield from self._list_paginated(self.path, page=page, per_page=per_page)

    def get(self, schedule_id: int) -> Schedule:
        """Get a schedule by id

        Args:
            schedule_id (int): Id of the schedule

        Returns:
            Schedule instance

        Raises:
            HttpError: if not found
        """
        return self._get(self.path, schedule_id)

    def delete(self, schedule_id: int) -> None:
        """Delete a schedule

        Args:
            schedule_id (int): Id of the schedule

        Raises:
            HTTPError: if schedule do not exist
        """
        self._delete(self.path, schedule_id)
