from fastapi import APIRouter, Query
from typing import Annotated

router = APIRouter(prefix="/cheatsheet", tags=["Cheatsheet"])

CHEATSHEET_DATA = {
    "linux": [
        {
            "command": "ls -lah",
            "description": "列出文件详情（含隐藏文件）",
            "example": "ls -lah /var/log",
        },
        {
            "command": "ps aux",
            "description": "查看所有进程",
            "example": "ps aux | grep nginx",
        },
        {"command": "df -h", "description": "查看磁盘使用情况", "example": "df -h"},
        {
            "command": "du -sh *",
            "description": "查看当前目录各文件大小",
            "example": "du -sh /home/*",
        },
        {"command": "top / htop", "description": "实时查看系统资源", "example": "htop"},
        {
            "command": "netstat -tunlp",
            "description": "查看监听端口",
            "example": "netstat -tunlp | grep 80",
        },
        {
            "command": "systemctl status <service>",
            "description": "查看服务状态",
            "example": "systemctl status sshd",
        },
        {
            "command": "journalctl -u <service>",
            "description": "查看服务日志",
            "example": "journalctl -u nginx --since today",
        },
        {
            "command": "find / -name <file>",
            "description": "查找文件",
            "example": "find / -name '*.log'",
        },
        {
            "command": "chmod 755 <file>",
            "description": "修改文件权限",
            "example": "chmod 755 script.sh",
        },
        {
            "command": "chown user:group <file>",
            "description": "修改文件属主",
            "example": "chown root:root /etc/passwd",
        },
        {
            "command": "tar -czvf archive.tar.gz <dir>",
            "description": "压缩目录",
            "example": "tar -czvf backup.tar.gz /data",
        },
        {
            "command": "tar -xzvf archive.tar.gz",
            "description": "解压 tar.gz",
            "example": "tar -xzvf backup.tar.gz -C /tmp",
        },
        {
            "command": "grep -rn 'pattern' <dir>",
            "description": "递归搜索文本",
            "example": "grep -rn 'error' /var/log",
        },
        {
            "command": "awk '{print $1}' <file>",
            "description": "文本处理提取列",
            "example": "awk '{print $1}' access.log",
        },
    ],
    "docker": [
        {
            "command": "docker ps",
            "description": "列出运行中的容器",
            "example": "docker ps -a",
        },
        {
            "command": "docker images",
            "description": "列出本地镜像",
            "example": "docker images",
        },
        {
            "command": "docker build -t <tag> .",
            "description": "构建镜像",
            "example": "docker build -t myapp:latest .",
        },
        {
            "command": "docker run -d -p 80:80 <image>",
            "description": "后台运行容器",
            "example": "docker run -d -p 8080:80 nginx",
        },
        {
            "command": "docker exec -it <container> bash",
            "description": "进入容器终端",
            "example": "docker exec -it nginx bash",
        },
        {
            "command": "docker logs -f <container>",
            "description": "查看容器日志",
            "example": "docker logs -f --tail 100 nginx",
        },
        {
            "command": "docker stop <container>",
            "description": "停止容器",
            "example": "docker stop nginx",
        },
        {
            "command": "docker rm <container>",
            "description": "删除容器",
            "example": "docker rm nginx",
        },
        {
            "command": "docker rmi <image>",
            "description": "删除镜像",
            "example": "docker rmi nginx:latest",
        },
        {
            "command": "docker-compose up -d",
            "description": "启动 Compose 服务",
            "example": "docker-compose up -d",
        },
        {
            "command": "docker-compose down",
            "description": "停止并移除 Compose 服务",
            "example": "docker-compose down -v",
        },
        {
            "command": "docker system prune",
            "description": "清理无用数据",
            "example": "docker system prune -a",
        },
        {
            "command": "docker inspect <container>",
            "description": "查看容器详情",
            "example": "docker inspect nginx",
        },
        {
            "command": "docker network ls",
            "description": "列出网络",
            "example": "docker network ls",
        },
        {
            "command": "docker volume ls",
            "description": "列出卷",
            "example": "docker volume ls",
        },
    ],
    "kubernetes": [
        {
            "command": "kubectl get pods",
            "description": "查看 Pod 列表",
            "example": "kubectl get pods -n kube-system",
        },
        {
            "command": "kubectl get nodes",
            "description": "查看节点",
            "example": "kubectl get nodes -o wide",
        },
        {
            "command": "kubectl describe pod <pod>",
            "description": "查看 Pod 详情",
            "example": "kubectl describe pod nginx-xxx",
        },
        {
            "command": "kubectl logs <pod>",
            "description": "查看 Pod 日志",
            "example": "kubectl logs -f nginx-xxx",
        },
        {
            "command": "kubectl exec -it <pod> -- bash",
            "description": "进入 Pod 容器",
            "example": "kubectl exec -it nginx-xxx -- bash",
        },
        {
            "command": "kubectl apply -f <file>.yaml",
            "description": "应用配置",
            "example": "kubectl apply -f deployment.yaml",
        },
        {
            "command": "kubectl delete -f <file>.yaml",
            "description": "删除资源",
            "example": "kubectl delete -f deployment.yaml",
        },
        {
            "command": "kubectl port-forward <pod> 8080:80",
            "description": "端口转发",
            "example": "kubectl port-forward nginx-xxx 8080:80",
        },
        {
            "command": "kubectl get svc",
            "description": "查看服务",
            "example": "kubectl get svc -A",
        },
        {
            "command": "kubectl get deployments",
            "description": "查看部署",
            "example": "kubectl get deployments",
        },
        {
            "command": "kubectl scale deployment <name> --replicas=3",
            "description": "扩缩容",
            "example": "kubectl scale deployment nginx --replicas=3",
        },
        {
            "command": "kubectl top pod",
            "description": "查看 Pod 资源使用",
            "example": "kubectl top pod -A",
        },
        {
            "command": "kubectl get events --sort-by='.lastTimestamp'",
            "description": "查看集群事件",
            "example": "kubectl get events --sort-by='.lastTimestamp'",
        },
        {
            "command": "helm list",
            "description": "列出 Helm Release",
            "example": "helm list -A",
        },
        {
            "command": "helm install <name> <chart>",
            "description": "安装 Helm Chart",
            "example": "helm install mynginx bitnami/nginx",
        },
    ],
    "shell": [
        {
            "command": "echo $PATH",
            "description": "查看环境变量 PATH",
            "example": "echo $PATH",
        },
        {
            "command": "export VAR=value",
            "description": "设置环境变量",
            "example": "export JAVA_HOME=/usr/lib/jvm/java-11",
        },
        {
            "command": "source ~/.bashrc",
            "description": "重新加载配置",
            "example": "source ~/.bashrc",
        },
        {
            "command": "nohup command &",
            "description": "后台运行命令",
            "example": "nohup python app.py &",
        },
        {
            "command": "crontab -e",
            "description": "编辑定时任务",
            "example": "crontab -e",
        },
        {
            "command": "ssh user@host",
            "description": "SSH 远程登录",
            "example": "ssh root@192.168.1.1",
        },
        {
            "command": "scp file user@host:/path",
            "description": "远程复制文件",
            "example": "scp app.tar.gz root@host:/tmp/",
        },
        {
            "command": "curl -I http://example.com",
            "description": "查看 HTTP 响应头",
            "example": "curl -I http://localhost:8000",
        },
        {
            "command": "wget -O file url",
            "description": "下载文件",
            "example": "wget -O backup.sql https://example.com/backup.sql",
        },
        {
            "command": "ping -c 4 host",
            "description": "网络连通测试",
            "example": "ping -c 4 baidu.com",
        },
        {
            "command": "traceroute host",
            "description": "路由追踪",
            "example": "traceroute baidu.com",
        },
        {
            "command": "sed -i 's/old/new/g' file",
            "description": "文本替换",
            "example": "sed -i 's/localhost/0.0.0.0/g' config.ini",
        },
        {
            "command": "xargs -I {} cmd {}",
            "description": "批量执行",
            "example": "cat files.txt | xargs -I {} rm {}",
        },
        {
            "command": "watch -n 1 'command'",
            "description": "定时执行并刷新",
            "example": "watch -n 1 'docker ps'",
        },
        {
            "command": "tee file",
            "description": "输出同时写入文件",
            "example": "echo 'config' | tee app.conf",
        },
    ],
    "git": [
        {
            "command": "git status",
            "description": "查看工作区状态",
            "example": "git status",
        },
        {"command": "git add .", "description": "暂存所有变更", "example": "git add ."},
        {
            "command": "git commit -m 'msg'",
            "description": "提交变更",
            "example": "git commit -m 'fix bug'",
        },
        {
            "command": "git push origin main",
            "description": "推送到远程",
            "example": "git push origin main",
        },
        {
            "command": "git pull origin main",
            "description": "拉取远程更新",
            "example": "git pull origin main",
        },
        {
            "command": "git branch -a",
            "description": "查看所有分支",
            "example": "git branch -a",
        },
        {
            "command": "git checkout -b feature",
            "description": "创建并切换分支",
            "example": "git checkout -b feature-x",
        },
        {
            "command": "git merge feature",
            "description": "合并分支",
            "example": "git merge feature-x",
        },
        {
            "command": "git log --oneline -10",
            "description": "查看最近提交",
            "example": "git log --oneline -10",
        },
        {
            "command": "git diff",
            "description": "查看变更差异",
            "example": "git diff HEAD~1",
        },
        {
            "command": "git stash",
            "description": "暂存当前修改",
            "example": "git stash push -m 'wip'",
        },
        {
            "command": "git stash pop",
            "description": "恢复暂存修改",
            "example": "git stash pop",
        },
        {
            "command": "git reset --hard HEAD~1",
            "description": "回退到上一个版本",
            "example": "git reset --hard HEAD~1",
        },
        {
            "command": "git remote -v",
            "description": "查看远程仓库",
            "example": "git remote -v",
        },
        {
            "command": "git tag -a v1.0 -m 'release'",
            "description": "创建标签",
            "example": "git tag -a v1.0 -m 'release'",
        },
    ],
}


def make_response(code: int = 200, message: str = "ok", data=None):
    return {"code": code, "message": message, "data": data}


@router.get("/categories", response_model=dict)
def get_categories():
    return make_response(data=list(CHEATSHEET_DATA.keys()))


@router.get("/{category}", response_model=dict)
def get_category(category: str):
    data = CHEATSHEET_DATA.get(category)
    if data is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Category not found")
    return make_response(data=data)


@router.get("/search/all", response_model=dict)
def search_cheatsheet(q: Annotated[str, Query(min_length=1)]):
    results = []
    for category, items in CHEATSHEET_DATA.items():
        for item in items:
            if (
                q.lower() in item["command"].lower()
                or q.lower() in item["description"].lower()
            ):
                results.append({"category": category, **item})
    return make_response(data=results)
