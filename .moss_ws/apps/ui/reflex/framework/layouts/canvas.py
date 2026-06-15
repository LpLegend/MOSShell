import reflex as rx
from PIL import Image

from framework.helpers.mixin import NameMixin


class CanvasLayout(rx.ComponentState, NameMixin):
    """Ghost 的画布 —— 左右分栏，文字在左边流式书写，图片在右边浮现。"""

    title: str = ""
    subtitle: str = ""
    tags: list[str] = []
    body: str = ""  # markdown
    images: list[Image.Image] = []

    @classmethod
    def name(cls) -> str:
        return "canvas"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.hstack(
            # ── 左栏：文字 ──
            rx.vstack(
                rx.skeleton(
                    rx.heading(cls.title, size="8", weight="bold"),
                    width="100%",
                    height="48px",
                    loading=cls.title == "",
                ),
                rx.skeleton(
                    rx.text(cls.subtitle, color_scheme="gray", size="4"),
                    width="100%",
                    height="24px",
                    loading=cls.subtitle == "",
                ),
                rx.skeleton(
                    rx.hstack(
                        rx.foreach(cls.tags, lambda t: rx.badge(t, variant="soft")),
                        spacing="2",
                    ),
                    width="100%",
                    height="28px",
                    loading=cls.tags.length() == 0,
                ),
                rx.skeleton(
                    rx.markdown(cls.body),
                    width="100%",
                    height="200px",
                    loading=cls.body == "",
                ),
                flex="1",
                min_width="0",
                spacing="5",
            ),
            # ── 右栏：图片 ──
            rx.box(
                rx.skeleton(
                    rx.vstack(
                        rx.foreach(
                            cls.images,
                            lambda img: rx.image(
                                img,
                                width="100%",
                                height="auto",
                                border_radius="12px",
                            ),
                        ),
                        spacing="4",
                    ),
                    width="100%",
                    height="400px",
                    loading=cls.images.length() == 0,
                ),
                flex="1",
                min_width="0",
            ),
            width="100%",
            max_width="1200px",
            margin="0 auto",
            min_height="100vh",
            padding="64px 48px",
            align="start",
            spacing="8",
            **props,
        )
