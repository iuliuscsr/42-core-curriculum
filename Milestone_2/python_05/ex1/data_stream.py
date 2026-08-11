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


class DataStream():

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []
        self.stats: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        if proc not in self.processors:
            self.processors.append(proc)
            self.stats[proc] = 0

    def process_item(self, item: typing.Any) -> bool:
        for proc in self.processors:
            if proc.validate(item):
                proc.ingest(item)
                count = len(item) if type(item) is list else 1
                self.stats[proc] += count
                return True
        return False

    def process_stream(self, stream: list[typing.Any]) -> None:

        for item in stream:
            if not self.process_item(item):
                print(f"DataStream error - "
                      f"Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:

        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            total = self.stats[proc]
            remaining = len(proc.storage)
            print(f"{name}: total {total} items processed, "
                  f"remaining {remaining} on processor")


def main() -> None:

    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor\n")
    num_proc = NumericProcessor()
    stream.register_processor(num_proc)
    package: list[typing.Any] = [
            'Hello world', [3.14, -1, 2.71],
            [{'log_level': 'WARNING',
              'log_message': 'Telnet access! Use ssh instead'},
             {'log_level': 'INFO', 'log_message': 'User wil is '
              'connected'}], 42, ['Hi', 'five']]
    print(f"\nSend first batch of data on stream: {package}")
    stream.process_stream(package)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    stream.register_processor(text_proc)
    stream.register_processor(log_proc)
    print("Send the same batch again")
    stream.process_stream(package)
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num_proc.output()
    for _ in range(2):
        text_proc.output()
    log_proc.output()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
