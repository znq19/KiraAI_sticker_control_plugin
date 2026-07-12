import random
from core.plugin import BasePlugin, logger, on, Priority
from core.chat.message_utils import KiraMessageBatchEvent
from core.chat.message_elements import Text, Sticker, Reply
from core.chat import MessageChain


class StickerControlPlugin(BasePlugin):
    def __init__(self, ctx, cfg: dict):
        super().__init__(ctx, cfg)
        self.sticker_probability = float(cfg.get("sticker_probability", 0.5))
        self.random_position = bool(cfg.get("random_position", True))

    async def initialize(self):
        logger.info(
            f"StickerControlPlugin initialized: "
            f"probability={self.sticker_probability}, "
            f"random_position={self.random_position}"
        )

    async def terminate(self):
        pass

    @on.after_xml_parse(priority=Priority.HIGH)
    async def process_stickers(self, event: KiraMessageBatchEvent, message_chains: list):
        if not message_chains:
            return

        # 1. 过滤掉只有 Reply 的消息链
        filtered_chains = []
        for chain in message_chains:
            if len(chain) == 1 and isinstance(chain[0], Reply):
                logger.debug(f"丢弃只有引用的消息块: {chain[0]}")
                continue
            filtered_chains.append(chain)
        message_chains[:] = filtered_chains

        if not message_chains:
            return

        # 2. 处理 sticker
        new_chains = []

        for chain in message_chains:
            elements = chain.message_list
            # 找出所有表情的位置
            sticker_indices = [i for i, e in enumerate(elements) if isinstance(e, Sticker)]

            if not sticker_indices:
                # 没有表情，直接保留原链
                new_chains.append(chain)
                continue

            # 1. 按概率决定哪些表情保留
            keep_indices = []
            for idx in sticker_indices:
                if random.random() < self.sticker_probability:
                    keep_indices.append(idx)
                else:
                    logger.debug(f"删除 sticker: {elements[idx]}")

            # 2. 原链中移除所有表情（无论是否保留），剩下的元素组成一个新链
            remaining_elements = [e for i, e in enumerate(elements) if i not in sticker_indices]

            # 3. 处理剩余链：如果它只包含一个 Reply（即空引用），则丢弃；否则加入
            if remaining_elements:
                if len(remaining_elements) == 1 and isinstance(remaining_elements[0], Reply):
                    logger.debug(f"丢弃只有引用的消息块: {remaining_elements[0]}")
                else:
                    new_chains.append(MessageChain(remaining_elements))

            # 4. 每个保留的表情单独成为一个消息链（独立成行）
            for idx in keep_indices:
                new_chains.append(MessageChain([elements[idx]]))

        # 5. 随机调整表情链的位置（如果启用）
        if self.random_position:
            # 分离出表情链和非表情链
            non_sticker_chains = [
                c for c in new_chains
                if not (len(c.message_list) == 1 and isinstance(c.message_list[0], Sticker))
            ]
            sticker_chains = [
                c for c in new_chains
                if len(c.message_list) == 1 and isinstance(c.message_list[0], Sticker)
            ]
            new_chains = non_sticker_chains.copy()
            for sc in sticker_chains:
                pos = random.randint(0, len(new_chains))
                new_chains.insert(pos, sc)
        # 如果未启用随机位置，表情链会按处理顺序紧跟原链（默认行为）

        message_chains.clear()
        message_chains.extend(new_chains)
        logger.debug(f"Sticker 处理完成，消息块数量: {len(message_chains)}")
