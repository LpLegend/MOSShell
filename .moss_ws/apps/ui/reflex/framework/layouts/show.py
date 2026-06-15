import reflex as rx
from pydantic import BaseModel, Field

from framework.helpers.mixin import NameMixin


class NoteCard(BaseModel):
    """笔记卡片"""
    image_url: str = Field(default="", description="封面图片URL")
    title: str = Field(default="", description="笔记标题")
    author_name: str = Field(default="", description="作者昵称")
    author_avatar: str = Field(default="", description="作者头像URL")
    likes: str = Field(default="0", description="点赞数")


def _note_card(card) -> rx.Component:
    """单张笔记卡片"""
    return rx.box(
        # 封面图
        rx.cond(
            card.image_url != "",
            rx.image(
                src=card.image_url,
                width="100%",
                height="auto",
                border_radius="10px 10px 0 0",
                object_fit="contain",
                display="block",
            ),
            rx.box(
                rx.text("📷", size="6"),
                display="flex",
                align_items="center",
                justify_content="center",
                height="200px",
                background="#f5f5f5",
                border_radius="10px 10px 0 0",
            ),
        ),
        # 内容区
        rx.box(
            # 标题
            rx.text(
                card.title,
                size="2",
                weight="bold",
                color="#333",
                line_height="1.4",
                display="-webkit-box",
                overflow="hidden",
                text_overflow="ellipsis",
                style={
                    "-webkit-line-clamp": "2",
                    "-webkit-box-orient": "vertical",
                },
            ),
            # 作者信息 + 点赞
            rx.hstack(
                rx.hstack(
                    rx.cond(
                        card.author_avatar != "",
                        rx.image(
                            src=card.author_avatar,
                            width="20px",
                            height="20px",
                            border_radius="50%",
                            object_fit="cover",
                        ),
                        rx.box(
                            width="20px",
                            height="20px",
                            border_radius="50%",
                            background="#e8e8e8",
                        ),
                    ),
                    rx.text(
                        card.author_name,
                        size="1",
                        color="#999",
                        max_width="80px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.text("♥", size="1", color="#ff2442"),
                    rx.text(card.likes, size="1", color="#999"),
                    spacing="1",
                    align="center",
                ),
                width="100%",
                align="center",
                margin_top="8px",
            ),
            padding="8px 10px 12px",
        ),
        background="white",
        border_radius="10px",
        overflow="hidden",
        box_shadow="0 1px 4px rgba(0,0,0,0.08)",
        cursor="pointer",
        transition="transform 0.2s, box-shadow 0.2s",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 12px rgba(0,0,0,0.12)",
        },
        width="100%",
        min_width="0",
    )


def _waterfall_column(cards, is_odd: bool) -> rx.Component:
    """瀑布流单列"""
    return rx.vstack(
        rx.foreach(
            cards,
            lambda card, i: rx.box(
                _note_card(card),
                margin_top=rx.cond(i > 0, "12px", "0px"),
            ),
        ),
        width="50%",
        spacing="0",
    )


class ShowLayout(rx.ComponentState, NameMixin):
    """
    小红书风格瀑布流布局，适用于内容展示、图片笔记、社交分享等场景
    """
    # 笔记数据
    notes: list[NoteCard] = []

    # 页面信息
    page_title: str = ""
    tab_items: list[str] = []

    @classmethod
    def name(cls) -> str:
        return "xiaohongshu"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.box(
            # ===== 顶部导航栏 =====
            rx.box(
                rx.hstack(
                    rx.text(
                        cls.page_title,
                        size="4",
                        weight="bold",
                        color="#333",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.foreach(
                            cls.tab_items,
                            lambda tab: rx.text(
                                tab,
                                size="2",
                                color="#666",
                                padding="6px 14px",
                                border_radius="20px",
                                cursor="pointer",
                                _hover={"background": "#f5f5f5", "color": "#333"},
                            ),
                        ),
                        spacing="2",
                    ),
                    width="100%",
                    align="center",
                ),
                padding="12px 0",
                margin_bottom="16px",
                width="100%",
            ),

            # ===== 瀑布流内容区 =====
            rx.skeleton(
                rx.hstack(
                    # 左列（偶数索引）
                    rx.vstack(
                        rx.foreach(
                            cls.notes,
                            lambda card, i: rx.cond(
                                i % 2 == 0,
                                rx.box(
                                    _note_card(card),
                                    margin_bottom="12px",
                                    width="100%",
                                ),
                                rx.box(),
                            ),
                        ),
                        width="50%",
                        spacing="0",
                        min_width="0",
                    ),
                    # 右列（奇数索引）
                    rx.vstack(
                        rx.foreach(
                            cls.notes,
                            lambda card, i: rx.cond(
                                i % 2 == 1,
                                rx.box(
                                    _note_card(card),
                                    margin_bottom="12px",
                                    width="100%",
                                ),
                                rx.box(),
                            ),
                        ),
                        width="50%",
                        spacing="0",
                        min_width="0",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                width="100%",
                height="400px",
                loading=cls.notes.length() == 0,
            ),

            # 全局样式
            background="#f5f5f5",
            min_height="100vh",
            padding="0 24px 24px",
            width="100%",
            max_width="800px",
            margin="0 auto",
            **props,
        )
