#!/bin/bash

# 设置文件名
SCENE_FILE="scene2.go"

# 循环执行10次
for i in {1..10}
do
  echo "执行第 $i 次..."

  # 运行 scene2.go（注意：需确保每次都会生成 timings.csv）
  go run "$SCENE_FILE"

  # 检查是否生成 timings.csv
  if [ -f timings.csv ]; then
    mv timings.csv timings_$i.csv
    echo "已保存为 timings_$i.csv"
  else
    echo "未找到 timings.csv，跳过本次。"
  fi

  # 可选：等待1秒避免冲突
  sleep 1
done

echo "全部完成。"
