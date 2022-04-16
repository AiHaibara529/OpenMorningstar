client=$1     # 并发数
reps=5        # 测试次数
file=urls.txt # url文件
# -i 随机选择url -b 请求无需等待
# siege -c $client -r $reps -f $file -i -b
siege -c $client -r $reps https://morningstar529.com/nav/ -i -b
