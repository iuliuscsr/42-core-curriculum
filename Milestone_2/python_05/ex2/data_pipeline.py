#!/usr/bin/env python3
import typing
import abc


class ExportPlugin(typing.Protocol):

    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        csv_items = [item[1] for item in data]
        print("CSV Output:")
        print(",".join(csv_items))


class JSONPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        json_items = [f'"item_{rank}": "{val}"' for rank, val in data]
        print("JSON Output: ")
        print("{" + ", ".join(json_items) + "}")


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
        """Extracts the oldest piece of data and its rank."""
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

    def ingest(self, data: typing.Any) -> None:
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

    def ingest(self, data: typing.Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if type(data) is list:
            self.storage.extend(data)
        else:
            self.storage.append(data)


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

    def ingest(self, data: typing.Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if type(data) is list:
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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            package: list[tuple[int, str]] = []
            count = 0
            while proc.storage and count < nb:
                rank, data = proc.output()
                package.append((rank, data))
                count += 1
            if package:
                plugin.process_output(package)

    def print_processors_stats(self) -> None:

        print("\n== DataStream statistics ==")
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

    print("=== Code Nexus - Data Pipeline ===")
    print("\nInitialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()

    stream.register_processor(num_proc)
    stream.register_processor(text_proc)
    stream.register_processor(log_proc)

    package1: list[typing.Any] = [
        'Hello world', [3.14, -1, 2.71],
        [{'log_level': 'WARNING',
          'log_message': 'Telnet access! Use ssh instead'},
         {'log_level': 'INFO', 'log_message': 'User wil is '
          'connected'}], 42, ['Hi', 'five']]

    print("\nSend first batch of data on stream:", package1)
    stream.process_stream(package1)
    stream.print_processors_stats()

    csv_plugin = CSVPlugin()
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, csv_plugin)
    stream.print_processors_stats()

    package2: list[typing.Any] = [
        21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [{'log_level': 'ERROR', 'log_message': '500 server crash'},
         {'log_level': 'NOTICE', 'log_message': 'Certificate '
          'expires in 10 days'}],
        [32, 42, 64, 84, 128, 168], 'World hello']

    print("\nSend another batch of data:")
    stream.process_stream(package2)
    stream.print_processors_stats()

    json_plugin = JSONPlugin()
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, json_plugin)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
