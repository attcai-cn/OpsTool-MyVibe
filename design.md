# 运维小工具技术设计文档

> 版本：v1.1
> 日期：2026-07-13
> 状态：已实现

---

## 一、项目概述

### 1.1 项目背景
开发一个面向运维人员的 Web 小工具，集成常用功能模块，降低日常排查与计算成本。

### 1.2 功能范围

| 模块 | 功能点 |
|------|--------|
| 用户系统 | 注册、登录、JWT 认证 |
| 笔记 | 增删改查个人运维笔记，支持标签与搜索 |
| 速查表 | Linux / Docker / Kubernetes / Shell / Git 命令速查与搜索 |
| 计算器 | 带宽 Bits↔Bytes 转换、Unix 时间戳转换、IP 子网计算 |
| Cron 表达式 | 可视化生成 Cron 表达式、解析表达式含义、预测下次执行时间 |
| 待办事项 | 个人 Todo 列表，支持紧急程度、截止日期、完成状态筛选 |

### 1.3 技术选型

| 层级 | 技术 | 版本建议 |
|------|------|----------|
| 前端 | Vue 3 + Vite + Vue Router + Pinia + Axios + Element Plus | Vue 3.5+ |
| 后端 | Python + FastAPI + Uvicorn | Python 3.11+ |
| 数据库 | SQLite + SQLAlchemy ORM + Alembic 迁移 | SQLite 3 |
| 认证 | JWT (PyJWT) + bcrypt 密码哈希 | — |
| Cron 解析 | croniter | — |

### 1.4 端口与服务划分

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 dev server | 5173 | Vite 默认开发端口，代理 `/api` 到后端 |
| 后端 API | 8000 | FastAPI + Uvicorn |

---

## 二、系统架构

### 2.1 部署架构（开发环境）

```
┌─────────────────┐         ┌─────────────────┐
│   Browser       │ ◄─────► │  前端 (Vue)     │
│                 │  5173   │  Vite DevServer │
└─────────────────┘         └────────┬────────┘
                                     │ API 请求 (/api)
                                     ▼ 8000
                              ┌─────────────────┐
                              │  后端 (FastAPI) │
                              │  /api/v1/...    │
                              └────────┬────────┘
                                       │ SQLAlchemy
                                       ▼
                              ┌─────────────────┐
                              │   SQLite        │
                              │   ops_tool.db   │
                              └─────────────────┘
```

> 前端 Vite 配置中已设置 `proxy: { '/api': { target: 'http://localhost:8000' } }`，开发时前端直接通过 `/api/v1/...` 访问后端。

### 2.2 前端架构

```
frontend/
├── dist/                 # 构建产物（npm run build）
├── public/
│   └── logo.svg
├── src/
│   ├── api/              # Axios 封装 + 各模块 API（index.js）
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   ├── router/           # Vue Router 路由配置
│   ├── stores/           # Pinia 状态管理
│   │   ├── auth.js
│   │   ├── note.js
│   │   ├── cheatsheet.js
│   │   └── calculator.js
│   ├── views/            # 页面级组件
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── DashboardView.vue
│   │   ├── NotesView.vue
│   │   ├── NoteDetailView.vue
│   │   ├── CheatsheetView.vue
│   │   ├── CalculatorView.vue
│   │   ├── CronView.vue
│   │   └── TodoView.vue
│   ├── App.vue
│   └── main.js
├── index.html
├── package.json
└── vite.config.js
```

### 2.3 后端架构

```
backend/
├── alembic/              # 数据库迁移配置
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI 入口 + 中间件 + 跨域 + 路由注册
│   ├── config.py         # 配置项（SECRET_KEY、DB_URL、CORS 等）
│   ├── database.py       # SQLAlchemy engine / session / Base
│   ├── dependencies.py   # 公共依赖（get_db、get_current_user）
│   ├── models/           # ORM 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── note.py
│   │   └── todo.py
│   ├── schemas/          # Pydantic 校验模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── note.py
│   │   └── todo.py
│   ├── routers/          # API 路由
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── notes.py
│   │   ├── cheatsheet.py
│   │   ├── calculator.py
│   │   ├── cron.py
│   │   └── todo.py
│   └── utils/            # 工具函数
│       ├── __init__.py
│       ├── security.py   # 密码哈希、JWT 生成与校验
│       ├── calculator.py # 计算器逻辑封装
│       └── cron.py       # Cron 表达式生成/解析/预测
├── ops_tool.db           # SQLite 数据库文件（gitignore）
├── requirements.txt
└── run.py                # uvicorn 启动脚本
```

---

## 三、数据库设计

### 3.1 ER 图（简化）

