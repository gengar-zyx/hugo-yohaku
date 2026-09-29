# Yohaku · 余白

基于 PaperMod 派生的独立 Hugo 主题。暖纸色、梅红点缀、衬线正文与轻量文章列表，面向中文长文和技术笔记。

## 安装

需要 Hugo **0.165.0 或以上**。无需 Node、Tailwind、网络字体服务或 PaperMod 运行时依赖。

在已有 Hugo 站点的根目录执行（私有仓库需要已获授权的 GitHub 账号）：

```sh
git submodule add https://github.com/gengar-zyx/hugo-yohaku.git themes/yohaku
```

在站点配置中启用主题：

```yaml
theme: ["yohaku"]
pagination:
  pagerSize: 5
markup:
  highlight:
    noClasses: false
```

克隆使用此主题的站点后，运行 `git submodule update --init --recursive` 获取主题。CI 和托管平台也需要有权读取此私有仓库；不要把访问令牌写进子模块 URL 或提交到配置文件。子模块共享配置使用 HTTPS URL；开发者本机的主题仓库 `origin` 可以使用 SSH URL `git@github.com:gengar-zyx/hugo-yohaku.git`。

更新主题时，在站点根目录执行 `git -C themes/yohaku pull --ff-only origin main`，再提交站点中的子模块版本变更。此仓库只包含 Yohaku；如需切回 PaperMod，请在站点中另行安装 PaperMod 并修改 `theme`。已有内容、路径和 front matter 无需迁移。

## 配置与内容

沿用 PaperMod 参数，包括 `homeInfoParams`、`mainSections`、`socialIcons`、`defaultTheme`、`ShowReadingTime`、`ShowPostNavLinks`、`ShowCodeCopyButtons`、`showtoc`、`tocopen` 和 `fuseOpts`。搜索仍需首页 JSON 输出及 `layout: search` 页面，归档使用 `layout: archives`。

颜色与字体变量在 `assets/css/core/theme-vars.css`；页面样式在 `assets/css/extended/yohaku.css`。默认跟随系统外观，用户切换后保留选择。正文 17px / 1.85，内容最大宽度 720px，移动端边距 20px。

支持站点的 `assets/css/extended/*.css` 扩展，但保留名称 `custom.css` 与 `alerts.css` 不参与 Yohaku 打包，以免历史 PaperMod 样式覆盖主题；请为新增扩展使用其他文件名。

中文使用本地 Noto Serif SC 400/500，拉丁字母优先 Georgia；系统没有 Georgia 时使用 Noto 字体及其回退链。界面与元数据使用系统 sans / mono 字体。字体加载失败时仍可阅读。中文不使用合成粗体，技术文章不启用首字下沉或自动章节编号。

提示块支持 NOTE / TIP / IMPORTANT / WARNING / CAUTION。字体、图标与脚本均不依赖参考站；文章中既有的外部图片仍按原内容地址加载。不会自动发布草稿。

## 本地预览

仓库内附有通用示例站点，不包含个人博客内容。在**主题仓库根目录**执行：

```sh
hugo server --source exampleSite \
  --themesDir "$(dirname "$PWD")" --theme "$(basename "$PWD")" \
  --cacheDir /tmp/yohaku-cache
```

上述命令自动采用当前目录名，克隆为 `hugo-yohaku`、`yohaku` 或其他名称均可。添加 `-D` 可预览示例草稿；不加时草稿不发布。示例配置刻意不写死主题目录名。在自己的 Hugo 站点中，则直接使用 `hugo server` 预览。

## 来源与许可

- 派生自 [PaperMod](https://github.com/adityatelange/hugo-PaperMod)，提交 `d3768854d00ad003b0a8dbdba254ce9224377a01`。保留根目录 `LICENSE` 和原 CSS / JavaScript 版权声明，主题代码遵循 MIT 许可。
- 视觉原则参考 [Yohaku](https://yohaku.innei.dev) 与其[长文样例](https://yohaku.innei.dev/demos/demo-post.html)，于 2026-09-09 观察。此主题为独立实现，不代表参考站作者发布或背书；未复制其文章、头像或品牌资产。
- [Noto Serif SC](https://github.com/google/fonts/tree/main/ofl/notoserifsc)，SIL Open Font License 1.1；许可证位于 `static/fonts/noto-serif-sc/OFL.txt`。经 Google Fonts CSS2 获取 400/500 字重的 WOFF2 unicode-range 分片，101 个共享文件共 6,027,992 字节，浏览器按需加载。字体地址已改为本地相对路径。

## 构建检查

在主题仓库根目录执行（Python 3）：

```sh
python3 tests/check_standalone.py
# 可选：指定 Hugo 二进制
python3 tests/check_standalone.py --hugo /path/to/hugo
```

检查脚本将主题复制到临时目录，以不同目录名独立构建示例站点的生产与草稿版本，不依赖父级博客或 PaperMod。复用 `tests/check_build.py` 检查站内链接、唯一搜索索引、字体相对路径、101 个字体文件、许可证、RSS 与 404，并确认草稿只进入草稿版本。缓存与构建产物均在临时目录，结束后自动清理。

已有站点也可以构建后运行 `python3 /path/to/hugo-yohaku/tests/check_build.py /path/to/build`。该检查要求首页输出 JSON 搜索索引。
