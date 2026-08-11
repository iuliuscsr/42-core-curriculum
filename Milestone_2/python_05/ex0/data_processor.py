#!/usr/bin/env python3
import typing
import abc


class DataProcessor(abc.ABC):

    def __init__(self) -> None:
        self.storage: list[str] = []
        self.rank: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:

        data: str = self.storage.pop(0)
        current_rank: int = self.rank
        self.rank += 1
        return current_rank, data


class NumericProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:
        if type(data) in (int, float):
            return True
        elif type(data) is list and data:
            return all(type(item) in (int, float) for item in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if type(data) is list:
            self.storage.extend(str(item) for item in data)
        else:
            self.storage.append(str(data))


class TextProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:
        if type(data) is str:
            return True
        elif type(data) is list and data:
            return all(type(item) is str for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if type(data) is list:
            self.storage.extend(data)
        else:
            self.storage.append(str(data))


class LogProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:
        if type(data) is dict:
            return (
                "log_level" in data
                and "log_message" in data
                and type(data["log_level"]) is str
                and type(data["log_message"]) is str
            )
        elif type(data) is list and data:
            return all(
                type(item) is dict
                and "log_level" in item
                and "log_message" in item
                and type(item["log_level"]) is str
                and type(item["log_message"]) is str
                for item in data
                )
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            self.storage.extend(
                f"{item['log_level']}: {item['log_message']}" for item in data
            )
        else:
            self.storage.append(f"{data['log_level']}: {data['log_message']}")


def main() -> None:

    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    num_proc = NumericProcessor()
    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest("foo")
    except ValueError as e:
        print(f"Got exception: {e}")

    num_data: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_data}")
    num_proc.ingest(num_data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num_proc.output()
        print(f"Numeric value {rank}: {val}")

    print("\nTesting Text Processor...")
    text_proc = TextProcessor()
    print(f"Trying to validate input '42': {text_proc.validate(42)}")
    text_data: list[str] = ["Hello", "Nexus", "World"]
    print(f"Processing data: {text_data}")
    text_proc.ingest(text_data)
    print("Extracting 1 value...")
    rank, val = text_proc.output()
    print(f"Text value {rank}: {val}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()
    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    log_data: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {log_data}")
    log_proc.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {rank}: {val}")


if __name__ == "__main__":
    main()
