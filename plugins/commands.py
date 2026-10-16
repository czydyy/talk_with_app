"""Example commands, kept independent of any particular chat platform."""

from nonebot import on_command
from nonebot.adapters import Event, Message
from nonebot.params import CommandArg

from .storage import add_item, list_items

help_command = on_command("help", priority=10, block=True)
status_command = on_command("status", priority=10, block=True)
collect_command = on_command("collect", priority=10, block=True)
list_command = on_command("list", priority=10, block=True)


@help_command.handle()
async def handle_help() -> None:
    await help_command.finish(
        "/collect 内容 — 保存一条内容\n"
        "/list — 查看当前会话保存的内容\n"
        "/status — 查看机器人状态\n"
        "/help — 查看命令"
    )


@status_command.handle()
async def handle_status() -> None:
    await status_command.finish("机器人正在运行。")


@collect_command.handle()
async def handle_collect(event: Event, args: Message = CommandArg()) -> None:
    content = args.extract_plain_text().strip()
    if not content:
        await collect_command.finish("用法：/collect 要保存的内容")
    item_id = add_item(event.get_session_id(), event.get_user_id(), content)
    await collect_command.finish(f"已收集 #{item_id}。")


@list_command.handle()
async def handle_list(event: Event) -> None:
    items = list_items(event.get_session_id())
    if not items:
        await list_command.finish("当前会话还没有收集内容。")
    lines = [f"#{item_id} {content}" for item_id, content in items]
    await list_command.finish("已收集：\n" + "\n".join(lines))
