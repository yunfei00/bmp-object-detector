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
