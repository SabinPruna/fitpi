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
#     result = budget_from_dict(json.loads(json_string))

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, TypeVar, Callable, Type, cast
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Transaction:
    amount: int
    date: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        amount = from_int(obj.get("amount"))
        date = from_str(obj.get("date"))
        name = from_str(obj.get("name"))
        return Transaction(amount, date, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = from_int(self.amount)
        result["date"] = self.date.isoformat()
        result["name"] = from_str(self.name)
        return result


@dataclass
class Budget:
    name: str
    budget: int
    current: int
    month: str
    transactions: List[Transaction]

    @staticmethod
    def from_dict(obj: Any) -> 'Budget':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        budget = from_int(obj.get("budget"))
        current = from_int(obj.get("current"))
        month = from_str(obj.get("month"))
        transactions = from_list(Transaction.from_dict, obj.get("transactions"))
        return Budget(name, budget, current, month, transactions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["budget"] = from_int(self.budget)
        result["current"] = from_int(self.current)
        result["month"] = from_str(self.month)
        result["transactions"] = from_list(lambda x: to_class(Transaction, x), self.transactions)
        return result


def budget_from_dict(s: Any) -> Budget:
    return Budget.from_dict(s)


def budget_to_dict(x: Budget) -> Any:
    return to_class(Budget, x)
