import random
from core.plugin import BasePlugin, logger, on, Priority
from core.chat.message_utils import KiraMessageBatchEvent
from core.chat.message_elements import Text, Sticker, Reply
from core.chat import MessageChain


class StickerControlPlugin(BasePlugin):
    def __init__(self, ctx, cfg: dict):
        super().__init__(ctx, cfg)
        self.probability = float(cfg.get("sticker_probability", 0.5))
        self.random_position = bool(cfg.get("random_position", True))

    async def initialize(self):
        logger.info(f"StickerControlPlugin initialized: probability={self.probability}, random_position={self.random_position}")

    async def terminate(self):
        pass

    @on.after_xml_parse(priority=Priority.HIGH)
    async def process_stickers(self, event: KiraMessageBatchEvent, message_chains: list):
        if not message_chains:
            return

        # 1. 过滤掉只有 Reply 的消息链
        filtered_chains = []
        for chain in message_chains:
            if len(chain.message_list) == 1 and isinstance(chain.message_list[0], Reply):
                logger.debug(f"丢弃只有引用的消息块: {chain.message_list[0]}")
                continue
            filtered_chains.append(chain)
        message_chains[:] = filtered_chains

        if not message_chains:
            return

        # 2. 处理 sticker
        sticker_chains = []      # 存放单独的表情链
        new_chains = []          # 存放处理后的非表情链

        for chain in message_chains:
            elements = chain.message_list
            # 找出所有 sticker 的索引
            sticker_indices = [i for i, e in enumerate(elements) if isinstance(e, Sticker)]
            if not sticker_indices:
                new_chains.append(chain)
                continue

            # 决定保留哪些 sticker
            keep_indices = []
            for idx in sticker_indices:
                if random.random() < self.probability:
                    keep_indices.append(idx)
                else:
                    logger.debug(f"删除 sticker: {elements[idx]}")

            # 从原链中移除所有 sticker（无论保留与否）
            new_elements = [e for i, e in enumerate(elements) if i not in sticker_indices]
            if new_elements:
                new_chains.append(MessageChain(new_elements))

            # 保留的 sticker 单独成链
            for idx in keep_indices:
                sticker_chains.append(MessageChain([elements[idx]]))

        # 3. 随机插入表情链
        if self.random_position:
            for sticker_chain in sticker_chains:
                pos = random.randint(0, len(new_chains))
                new_chains.insert(pos, sticker_chain)
        else:
            new_chains.extend(sticker_chains)

        message_chains.clear()
        message_chains.extend(new_chains)
        logger.debug(f"处理完成，消息块数量: {len(message_chains)}")