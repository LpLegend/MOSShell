import base64
import re
import webbrowser

from ghoshell_moss.core import PyChannel

__all__ = ["new_mermaid_chan"]

_MERMAID_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'default'
  }});
</script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 100%; height: 100%;
    background: #fff;
  }}
  body {{
    display: flex; flex-direction: column;
  }}
  h1 {{
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 1.5rem; padding: 1rem;
    text-align: center;
    flex-shrink: 0;
  }}
  .wrapper {{
    flex: 1;
    display: flex; justify-content: center; align-items: center;
    min-height: 0;
  }}
  .mermaid {{
    height: 100%;
    display: flex; justify-content: center; align-items: center;
  }}
  .mermaid svg {{
    height: 100% !important;
    width: auto !important;
    max-width: none !important;
  }}
</style>
</head>
<body>
  <h1>{title}</h1>
  <div class="wrapper">
    <pre class="mermaid">
{code}
    </pre>
  </div>
</body>
</html>"""


def new_mermaid_chan() -> PyChannel:
    channel = PyChannel(
        name="mermaid",
        description="在浏览器中绘制 Mermaid 架构图、流程图等",
        blocking=True,
    )

    channel.build.command()(draw_mermaid)

    return channel


async def draw_mermaid(title: str = "MOSShell Diagram", text__: str = "") -> str:
    """在浏览器中绘制 Mermaid 图表

    Args:
        title: 图表标题
        text__: Mermaid 代码
    CTML:
        注意使用 cdata: <draw_mermaid title="xx"><![CDATA[...]]></draw_mermaid>

    Returns:
        状态消息
    """
    code = text__.strip()
    code = re.sub(r"^```(?:mermaid)?\s*\n?", "", code)
    code = re.sub(r"\n?```\s*$", "", code)
    code = code.replace("\\n", "<br/>")

    html = _MERMAID_HTML.replace("{title}", title).replace("{code}", code)
    b64 = base64.b64encode(html.encode("utf-8")).decode("ascii")
    url = f"data:text/html;charset=utf-8;base64,{b64}"
    webbrowser.open(url)
    return f"已在浏览器中打开 Mermaid 图表: {title}"
