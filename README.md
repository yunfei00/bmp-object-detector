# bmp-object-detector

一个使用 **OpenCV 传统图像处理**（非深度学习）来检测 BMP 图片中物体并绘制矩形框的 Python 工程。

## 项目简介

第一阶段实现了针对 `.bmp` 图片的目标检测流程：

1. 灰度化
2. 高斯去噪
3. 阈值分割（Otsu）
4. 轮廓查找
5. 过滤过小区域
6. 计算外接矩形
7. 在原图上绘制矩形框

最终输出：
- 标注图：`output/result.png`
- 检测结果：`output/result.json`

## 安装方法

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e .[dev]
```

## 运行示例

```bash
python -m bmp_object_detector detect --input samples/test.bmp --output output
```

查看命令帮助：

```bash
python -m bmp_object_detector --help
```

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

字段含义：
- `input`: 输入图片路径
- `image_width`, `image_height`: 原图尺寸
- `count`: 检测到的目标数量
- `boxes`: 每个目标的外接矩形信息
  - `x`, `y`: 左上角坐标
  - `w`, `h`: 矩形宽高
  - `area`: 矩形面积 (`w * h`)

## 下一阶段计划

第二阶段将引入 **YOLO 自定义目标检测**，包括：
- 数据集标注与训练流程
- 模型推理接口
- 与当前 OpenCV 流程并行对比
- 更复杂场景下的精度评估
