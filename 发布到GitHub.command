#!/bin/bash
# 双击：把这个文件夹发布成 GitHub 公开仓库 Nicedeer66/fitness-handbook；以后改了内容再双击就是提交并推送。
cd "$(dirname "$0")" || exit 1
echo "=== 发布到 GitHub ==="
if ! command -v git >/dev/null 2>&1; then
  echo "没找到 git。在终端运行 xcode-select --install 装好后再双击。"; read -n 1 -s -r -p "按任意键关闭"; exit 1
fi
if [ ! -d .git ]; then
  git init -q -b main
fi
git add -A
git commit -q -m "${1:-更新健身知识手册}" || echo "（没有新的改动要提交）"
if git remote get-url origin >/dev/null 2>&1; then
  git push -u origin main
elif command -v gh >/dev/null 2>&1; then
  gh auth status >/dev/null 2>&1 || gh auth login
  gh repo create Nicedeer66/fitness-handbook --public --source=. --remote=origin --push \
    --description "健身知识手册：肌肉怎么长、每个部位怎么练、一周怎么排、怎么吃。每个结论标了研究来源和证据等级。" \
    --homepage "https://fitness.liangdeer.com"
else
  echo "没装 GitHub 命令行工具 gh。两种办法任选："
  echo "1. 运行 brew install gh 装好后再双击这个文件；"
  echo "2. 在 github.com 新建公开仓库 fitness-handbook（不要勾选添加 README），然后在终端进入这个文件夹运行："
  echo "   git remote add origin https://github.com/Nicedeer66/fitness-handbook.git && git push -u origin main"
fi
read -n 1 -s -r -p "按任意键关闭"
