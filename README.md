# KiraAI_sticker_control_plugin / 表情包发送频率和随机位置控制 1.2.0

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/znq19/KiraAI_sticker_control_plugin)

该插件已整合至 KiraAI 官方 QQ 增强插件并得到开发者 @xxynet 更优秀的代码修改：https://github.com/xxynet/kira-ai-plugin-qq-enhance

控制 AI 发送表情（注：是 sticker 而非 emoji）的频率和随机位置，并确保表情独立成行。

这对节省部分人设提示词字数以及一些不太能很好处理这类问题（如总是发表情包、表情包和文字段落没有分开、表情包总是固定最后一条发送）的模型增加活人感很有用。

## 行为说明（与 QQ 增强对齐）

- 过滤纯 Reply 消息块（`len(chain)==1` 且为 Reply）。
- 按概率保留 sticker，并从原链剥离后独立成行。
- 去掉 sticker 后若只剩 Reply，则丢弃该空引用链。
- 开启随机位置时：先分离表情链/非表情链，再随机插入；关闭时表情链紧跟对应原链顺序。

## WebUI 配置

| 配置项 | 默认 | 说明 |
|---|---|---|
| `sticker_probability` | 0.5 | 每个表情被保留的概率（0~1） |
| `random_position` | true | 是否将表情随机插入到消息中间 |
