# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = stats_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    #assert isinstance(x, int) and not isinstance(x, bool)
    return int(x or 0)


def from_str(x: Any) -> str:
    #assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    #assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    #assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
     #assert isinstance(x, list)
     if not x: 
        return []

     return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    #assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Goals:
    active_minutes: int
    calories_out: int
    distance: int
    floors: int
    steps: int

    @staticmethod
    def from_dict(obj: Any) -> 'Goals':
        #assert isinstance(obj, dict)
        active_minutes = from_int(obj.get("activeMinutes"))
        calories_out = from_int(obj.get("caloriesOut"))
        distance = from_int(obj.get("distance"))
        floors = from_int(obj.get("floors"))
        steps = from_int(obj.get("steps"))
        return Goals(active_minutes, calories_out, distance, floors, steps)

    def to_dict(self) -> dict:
        result: dict = {}
        result["activeMinutes"] = from_int(self.active_minutes)
        result["caloriesOut"] = from_int(self.calories_out)
        result["distance"] = from_int(self.distance)
        result["floors"] = from_int(self.floors)
        result["steps"] = from_int(self.steps)
        return result


@dataclass
class Distance:
    activity: str
    distance: float

    @staticmethod
    def from_dict(obj: Any) -> 'Distance':
        #assert isinstance(obj, dict)
        activity = from_str(obj.get("activity"))
        distance = from_float(obj.get("distance"))
        return Distance(activity, distance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["activity"] = from_str(self.activity)
        result["distance"] = to_float(self.distance)
        return result


@dataclass
class HeartRateZone:
    calories_out: float
    max: int
    min: int
    minutes: int
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'HeartRateZone':
        #assert isinstance(obj, dict)
        calories_out = from_float(obj.get("caloriesOut"))
        max = from_int(obj.get("max"))
        min = from_int(obj.get("min"))
        minutes = from_int(obj.get("minutes"))
        name = from_str(obj.get("name"))
        return HeartRateZone(calories_out, max, min, minutes, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["caloriesOut"] = to_float(self.calories_out)
        result["max"] = from_int(self.max)
        result["min"] = from_int(self.min)
        result["minutes"] = from_int(self.minutes)
        result["name"] = from_str(self.name)
        return result


@dataclass
class Summary:
    active_score: int
    activity_calories: int
    calories_bmr: int
    calories_out: int
    distances: List[Distance]
    elevation: float
    fairly_active_minutes: int
    floors: int
    heart_rate_zones: List[HeartRateZone]
    lightly_active_minutes: int
    marginal_calories: int
    resting_heart_rate: int
    sedentary_minutes: int
    steps: int
    very_active_minutes: int

    @staticmethod
    def from_dict(obj: Any) -> 'Summary':
        #assert isinstance(obj, dict)
        active_score = from_int(obj.get("activeScore"))
        activity_calories = from_int(obj.get("activityCalories"))
        calories_bmr = from_int(obj.get("caloriesBMR"))
        calories_out = from_int(obj.get("caloriesOut"))
        distances = from_list(Distance.from_dict, obj.get("distances"))
        elevation = from_float(obj.get("elevation"))
        fairly_active_minutes = from_int(obj.get("fairlyActiveMinutes"))
        floors = from_int(obj.get("floors"))
        heart_rate_zones = from_list(HeartRateZone.from_dict, obj.get("heartRateZones"))
        lightly_active_minutes = from_int(obj.get("lightlyActiveMinutes"))
        marginal_calories = from_int(obj.get("marginalCalories"))
        resting_heart_rate = from_int(obj.get("restingHeartRate"))
        sedentary_minutes = from_int(obj.get("sedentaryMinutes"))
        steps = from_int(obj.get("steps"))
        very_active_minutes = from_int(obj.get("veryActiveMinutes"))
        return Summary(active_score, activity_calories, calories_bmr, calories_out, distances, elevation, fairly_active_minutes, floors, heart_rate_zones, lightly_active_minutes, marginal_calories, resting_heart_rate, sedentary_minutes, steps, very_active_minutes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["activeScore"] = from_int(self.active_score)
        result["activityCalories"] = from_int(self.activity_calories)
        result["caloriesBMR"] = from_int(self.calories_bmr)
        result["caloriesOut"] = from_int(self.calories_out)
        result["distances"] = from_list(lambda x: to_class(Distance, x), self.distances)
        result["elevation"] = to_float(self.elevation)
        result["fairlyActiveMinutes"] = from_int(self.fairly_active_minutes)
        result["floors"] = from_int(self.floors)
        result["heartRateZones"] = from_list(lambda x: to_class(HeartRateZone, x), self.heart_rate_zones)
        result["lightlyActiveMinutes"] = from_int(self.lightly_active_minutes)
        result["marginalCalories"] = from_int(self.marginal_calories)
        result["restingHeartRate"] = from_int(self.resting_heart_rate)
        result["sedentaryMinutes"] = from_int(self.sedentary_minutes)
        result["steps"] = from_int(self.steps)
        result["veryActiveMinutes"] = from_int(self.very_active_minutes)
        return result


@dataclass
class Stats:
    activities: List[Any]
    goals: Goals
    summary: Summary
    date: str
    start_weight: float
    weight: int
    sleep_goal_minutes: int
    sleep_minutes: int
    sleep_minutes_awake: int

    @staticmethod
    def from_dict(obj: Any) -> 'Stats':
        #assert isinstance(obj, dict)
        activities = from_list(lambda x: x, obj.get("activities"))
        goals = Goals.from_dict(obj.get("goals"))
        summary = Summary.from_dict(obj.get("summary"))
        date = from_str(obj.get("date"))
        start_weight = from_float(obj.get("startWeight"))
        weight = from_int(obj.get("weight"))
        sleep_goal_minutes = from_int(obj.get("sleepGoalMinutes"))
        sleep_minutes = from_int(obj.get("sleepMinutes"))
        sleep_minutes_awake = from_int(obj.get("sleepMinutesAwake"))
        return Stats(activities, goals, summary, date, start_weight, weight, sleep_goal_minutes, sleep_minutes, sleep_minutes_awake)

    def to_dict(self) -> dict:
        result: dict = {}
        result["activities"] = from_list(lambda x: x, self.activities)
        result["goals"] = to_class(Goals, self.goals)
        result["summary"] = to_class(Summary, self.summary)
        result["date"] = from_str(self.date)
        result["startWeight"] = to_float(self.start_weight)
        result["weight"] = from_int(self.weight)
        result["sleepGoalMinutes"] = from_int(self.sleep_goal_minutes)
        result["sleepMinutes"] = from_int(self.sleep_minutes)
        result["sleepMinutesAwake"] = from_int(self.sleep_minutes_awake)
        return result


def stats_from_dict(s: Any) -> Stats:
    return Stats.from_dict(s)


def stats_to_dict(x: Stats) -> Any:
    return to_class(Stats, x)
