from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    #assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    #assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    #assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    #assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Totals:
    calories: int
    carbohydrates: int
    fat: int
    protein: int
    sodium: int
    sugar: int

    @staticmethod
    def from_dict(obj: Any) -> 'Totals':
        #assert isinstance(obj, dict)
        calories = from_int(obj.get("calories"))
        carbohydrates = from_int(obj.get("carbohydrates"))
        fat = from_int(obj.get("fat"))
        protein = from_int(obj.get("protein"))
        sodium = from_int(obj.get("sodium"))
        sugar = from_int(obj.get("sugar"))
        return Totals(calories, carbohydrates, fat, protein, sodium, sugar)

    def to_dict(self) -> dict:
        result: dict = {}
        result["calories"] = from_int(self.calories)
        result["carbohydrates"] = from_int(self.carbohydrates)
        result["fat"] = from_int(self.fat)
        result["protein"] = from_int(self.protein)
        result["sodium"] = from_int(self.sodium)
        result["sugar"] = from_int(self.sugar)
        return result


@dataclass
class Entry:
    name: str
    nutrition_information: Totals

    @staticmethod
    def from_dict(obj: Any) -> 'Entry':
        #assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        nutrition_information = Totals.from_dict(obj.get("nutrition_information"))
        return Entry(name, nutrition_information)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["nutrition_information"] = to_class(Totals, self.nutrition_information)
        return result


@dataclass
class Breakfast:
    totals: Totals
    entries: List[Entry]

    @staticmethod
    def from_dict(obj: Any) -> 'Breakfast':
        #assert isinstance(obj, dict)
        totals = Totals.from_dict(obj.get("totals"))
        entries = from_list(Entry.from_dict, obj.get("entries"))
        return Breakfast(totals, entries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["totals"] = to_class(Totals, self.totals)
        result["entries"] = from_list(lambda x: to_class(Entry, x), self.entries)
        return result

@dataclass
class Lunch:
    totals: Totals
    entries: List[Entry]

    @staticmethod
    def from_dict(obj: Any) -> 'Lunch':
        #assert isinstance(obj, dict)
        totals = Totals.from_dict(obj.get("totals"))
        entries = from_list(Entry.from_dict, obj.get("entries"))
        return Lunch(totals, entries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["totals"] = to_class(Totals, self.totals)
        result["entries"] = from_list(lambda x: to_class(Entry, x), self.entries)
        return result

@dataclass
class Dinner:
    totals: Totals
    entries: List[Entry]

    @staticmethod
    def from_dict(obj: Any) -> 'Dinner':
        #assert isinstance(obj, dict)
        totals = Totals.from_dict(obj.get("totals"))
        entries = from_list(Entry.from_dict, obj.get("entries"))
        return Dinner(totals, entries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["totals"] = to_class(Totals, self.totals)
        result["entries"] = from_list(lambda x: to_class(Entry, x), self.entries)
        return result

@dataclass
class Snacks:
    totals: Totals
    entries: List[Entry]

    @staticmethod
    def from_dict(obj: Any) -> 'Snacks':
        #assert isinstance(obj, dict)
        totals = Totals.from_dict(obj.get("totals"))
        entries = from_list(Entry.from_dict, obj.get("entries"))
        return Snacks(totals, entries)

    def to_dict(self) -> dict:
        result: dict = {}
        result["totals"] = to_class(Totals, self.totals)
        result["entries"] = from_list(lambda x: to_class(Entry, x), self.entries)
        return result       



@dataclass
class MfpModel:
    calories: int
    carbohydrates: int
    fat: int
    protein: int
    sodium: int
    sugar: int
    weight: str
    date: str
    breakfast: Breakfast
    lunch: Lunch
    dinner: Dinner
    snacks: Snacks

    @staticmethod
    def from_dict(obj: Any) -> 'MfpModel':
        #assert isinstance(obj, dict)
        calories = from_int(obj.get("calories"))
        carbohydrates = from_int(obj.get("carbohydrates"))
        fat = from_int(obj.get("fat"))
        protein = from_int(obj.get("protein"))
        sodium = from_int(obj.get("sodium"))
        sugar = from_int(obj.get("sugar"))
        weight = from_str(obj.get("weight"))
        date = from_str(obj.get("date"))
        breakfast = Breakfast.from_dict(obj.get("breakfast"))
        lunch = Lunch.from_dict(obj.get("lunch"))
        dinner = Dinner.from_dict(obj.get("dinner"))
        snacks = Snacks.from_dict(obj.get("snacks"))
        return MfpModel(calories, carbohydrates, fat, protein, sodium, sugar, weight, date, breakfast, lunch, dinner, snacks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["calories"] = from_int(self.calories)
        result["carbohydrates"] = from_int(self.carbohydrates)
        result["fat"] = from_int(self.fat)
        result["protein"] = from_int(self.protein)
        result["sodium"] = from_int(self.sodium)
        result["sugar"] = from_int(self.sugar)
        result["weight"] = from_str(self.weight)
        result["date"] = self.date.isoformat()
        result["breakfast"] = to_class(Breakfast, self.breakfast)
        result["lunch"] = to_class(Lunch, self.lunch)
        result["dinner"] = to_class(Dinner, self.dinner)
        result["snacks"] = to_class(Snacks, self.snacks)
        return result


def mfp_model_from_dict(s: Any) -> MfpModel:
    return MfpModel.from_dict(s)


def mfp_model_to_dict(x: MfpModel) -> Any:
    return to_class(MfpModel, x)