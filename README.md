# Takanashi-Hoshino API

一个基于Node.js和Express的图片API服务，提供按宽高比筛选的随机图片访问功能。

## 功能介绍

本项目主要包含两个部分：

1. 图片整理脚本 - 对图片按宽高比进行分类整理
2. API服务 - 提供按宽高比参数随机返回图片的接口

## 项目结构

```
.
├── img/                 # 整理后的图片文件夹
├── nosortimgs/          # 待整理的图片文件夹
├── config.json          # 配置文件（端口设置）
├── imgs.json            # 图片索引文件
├── index.js             # API服务主文件
├── sort_img.py          # 图片整理脚本
└── README.md            # 项目说明文档
```

## 图片整理脚本

### 功能

- 扫描`nosortimgs`文件夹中的图片
- 根据图片的宽高比自动分类到不同的子文件夹中
- 生成`imgs.json`索引文件，记录所有图片的信息

### 支持的宽高比

- 16:9
- 9:16
- 4:3
- 3:4
- 3:2
- 2:3
- 1:1 (正方形)
- 21:9
- 9:21
- 以及其他自定义比例

### 使用方法

```bash
python sort_img.py
```

脚本会自动处理图片并生成索引文件。

## API服务

### 启动服务

1. 安装依赖：
```bash
npm install express
```

2. 启动服务：
```bash
node index.js
```

服务将运行在配置文件中指定的端口（默认为20009）。

### 接口说明

#### 获取指定宽高比的随机图片

```
GET /api/img/Takanashi-Hoshino?ratio={宽高比}
```

示例：
- `http://localhost:20009/api/img/Takanashi-Hoshino?ratio=16_9` - 获取16:9的随机图片
- `http://localhost:20009/api/img/Takanashi-Hoshino?ratio=3_4` - 获取3:4的随机图片

接口将重定向到实际的图片地址。

### 响应码说明

- 200: 成功重定向到图片
- 400: 缺少ratio参数
- 404: 未找到指定宽高比的图片

## 配置文件

### config.json

```json
{
    "port": 20009
}
```

设置API服务运行的端口号。

## 许可证

MIT