```
┌──────────────┐
│    users     │
├──────────────┤
│ id (PK)      │
│ username     │
│ email        │
│ hashed_password
│ created_at   │
│ updated_at   │
└──────┬───────┘
       │ 1 : N
       ├──────────────► ┌──────────────┐
       │                │    notes     │
       │                ├──────────────┤
       │                │ id (PK)      │
       │                │ user_id (FK) │
       │                │ title        │
       │                │ content      │
       │                │ tags         │
       │                │ created_at   │
       │                │ updated_at   │
       │                └──────────────┘
       │
       └──────────────► ┌──────────────┐
                        │    todos     │
                        ├──────────────┤
                        │ id (PK)      │
                        │ user_id (FK) │
                        │ title        │
                        │ urgency      │
                        │ deadline     │
                        │ completed    │
                        │ created_at   │
                        │ updated_at   │
                        └──────────────┘
```

### 3.2 表结构

#### users 表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PK, AUTOINCREMENT | 主键 |
| username | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | 用户名 |
| email | VARCHAR(100) | UNIQUE, NOT NULL | 邮箱 |
| hashed_password | VARCHAR(255) | NOT NULL | bcrypt 哈希密码 |
| created_at | DATETIME | server_default now | 创建时间 |
| updated_at | DATETIME | server_default now, onupdate | 更新时间 |

#### notes 表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PK, AUTOINCREMENT | 主键 |
| user_id | INTEGER | FK(users.id), NOT NULL, INDEX | 归属用户 |
| title | VARCHAR(200) | NOT NULL | 标题 |
| content | TEXT | NOT NULL | 内容（Markdown） |
| tags | VARCHAR(200) | DEFAULT '' | 标签，逗号分隔 |
| created_at | DATETIME | server_default now | 创建时间 |
| updated_at | DATETIME | server_default now, onupdate | 更新时间 |

#### todos 表

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PK, AUTOINCREMENT | 主键 |
| user_id | INTEGER | FK(users.id, ondelete=CASCADE), NOT NULL, INDEX | 归属用户 |
| title | VARCHAR(200) | NOT NULL | 标题 |
| urgency | VARCHAR(10) | NOT NULL, DEFAULT 'medium' | 紧急程度：low / medium / high |
| deadline | DATETIME | NOT NULL | 截止日期 |
| completed | BOOLEAN | DEFAULT FALSE, NOT NULL | 是否完成 |
| created_at | DATETIME | server_default now | 创建时间 |
| updated_at | DATETIME | server_default now, onupdate | 更新时间 |

### 3.3 数据迁移策略
- 使用 **Alembic** 管理数据库版本迁移
- 开发环境下 `main.py` 启动时会自动 `Base.metadata.create_all(bind=engine)` 建表（生产环境建议只用 Alembic）
- 后续扩展通过新增迁移脚本完成

---

## 四、API 接口设计

> 基础路径：`http://localhost:8000/api/v1`
> 统一响应格式：
> ```json
> {
>   "code": 200,
>   "message": "ok",
>   "data": { ... }
> }
> ```

### 4.1 认证模块（`/auth`）

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/auth/register` | 用户注册 | `{ username, email, password }` | 用户信息（脱敏） |
| POST | `/auth/login` | 用户登录 | `{ username, password }` | `{ access_token, token_type: "bearer" }` |
| GET | `/auth/me` | 获取当前用户 | Header: Authorization | 当前用户信息 |

### 4.2 笔记模块（`/notes`）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/notes` | 笔记列表（支持分页、搜索 `q`、标签过滤 `tag`） | 是 |
| GET | `/notes/{id}` | 笔记详情 | 是 |
| POST | `/notes` | 创建笔记 | 是 |
| PUT | `/notes/{id}` | 更新笔记 | 是 |
| DELETE | `/notes/{id}` | 删除笔记 | 是 |

### 4.3 待办事项模块（`/todos`）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/todos` | Todo 列表（支持 `urgency`、`completed` 筛选、分页） | 是 |
| GET | `/todos/{id}` | Todo 详情 | 是 |
| POST | `/todos` | 创建 Todo | 是 |
| PUT | `/todos/{id}` | 更新 Todo | 是 |
| PATCH | `/todos/{id}/complete` | 切换完成状态 | 是 |
| DELETE | `/todos/{id}` | 删除 Todo | 是 |

### 4.4 速查表模块（`/cheatsheet`）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/cheatsheet/categories` | 获取所有分类 | 否 |
| GET | `/cheatsheet/{category}` | 获取某分类下所有命令条目 | 否 |
| GET | `/cheatsheet/search/all` | 关键词搜索命令 | 否 |

> 当前分类包括：`linux`、`docker`、`kubernetes`、`shell`、`git`。

### 4.5 计算器模块（`/calculator`）

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| POST | `/calculator/bandwidth` | 带宽转换 | `{ value, from_unit, to_unit }` |
| POST | `/calculator/timestamp` | Unix 时间戳转换 | `{ timestamp?, datetime? }`（二传一，皆空则返回当前时间） |
| POST | `/calculator/subnet` | IP 子网计算 | `{ cidr: "192.168.1.0/24" }` |

