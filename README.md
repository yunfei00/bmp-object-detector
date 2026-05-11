# bmp-object-detector

一个使用 **OpenCV 传统图像处理**（非深度学习）来检测 BMP 图片中物体并绘制矩形框的 Python 工程。

## 项目简介

当前工程支持两种使用方式：

1. 命令行检测（detect）
2. Windows 桌面图形界面（PySide6 GUI）

基础检测流程：

1. 灰度化
2. 高斯去噪
3. 阈值分割（Otsu / Adaptive / Manual）
4. 轮廓查找
5. 面积过滤
6. `boundingRect` 计算外接矩形
7. 在图像副本上绘制矩形框

最终可输出：
- 标注图：`result.png`
- 检测结果：`result.json`

## 安装方法

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e .[dev]
```

## 命令行运行示例

```bash
python -m bmp_object_detector detect --input samples/test.bmp --output output
```

查看命令帮助：

```bash
python -m bmp_object_detector --help
```

## GUI 使用说明

```bash
pip install -e .
python -m bmp_object_detector gui
```

GUI 功能包括：打开 BMP、参数配置、执行检测、结果表格显示、保存标注图、保存 JSON、清空结果。

新增交互能力：
- 支持在图片区域点击检测框，自动高亮并定位右侧结果表格对应行。
- 支持点击右侧结果表格行，反向高亮图片中的对应检测框并尽量居中显示。
- 图片与表格的选中状态双向联动，点击空白区域可取消当前选中。

## 输出 JSON 格式说明

`output/result.json` 的结构如下：

```json
{
  "input": "samples/test.bmp",
  "image_width": 640,
  "image_height": 480,
  "count": 2,
  "boxes": [
    {"x": 50, "y": 60, "w": 120, "h": 90, "area": 10800},
    {"x": 260, "y": 120, "w": 80, "h": 140, "area": 11200}
  ]
}
```

## Windows EXE 自动打包与发布（GitHub Actions）

- 当 `main` 分支发生 push 后，Actions 会自动构建 `BMPObjectDetector.exe`，可在对应 Workflow 的 Artifacts 下载测试构建产物。
- 当 push 符合 `v*.*.*` 的 tag（例如 `v0.1.0`）后，Actions 会自动创建 GitHub Release，并上传正式版 `BMPObjectDetector.exe` 到 Release Assets。

发布示例：

```bash
git tag v0.1.0
git push origin v0.1.0
```

如果需要重新发布同一个版本：

```bash
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0
git tag v0.1.0
git push origin v0.1.0
```
