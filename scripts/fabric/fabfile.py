from fabric import task
from invoke import Responder
import os
import sh
import subprocess
from dotenv import load_dotenv
import colorama
# NOTE: 因为.env的路径问题，所以本脚本只能通过shortcut.sh在根目录执行


def runcmd1(command):
    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, encoding="utf-8", timeout=1, universal_newlines=True)
    if ret.returncode == 0:
        print("success:", ret)
    else:
        print("error:", ret)


def runcmd2(command):
    process = subprocess.Popen(
        command.split(), stdout=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    print(output)
    if error:
        print(error)


def better_print(var):
    print(colorama.Fore.YELLOW + colorama.Style.BRIGHT +
          str(var) + colorama.Style.RESET_ALL)


env_path = os.getcwd() + "/.env"
load_dotenv(dotenv_path=env_path, verbose=True)
PASSWORD = os.getenv("PASSWORD")


@task()
def check(c):
    home_path = "~/"
    with c.cd(home_path):
        better_print("Let's Encrypt证书剩余时间: ")
        c.run('source ~/.zshrc && docker exec morningstar_nginx certbot certificates')
        better_print("=======================================================")
    print("Done!!")


@task()
def update(c):
    project_root_path = '~/morningstar'

    # 从Git拉取最新代码
    try:
        with c.cd(project_root_path):
            c.run('git checkout .')
            c.run('git pull')
    except:
        c.run('sudo rm -rf ~/morningstar/')
        c.run('git clone https://github.com/HenryJi529/OpenMorningstar.git ~/morningstar')

    # 暂停所有任务
    c.run('docker restart morningstar_django')

    # 安装依赖，迁移数据库，收集静态文件
    c.run('docker exec -it morningstar_django python3 -m pip install --upgrade pip -i https://pypi.douban.com/simple')
    c.run('docker exec -it morningstar_django python3 -m pip install -r /app/requirements.txt -i https://pypi.douban.com/simple')
    c.run('docker exec -it morningstar_django bash /production.sh')
    try:
        c.run('docker exec -it morningstar_django service supervisor start')
    except:
        c.run('docker exec -it morningstar_django service supervisor status')

    print("Done!!")


@task()
def backup(c):
    project_root_path = '~/morningstar'
    with c.cd(project_root_path):
        try:
            c.run('docker exec -it morningstar_django bash -c "mkdir /app/data/"')
        except:
            pass
        c.run('docker exec -it morningstar_django bash -c "python3 manage.py dumpdata --settings=Morningstar.settings.production > data/all.json"')
        c.run('sshpass -p ' + PASSWORD +
              ' scp -P 1022 ~/morningstar/data/all.json henry529@frp.morningstar529.com:~/Projects/OpenMorningstar/database')
    print("Done!!")


@task()
def restore(c):
    project_root_path = '~/morningstar'
    with c.cd(project_root_path):
        c.run('docker exec -it morningstar_django bash -c "python3 manage.py loaddata --settings=Morningstar.settings.production data/all.json"')
    print("Done!!")


@task()
def upgrade(c):
    home_path = "~/"
    with c.cd(home_path):
        """更新项目"""
        # 从Git拉取最新代码
        c.run('sudo rm -rf ~/morningstar/')
        c.run('git clone https://github.com/HenryJi529/OpenMorningstar.git ~/morningstar')
        print("更新代码...")

        def update_file_with_secret():
            c.run(
                "source ~/.zshrc && echo \"\nenvironment=DJANGO_SECRET_KEY='${DJANGO_SECRET_KEY}',EMAIL_HOST_PASSWORD='${EMAIL_HOST_PASSWORD}',TENCENT_SMS_APP_KEY='${TENCENT_SMS_APP_KEY}',RECAPTCHA_PUBLIC_KEY='${RECAPTCHA_PUBLIC_KEY}',RECAPTCHA_PRIVATE_KEY='${RECAPTCHA_PRIVATE_KEY}',QINIU_SECRET_KEY='${QINIU_SECRET_KEY}'\" >> ~/morningstar/deploy/django/supervise.conf")
            c.run(
                'source ~/.zshrc && sed -i "s/USERNAME/${USERNAME}/" ~/morningstar/deploy/_config/frp/frps.ini')
            c.run(
                'source ~/.zshrc && sed -i "s/PASSWORD/${PASSWORD}/" ~/morningstar/deploy/_config/frp/frps.ini')
        update_file_with_secret()
        print("添加密钥...")

        # 更新容器
        try:
            c.run('docker rm -f $(docker ps -aq | tr "\\n" " ")')  # NOTE: 删除全部容器
        except:
            pass

        order = input("是否同时更新所有包(Y/n): ")
        images_host = ["henry529/django", "henry529/nginx", "henry529/beancount", "henry529/tshock"]
        for image in images_host:
            try:
                c.run(f'docker rmi {image}')
            except:
                pass

        if order == 'n':
            pass
        else:
            images_others = ["niruix/sshwifty", "diygod/rsshub", "ghost", "gitea/gitea", "snowdreamtech/frps", "nextcloud", "mysql", "memcached", "registry.gitlab.com/timvisee/send",
                    "jellyfin/jellyfin", "registry", "portainer/portainer", "fauria/vsftpd", "redis", "alpine", "nginx", "ubuntu",]
            for image in images_others:
                try:
                    c.run(f'docker rmi {image}')
                except:
                    pass

        c.run('docker image prune -a')

        if order == 'n':
            pass
        else:
            for image in images_others:
                try:
                    c.run(f'docker pull {image}')
                except:
                    pass

        c.run('source ~/.zshrc && cd ~/morningstar/deploy; docker-compose build && docker-compose up -d')
        print("部署项目...")

        # 配置django
        c.run('docker exec -it morningstar_django bash /production.sh')
        try:
            c.run('docker exec -it morningstar_django service supervisor start')
        except:
            c.run('docker exec -it morningstar_django service supervisor status')
        # 解决数据库无连接错误
        c.run('docker exec -it morningstar_django supervisorctl restart django')

        # 配置nginx
        c.run('docker exec morningstar_nginx bash /start.sh')
        c.run('docker exec -it morningstar_nginx certbot --nginx')

    print("Done!!")

# ================================================================


@task()
def backupDockerVolume(c):
    home_path = "~/"
    with c.cd(home_path):
        c.run('docker volume ls')
        volumeName = input("请输入卷名: ")
        print(f"volumeName: {volumeName}")
        cmd = f'docker run --rm -v deploy_{volumeName}:/volume -v ~/backup/docker_volume:/backup alpine sh -c "tar -C /volume -cvzf /backup/{volumeName}.tar.gz ./"'
        better_print(cmd)
        c.run(cmd)


@task()
def restoreDockerVolume(c):
    home_path = "~/"
    with c.cd(home_path):
        c.run('ls /home/jeep_jipu/backup/docker_volume/')
        volumeName = input("请输入卷名: ")
        print(f"volumeName: {volumeName}")
        cmd = f'docker run --rm -v deploy_{volumeName}:/volume -v ~/backup/docker_volume:/backup alpine sh -c "rm -rf /volume/* ; tar -C /volume/ -xzvf /backup/{volumeName}.tar.gz"'
        better_print(cmd)
        c.run(cmd)


@task()
def updatePackage(c):
    home_path = "~/"
    with c.cd(home_path):
        """发布包(dockerhub与ghcr)"""
        packages = ["nginx", "beancount", "tshock", "django"]
        for package in packages:
            try:
                c.run(f'docker rmi ghcr.io/henryji529/morningstar-{package}')
                c.run(
                    f'docker rmi dockerhub.morningstar529.com/morningstar-{package}')
            except:
                pass
            c.run(
                f'docker tag henry529/{package} ghcr.io/henryji529/morningstar-{package}')
            c.run(
                f'docker tag henry529/{package} dockerhub.morningstar529.com/morningstar-{package}')
            c.run(f'docker push ghcr.io/henryji529/morningstar-{package}')
            c.run(f'docker push henry529/{package}')
            c.run(
                f'docker push dockerhub.morningstar529.com/morningstar-{package}')

    print("Done!!")