### 4.6 Cron 表达式模块（`/cron`）

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| POST | `/cron/build` | 根据参数生成 Cron 表达式 | `{ mode: "daily"\|"weekly", minute, hour, day_of_week? }` |
| POST | `/cron/parse` | 解析 Cron 表达式 | `{ expression: "0 2 * * *" }` |

> 响应中包含 `expression`、`description`（人类可读描述）、`next_executions`（最近 5 次执行时间）。

---

## 五、安全设计

| 层面 | 措施 |
|------|------|
| 密码存储 | bcrypt 哈希（salt rounds = 12） |
| 身份认证 | JWT Access Token，有效期 24h，Bearer 方式传递 |
| CORS | 后端配置 `allow_origins=["http://localhost:5173"]` |
| 输入校验 | Pydantic Schema 严格校验 + FastAPI 自动文档 |
| SQL 注入 | SQLAlchemy ORM 参数化查询，杜绝拼接 |
| 速率限制 | 初期可引入 `slowapi` 对登录/注册接口限流（可选） |

---

## 六、前端设计

### 6.1 路由规划

| 路由 | 页面 | 说明 |
|------|------|------|
| `/login` | LoginView | 登录页（未登录跳转） |
| `/register` | RegisterView | 注册页 |
| `/` | DashboardView | 首页 / 仪表盘 |
| `/notes` | NotesView | 笔记列表 + 编辑器 |
| `/notes/:id` | NoteDetailView | 笔记详情（编辑模式） |
| `/cheatsheet` | CheatsheetView | 速查表（左侧分类 + 右侧列表） |
| `/calculator` | CalculatorView | 计算器（Tab 切换三个子工具） |
| `/cron` | CronView | Cron 表达式生成与解析 |
| `/todos` | TodoView | 待办事项列表与管理 |

### 6.2 状态管理（Pinia）

- `authStore`：用户信息、token、登录状态、登录/登出动作
- `noteStore`：笔记列表、当前笔记、CRUD 动作
- `cheatsheetStore`：分类、命令列表、搜索
- `calculatorStore`：带宽/时间戳/子网计算结果缓存

> Cron 与 Todo 模块当前直接在组件中调用封装好的 `api` 方法，未独立创建 Pinia store，如需复杂状态共享可后续补充。

### 6.3 Axios 封装要点

- 封装 `request` / `response` 拦截器（`frontend/src/api/index.js`）
- 请求头自动注入 `Authorization: Bearer <token>`
- 统一处理 401 状态码 → 清除 token 并跳转登录页
- 统一错误提示（Element Plus `ElMessage`）

---

## 七、扩展性设计（后续迭代预留）

| 扩展方向 | 预留设计 |
|----------|----------|
| 用户自定义速查表 | cheatsheet 数据接口已设计为 RESTful，未来可添加 `POST /cheatsheet`（需认证） |
| 计算历史保存 | calculator 接口可扩展 `save_history` 字段，配合 `calculator_history` 表 |
| 多用户协作 | notes / todos 表已预留 user_id，未来增加 `shared_with` 关联表即可 |
| 更换数据库 | SQLAlchemy ORM + Alembic 天然支持迁移到 PostgreSQL / MySQL |
| 部署生产 | 前端 `npm run build` 产出静态文件，Nginx 托管；后端 Uvicorn + Gunicorn |
| Cron 模块增强 | 可扩展支持更多调度模式（每月、每年），或对接真实定时任务调度器 |
| Todo 模块增强 | 可扩展支持分类、标签、重复任务、邮件提醒等 |

---

## 八、开发环境启动流程

### 后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python run.py
# 服务运行于 http://localhost:8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
# 服务运行于 http://localhost:5173
# API 请求通过 Vite proxy 自动转发到 http://localhost:8000
```

---

## 九、目录结构总览

```
ops-tool/
├── design.md                  # 本设计文档
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── utils/
│   ├── ops_tool.db
│   ├── requirements.txt
│   └── run.py
└── frontend/
    ├── dist/                  # 构建产物
    ├── public/
    ├── src/
    │   ├── api/
    │   ├── assets/
    │   ├── components/
    │   ├── router/
    │   ├── stores/
    │   ├── views/
    │   ├── App.vue
    │   └── main.js
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 十、总结

本设计遵循 **前后端分离、轻量可扩展** 的原则：

1. **后端** 以 FastAPI 提供标准化 RESTful API，SQLAlchemy + Alembic 保障数据层规范与可迁移性，JWT + bcrypt 保障基础安全。
2. **前端** 以 Vue 3 组合式 API + Pinia 构建，模块化视图与状态管理，Element Plus 提供统一 UI 风格，便于后续功能扩展。
3. **数据库** 选用 SQLite 降低初期部署成本，ORM 层预留了向 PostgreSQL / MySQL 迁移的能力。
4. **功能模块** 各自独立（auth、notes、todos、cheatsheet、calculator、cron），降低耦合，方便后续单独迭代。
5. **开发体验** 通过 Vite DevServer 的 `proxy` 配置实现前后端无缝联调，无需处理跨域。
