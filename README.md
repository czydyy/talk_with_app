# 群聊命令机器人

基于 [NoneBot2](https://nonebot.dev/) 的命令机器人起点。目前使用 Console 适配器在本地试跑；确定 Telegram、Discord、QQ 等目标平台后，再安装并注册对应适配器。

## 运行

需要 Python 3.10 或更新版本。在项目目录执行：

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python bot.py
```

如果系统中使用 `python` 而非 `py`，将第一行改为 `python -m venv .venv`。

在启动的终端中输入：

```text
/help
/collect 需要保存的内容
/list
/status
```

`/collect` 暂时保存命令后面的文字到本地 SQLite 数据库（`data/collect.sqlite3`）；`/list` 显示当前会话最近 20 条。CLI 集成尚未指定，后续可以在 `plugins/commands.py` 的处理函数中调用独立的业务函数。

## 扩展命令

在 `plugins/commands.py` 中用 `on_command("命令名")` 注册新命令，再添加对应的处理函数。对接真实群聊平台时，在 `bot.py` 注册它的 NoneBot 适配器，并安装该适配器包。不同平台的群会话标识和可见消息范围需要在接入时确认。
