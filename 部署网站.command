#!/bin/bash
# 双击：重新生成网页，并部署到 https://fitness.liangdeer.com
cd "$(dirname "$0")" || exit 1
echo "=== 部署健身知识手册 ==="
if command -v python3 >/dev/null 2>&1 && python3 -c "import markdown" 2>/dev/null; then
  python3 build.py || { echo "生成失败，把上面的报错发给 Claude。"; read -n 1 -s -r -p "按任意键关闭"; exit 1; }
else
  echo "（没装 python3 的 markdown 包，跳过重新生成，直接部署现有的 site/index.html）"
fi
if ! command -v npx >/dev/null 2>&1; then
  echo "没找到 Node.js。先装 Node.js（https://nodejs.org），再双击这个文件。"
  read -n 1 -s -r -p "按任意键关闭"; exit 1
fi
npx --yes wrangler@4 deploy
status=$?
echo
if [ $status -eq 0 ]; then
  echo "部署完成。打开 https://fitness.liangdeer.com 看看（第一次绑定域名可能要等几分钟）。"
else
  echo "部署没成功，把上面的报错发给 Claude。"
fi
read -n 1 -s -r -p "按任意键关闭"
