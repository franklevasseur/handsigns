import rich


class Logger:

    def debug(self, message):
        rich.print(f"[white on blue] [/] {message}")

    def info(self, message: str):
        rich.print(f"[white on green] [/] {message}")

    def warning(self, message: str):
        rich.print(f"[white on yellow] [/] {message}")

    def error(self, message: str):
        rich.print(f"[white on red] [/] {message}")
