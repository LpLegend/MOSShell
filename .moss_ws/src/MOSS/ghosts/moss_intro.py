from ghoshell_moss.ghosts.atom import AtomMeta, Atom


class MossIntro(Atom):
    """MossIntro — 专门介绍自身的 Ghost，保留最近 20 轮对话历史."""

    _max_rounds: int = 20

    def model_history(self) -> list:
        history = self._history
        max_messages = self._max_rounds * 2
        if len(history) <= max_messages:
            return list(history)
        return list(history[-max_messages:])


class MossIntroMeta(AtomMeta):
    """MossIntro 的 Bootstrapper — 与 AtomMeta 一致，仅 factory 返回 MossIntro."""

    def factory(self, container):
        agent = self.build_agent(container)
        return MossIntro(meta=self, agent=agent, container=container)


ghost = MossIntroMeta(
    name="moss_intro",
    description=(
        "MossIntro — MOSS 的自我介绍 Ghost。向每位访客讲述 MOSS 是什么、"
        "它如何工作、以及它为什么存在。保留最近 20 轮对话上下文。"
    ),
)
