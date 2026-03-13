# Performagent

## 启动说明（天气与定位功能）

天气和定位依赖代理服务，请按以下步骤操作：

1. 进入 server 目录并启动代理：`cd server && npm install && npm start`
2. 在浏览器打开：**http://localhost:3001/index.html**（不要用 file:// 直接打开）

若仍失败，请检查 `server/.env` 中 `AMAP_KEY` 是否已配置且高德控制台已开通「Web 服务」权限（天气、地理编码、逆地理编码）。
