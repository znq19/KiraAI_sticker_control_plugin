# KiraAI_sticker_control_plugin/表情包发送频率和随机位置控制
该插件已整合至KiraAI官方QQ增强插件并得到开发者@xxynet更优秀的代码修复：https://github.com/xxynet/kira-ai-plugin-qq-enhance
控制AI发送表情（注：是sticker而非emoji）的频率和随机位置，并确保表情独立成行。
这对节省部分人设提示词字数以及一些不太能很好处理这类问题（如总是发表情包、表情包和文字段落没有分开、表情包总是固定最后一条发送）的模型增加活人感很有用。
webui中可设置每个表情被保留的概率（0~1）。例如 0.3 表示30%的概率保留，70%概率删除；
是否将表情随机插入到消息中间（而不是固定在最后）（默认true）。
