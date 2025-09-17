@echo off
echo 正在启动热点聚焦系统...
echo.

echo 启动API服务器...
start /min python api_server.py
timeout /t 3 /nobreak >nul

echo 启动静态文件服务器...
start /min python static_server.py
timeout /t 2 /nobreak >nul

echo.
echo 系统启动完成！
echo API服务器: http://127.0.0.1:5000/
echo 前端页面: http://localhost:8080/index.html
echo.
echo 如果浏览器没有自动打开，请手动访问:
echo http://localhost:8080/index.html
echo.
pause