---
title: 技术笔记的代码与表格
date: 2026-01-01
description: 演示代码高亮、表格、目录和提示块。
categories: [技术]
tags: [Hugo, 笔记]
---

把操作步骤整理成一篇笔记，可以减少下一次寻找答案的时间。

## 代码示例

```python
def greet(name: str) -> str:
    return f"你好，{name}！"

print(greet("余白"))
```

代码块支持复制，较长的行在容器内横向滚动。

## 配置速查

| 设置 | 作用 |
| --- | --- |
| `defaultTheme: auto` | 默认跟随系统外观 |
| `ShowReadingTime: true` | 显示预计阅读时间 |
| `showtoc: true` | 显示文章目录 |

> [!TIP]
> 搜索页面需要首页的 JSON 输出。示例配置已经启用。

> [!WARNING]
> 预览草稿时使用 `hugo server -D`；发布前确认文章的 `draft` 状态。
