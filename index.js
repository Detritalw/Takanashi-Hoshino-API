const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();

// 读取配置文件
const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf-8'));
const port = config.port;

// 读取图片数据
const imageData = JSON.parse(fs.readFileSync(path.join(__dirname, 'imgs.json'), 'utf-8'));

// API路由：根据宽高比参数重定向到指定图片
app.get('/api/img/Takanashi-Hoshino', (req, res) => {
  const ratio = req.query.ratio;
  
  // 记录用户访问
  const timestamp = new Date().toISOString();
  const userAgent = req.get('User-Agent') || 'Unknown';
  const ip = req.ip || req.connection.remoteAddress;
  
  // 如果没有提供ratio参数，则从所有文件夹中随机选择一张图片
  if (!ratio) {
    // 将所有图片放入一个数组中
    const allImages = [];
    for (const ratioKey in imageData) {
      allImages.push(...imageData[ratioKey]);
    }
    
    // 随机选择一张图片
    const randomImage = allImages[Math.floor(Math.random() * allImages.length)];
    
    // 记录访问日志
    console.log(`[${timestamp}] 用户访问: IP=${ip}, User-Agent="${userAgent}", 请求类型=随机图片, 返回图片=${randomImage.path}`);
    
    // 重定向到图片路径
    res.redirect(`/${randomImage.path}`);
    return;
  }
  
  // 检查是否存在该宽高比的图片
  if (!imageData[ratio]) {
    // 记录访问日志
    console.log(`[${timestamp}] 用户访问: IP=${ip}, User-Agent="${userAgent}", 请求类型=指定宽高比, 宽高比=${ratio}, 结果=未找到图片`);
    return res.status(404).json({ error: `未找到宽高比为 ${ratio} 的图片` });
  }
  
  // 获取该宽高比下的所有图片
  const images = imageData[ratio];
  
  // 随机选择一张图片
  const randomImage = images[Math.floor(Math.random() * images.length)];
  
  // 记录访问日志
  console.log(`[${timestamp}] 用户访问: IP=${ip}, User-Agent="${userAgent}", 请求类型=指定宽高比, 宽高比=${ratio}, 返回图片=${randomImage.path}`);
  
  // 重定向到图片路径
  res.redirect(`/${randomImage.path}`);
});

// 静态文件服务，提供图片访问
app.use('/img', express.static(path.join(__dirname, 'img')));

// 启动服务器
app.listen(port, () => {
  console.log(`服务器运行在端口 ${port}`);
});