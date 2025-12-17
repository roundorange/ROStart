@echo off
title 文件服务器

echo 本机IP...
ipconfig | findstr "IPv4"

echo.
echo 启动网站服务器...
python -m http.server 50020  --directory ./src