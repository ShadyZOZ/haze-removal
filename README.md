# Haze Removal
Single Image Haze Removal Using Dark Channel Prior

## Usages

启动服务

```bash
$ python server.py
```

使用CLI

```bash
# 恢复图片
$ python main.py recover --image images/gugong.bmp
# 恢复并保存图片
$ python main.py recover --image images/gugong.bmp --save
# 清除用户上传图片
$ python main.py clean
# benchmark
$ python main.py benchmark --tries 10 --image images/forest1.jpg
```

## Docker Deploy

```bash
$ curl -O http://7vzsal.com1.z0.glb.clouddn.com/dehaze.tar.gz
$ tar -zxvf dehaze.tar.gz
$ docker build -t dehaze-server .
$ docker run -it --rm -p 5000:5000 --name my-dehaze-server dehaze-server
```

## 展示平台要求
运行中间结果　＋　除雾后的图
