# Mode 的 main channel。
# Mode 的 __main__ channel 是唯一的生效 main channel。
#
# 两种构建模式：
#
# 1. 从零构建（推荐 — 独立 mode）：
#    from ghoshell_moss import new_default_shell_main_channel
#    main = new_default_shell_main_channel(description="...")
#    # 在 main 上追加 command 或 compose sub-channel...
#
# 2. 复用全局 main（mode 作为全局的增量改造）：
#    from MOSS.manifests.channels import main
#    # 在 main 上追加改造...

from MOSS.manifests.channels import main

from ghoshell_moss.bridges.zmq_channel import ZMQChannelProxy

# 这是一条指引的文本：jetarm连接点
main.import_channels(ZMQChannelProxy(
    name="jetarm",
    address='tcp://127.0.0.1:9527',
))