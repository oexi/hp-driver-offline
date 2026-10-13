# HP 键盘网页驱动（离线版）

抓取自 https://hub.hpgthub.com/ ，2026-10-13。`site/` 内的网页驱动代码版权归原厂商所有，本仓库仅作离线备份。

## 使用

```bash
python3 serve.py
```

会自动用默认浏览器打开 http://127.0.0.1:8787/ 。必须用 Chrome / Edge（Firefox 不支持 WebHID）。
不能直接双击 `site/index.html`：WebHID 只能在 localhost 或 https 下工作。

指定端口：`python3 serve.py 9000`；不自动打开浏览器：加 `--no-browser`。

## 离线时不可用的功能

- 检查固件更新（请求 hubx.pro）
- 更新日志
- PC 端驱动下载链接

改键、灯效、宏等配置功能都是通过 WebHID 直接和键盘通信，离线可用。

## Linux 权限

键盘的 hidraw 设备需要普通用户可读写，已在 `/etc/udev/rules.d/99-hp-keyboard.rules` 添加：

```
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="258a", ATTRS{idProduct}=="010c", MODE="0666"
```

## 更新到网站最新版本

```bash
rm -rf site && python3 -I update.py https://hub.hpgthub.com/ site
```
