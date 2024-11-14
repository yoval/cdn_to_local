# 说明

使用`folium`绘制地图时，发现引用的cdn源`cdn.jsdelivr.net`、`netdna.bootstrapcdn.com` 打开速度都有问题。

鉴于都是在本地使用，干脆把cdn文件下载到本地了。

推荐直接开启代理使用

`python download_and_update_html.py "C:\Users\Administrator\Desktop\colored_china_provinces_map_with_amap.html"`

也可以在脚本中使用代理

`python download_and_update_html.py "C:\Users\Administrator\Desktop\colored_china_provinces_map_with_amap.html" --http-proxy "http://your.proxy.server:port" --https-proxy "https://your.proxy.server:port"` 



生成文件（与源`.html`文件同目录）

- `index_local.html`文件

将`.html`文件转换成本地后的文件

- `local`文件夹 

下载js、css的文件夹。
