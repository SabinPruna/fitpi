# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = activity_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    #assert isinstance(x, int) and not isinstance(x, bool)
    if not x:
        return 0
    else:
        return x


def from_str(x: Any) -> str:
    #assert isinstance(x, str)
    if not x:
        return ""
    else:
        return x


def from_bool(x: Any) -> bool:
    #assert isinstance(x, bool)
    if not x:
        return False
    else:
        return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    #assert isinstance(x, list)
    if not x: 
        return []
        
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    if not x:
        return datetime.now()
    else:
        return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    #assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class ActivityLevel:
    minutes: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'ActivityLevel':
        #assert isinstance(obj, dict)
        minutes = from_int(obj.get("minutes"))
        name = from_str(obj.get("name"))
        return ActivityLevel(minutes, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["minutes"] = from_int(self.minutes)
        result["name"] = from_str(self.name)
        return result


@dataclass
class HeartRateZone:
    max: int
    min: int
    minutes: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'HeartRateZone':
        #assert isinstance(obj, dict)
        max = from_int(obj.get("max"))
        min = from_int(obj.get("min"))
        minutes = from_int(obj.get("minutes"))
        name = from_str(obj.get("name"))
        return HeartRateZone(max, min, minutes, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["max"] = from_int(self.max)
        result["min"] = from_int(self.min)
        result["minutes"] = from_int(self.minutes)
        result["name"] = from_str(self.name)
        return result


@dataclass
class ManualValuesSpecified:
    calories: bool
    distance: bool
    steps: bool

    @staticmethod
    def from_dict(obj: Any) -> 'ManualValuesSpecified':
        #assert isinstance(obj, dict)
        if not obj:
            calories = False
            distance = False
            steps = False
        else:
            calories = from_bool(obj.get("calories"))
            distance = from_bool(obj.get("distance"))
            steps = from_bool(obj.get("steps"))
            return ManualValuesSpecified(calories, distance, steps)

    def to_dict(self) -> dict:
        result: dict = {}
        result["calories"] = from_bool(self.calories)
        result["distance"] = from_bool(self.distance)
        result["steps"] = from_bool(self.steps)
        return result


@dataclass
class Activity:
    active_duration: int
    activity_level: List[ActivityLevel]
    activity_name: str
    activity_type_id: int
    average_heart_rate: int
    calories: int
    duration: int
    elevation_gain: int
    heart_rate_link: str
    heart_rate_zones: List[HeartRateZone]
    last_modified: datetime
    log_id: int
    log_type: str
    manual_values_specified: ManualValuesSpecified
    original_duration: int
    original_start_time: datetime
    start_time: datetime
    steps: int
    tcx_link: str

    @staticmethod
    def from_dict(obj: Any) -> 'Activity':
        #assert isinstance(obj, dict)
        active_duration = from_int(obj.get("activeDuration"))
        activity_level = from_list(ActivityLevel.from_dict, obj.get("activityLevel"))
        activity_name = from_str(obj.get("activityName"))
        activity_type_id = from_int(obj.get("activityTypeId"))
        average_heart_rate = from_int(obj.get("averageHeartRate"))
        calories = from_int(obj.get("calories"))
        duration = from_int(obj.get("duration"))
        elevation_gain = from_int(obj.get("elevationGain"))
        heart_rate_link = from_str(obj.get("heartRateLink"))
        heart_rate_zones = from_list(HeartRateZone.from_dict, obj.get("heartRateZones"))
        last_modified = from_datetime(obj.get("lastModified"))
        log_id = from_int(obj.get("logId"))
        log_type = from_str(obj.get("logType"))
        manual_values_specified = ManualValuesSpecified.from_dict(obj.get("manualValuesSpecified"))
        original_duration = from_int(obj.get("originalDuration"))
        original_start_time = from_datetime(obj.get("originalStartTime"))
        start_time = from_datetime(obj.get("startTime"))
        steps = from_int(obj.get("steps"))
        tcx_link = from_str(obj.get("tcxLink"))
        return Activity(active_duration, activity_level, activity_name, activity_type_id, average_heart_rate, calories, duration, elevation_gain, heart_rate_link, heart_rate_zones, last_modified, log_id, log_type, manual_values_specified, original_duration, original_start_time, start_time, steps, tcx_link)

    def to_dict(self) -> dict:
        result: dict = {}
        result["activeDuration"] = from_int(self.active_duration)
        result["activityLevel"] = from_list(lambda x: to_class(ActivityLevel, x), self.activity_level)
        result["activityName"] = from_str(self.activity_name)
        result["activityTypeId"] = from_int(self.activity_type_id)
        result["averageHeartRate"] = from_int(self.average_heart_rate)
        result["calories"] = from_int(self.calories)
        result["duration"] = from_int(self.duration)
        result["elevationGain"] = from_int(self.elevation_gain)
        result["heartRateLink"] = from_str(self.heart_rate_link)
        result["heartRateZones"] = from_list(lambda x: to_class(HeartRateZone, x), self.heart_rate_zones)
        result["lastModified"] = self.last_modified.isoformat()
        result["logId"] = from_int(self.log_id)
        result["logType"] = from_str(self.log_type)
        result["manualValuesSpecified"] = to_class(ManualValuesSpecified, self.manual_values_specified)
        result["originalDuration"] = from_int(self.original_duration)
        result["originalStartTime"] = self.original_start_time.isoformat()
        result["startTime"] = self.start_time.isoformat()
        result["steps"] = from_int(self.steps)
        result["tcxLink"] = from_str(self.tcx_link)
        return result


def activity_from_dict(s: Any) -> Activity:
    return Activity.from_dict(s)


def activity_to_dict(x: Activity) -> Any:
    return to_class(Activity, x)
