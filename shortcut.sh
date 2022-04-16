# 检视信息
check() {
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric --prompt-for-login-password -p check
}

# 本地开发
dev() {
	# python scripts/initialize/main.py # 开发测试数据生成
	python manage.py makemigrations && python manage.py migrate
	python manage.py rebuild_index --noinput
	# python manage.py crontab add # 启动定时任务
	python manage.py runserver 127.0.0.1:8000
}

# 代码测试
coverage() {
	COVERAGE=$(pwd)/env/bin/coverage
	${COVERAGE} erase --rcfile=scripts/coverage/.coveragerc
	${COVERAGE} run --rcfile=scripts/coverage/.coveragerc manage.py test Morningstar/ apps/ --failfast --keepdb
	${COVERAGE} report --rcfile=scripts/coverage/.coveragerc
	${COVERAGE} html --rcfile=scripts/coverage/.coveragerc
	live-server scripts/coverage/coverage_html_report
}

# 更新依赖
updateDep() {
	pip freeze >requirements.txt && pip freeze >deploy/django/requirements.txt
	pipdeptree -fl >pipdeptree.txt
}

# 更新静态
updateStatic() {
	ci_time=$(date "+%Y.%m.%d %H:%M")
	python manage.py collectstatic --noinput
	cd static/ && git add -A && git ci "💩update: ${ci_time}" && git push github main && cd ../
}

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# 远程同步
updateProd() {
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p update
}

# 整体更新
upgradeProd() {
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p upgrade
}

# 数据备份
backupProd() {
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p backup
}

# 数据还原
restoreProd() {
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p restore
}

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

backupDockerVolume() {
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p backupDockerVolume
}

restoreDockerVolume() {
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p restoreDockerVolume
}

publicPackage() {
	echo "更新生产环境下的容器..."
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p updatePackage
	echo "更新开发环境下的容器..."
	read -s -n1 -p "按任意键继续..."
	docker compose -f deploy/example_dev.yml up --build -d
	docker push henry529/dev
	docker tag henry529/dev ghcr.io/henryji529/morningstar-dev && docker push ghcr.io/henryji529/morningstar-dev
	docker tag henry529/dev dockerhub.morningstar529.com/morningstar-dev && docker push dockerhub.morningstar529.com/morningstar-dev
}

publicCoverage() {
	cd scripts/coverage/coverage_html_report/ && vercel --prod
}

#==================================================================

cat <<_haibara_
$(figlet Morningstar)
_haibara_

echo "运行命令:
============================================================
a. backupDockerVolume();
b. restoreDockerVolume();
c. publicPackage();
d. publicCoverage();
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
0. check();
1. dev();
2. coverage();
3. updateDep();
4. updateStatic();
5. updateProd();
6. upgradeProd();
7. backupProd();
8. restoreProd();
"
read -p "输入序号(a-e|0-8): " order

start_time=$(date +%s)

# NOTE: 虚拟环境几乎是必须的
source $(pwd)/env/bin/activate

case $order in
a) backupDockerVolume ;;
b) restoreDockerVolume ;;
c) publicPackage ;;
d) publicCoverage ;;
# ==========================
0) check ;;
1) dev ;;
2) coverage ;;
3) updateDep ;;
4) updateStatic ;;
5) updateProd ;;
6) upgradeProd ;;
7) backupProd ;;
8) restoreProd ;;
*) echo "输入错误" ;;
esac
end_time=$(date +%s)
during=$((end_time - start_time))
echo "\033[33m总运行时间: $during 秒\033[0m"
fortune | lolcat
