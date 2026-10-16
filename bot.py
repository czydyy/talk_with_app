"""NoneBot2 entry point. Register a group platform adapter here later."""

import nonebot
from nonebot.adapters.console import Adapter as ConsoleAdapter

nonebot.init(command_start={"/"})
driver = nonebot.get_driver()
driver.register_adapter(ConsoleAdapter)
nonebot.load_plugin("plugins.commands")

if __name__ == "__main__":
    nonebot.run()
