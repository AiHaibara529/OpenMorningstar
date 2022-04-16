.PHONY: venv dev coverage updateDep updateStatic

PWD := $(shell pwd)
PYTHON := ${PWD}/env/bin/python3
PIP := ${PWD}/env/bin/pip
COVERAGE := ${PWD}/env/bin/coverage
FAB := ${PWD}/env/bin/fab
CURRENT_TIME := $(shell date "+%Y.%m.%d %H:%M")
PIPDEPTREE := ${PWD}/env/bin/pipdeptree


# 激活环境
venv: ${PWD}/env/bin/activate
	@zsh -c "source ${PWD}/env/bin/activate"

# 本地开发
dev: venv
	@${PYTHON} manage.py makemigrations && ${PYTHON} manage.py migrate
	@${PYTHON} manage.py rebuild_index --noinput
	@${PYTHON} manage.py crontab add
	@${PYTHON} manage.py runserver 0:8000

# 代码测试
coverage: venv ${COVERAGE}
	@${COVERAGE} erase --rcfile=scripts/coverage/.coveragerc
	@${COVERAGE} run --rcfile=scripts/coverage/.coveragerc manage.py test Morningstar/ apps/ --failfast --keepdb
	@${COVERAGE} report --rcfile=scripts/coverage/.coveragerc
	@${COVERAGE} html --rcfile=scripts/coverage/.coveragerc
	@live-server scripts/coverage/coverage_html_report

# 更新依赖
updateDep : venv
	@${PIP} freeze > requirements.txt && ${PIP} freeze > deploy/django/requirements.txt && ${PIPDEPTREE} -fl > pipdeptree.txt

# 更新静态
updateStatic: venv
	@${PYTHON} manage.py collectstatic --noinput && cd static/ && git add -A && git ci "💩update: ${CURRENT_TIME}" && git push github main && cd ../;

