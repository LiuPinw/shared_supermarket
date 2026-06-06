# 共享大超市

基于 Django 的 B2C 电商平台项目，源自项目天天生鲜，经过全面升级和改造。

---

## 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装与启动

```bash
# 1. 创建虚拟环境
conda create -n your_env python=3.10
conda activate homework

# 2. 安装依赖
pip install Django==3.2.25
pip install celery django-haystack django-tinymce jieba Pillow PyMySQL \
    itsdangerous mutagen python-alipay-sdk Whoosh django-redis \
    django-redis-sessions fakeredis

# 3. 数据库迁移
python manage.py makemigrations user goods cart order
python manage.py migrate

# 4. 启动开发服务器
python manage.py runserver
```

访问 **http://127.0.0.1:8000**

> **注意**：开发环境使用 SQLite 数据库和 fakeredis 模拟 Redis，无需额外安装 MySQL、Redis、Nginx、FastDFS 等服务。

---

## 功能模块

### 用户模块
- [x] 用户注册（注册即自动激活，无需邮件验证）
- [x] 用户登录 / 退出
- [x] 个人中心（信息页、订单页、地址管理）
- [x] 收货地址增删改查

### 商品模块
- [x] 首页（按分类展示商品，每类显示前4件）
- [x] 商品详情页
- [x] 商品列表页（支持分页、按价格/人气排序）
- [x] 搜索功能（haystack + whoosh）
- [x] 商品分类导航：数码产品 / 食品专区 / 美妆护肤 / 医疗保健 / 运动户外

### 购物车模块
- [x] 加入购物车（AJAX 无刷新）
- [x] 修改商品数量（加减按钮 + 手动输入）
- [x] 删除购物车记录
- [x] 立即购买（加入购物车并跳转下单）
- [x] 购物车商品总数实时更新

### 订单模块
- [x] 确认订单页面（地址选择、支付方式选择）
- [x] 订单创建（支持悲观锁防超卖）
- [x] 订单评论
- [x] 支付宝支付接口（开发环境使用沙箱）

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Django 3.2.25 |
| 数据库 | SQLite（开发）/ MySQL（生产） |
| 缓存 | LocMemCache（开发）/ Redis（生产） |
| 搜索 | haystack + Whoosh |
| 前端 | jQuery + Django Templates |
| 异步任务 | Celery（生产环境） |

---

## 与原始项目的主要改动

### 环境升级
| 项目 | 原版 | 升级后 |
|------|------|--------|
| Python | 3.6 | **3.10** |
| Django | 1.8.2 | **3.2.25** |
| 数据库 | MySQL | **SQLite**（零配置开发） |
| Redis | 需要真实服务 | **fakeredis**（自动模拟） |
| Celery | 依赖 Redis | **开发环境跳过** |
| FastDFS | 需要分布式文件系统 | **本地文件存储** |

### Bug 修复（8处）
1. **购物车/订单按钮无反应** — `user.is_authenticated()` 改为属性访问
2. **收货地址无法保存** — 手机号正则修复，支持所有号段
3. **下单提示"参数不完整"** — 增加无地址时的前端校验和提示
4. **注册后需重新登录** — 注册成功自动登录
5. **购物车数量显示 `b'1'`** — fakeredis 启用 `decode_responses=True`
6. **模板 500 错误** — 所有页面的图片引用增加空值保护（16个文件）
7. **登录页旧品牌图片** — CSS 背景图改为纯色
8. **导航栏残留旧文字** — "手机生鲜/抽奖" 改为数据库动态读取

### 前端改造
- **重命名**：天天生鲜 → 共享大超市
- **色调**：绿色系 `#37ab40` → 橙红色系 `#e8460a`
- **首页**：恢复分类区块样式，每个分类展示实际商品
- **分类**：数码产品 / 食品专区 / 美妆护肤 / 医疗保健 / 运动户外（5个）
- **登录页**：删除旧品牌 slogan 和 banner 图片
- **商品详情**：新增"立即购买"按钮
- **商品列表**：新增快捷加入购物车功能
- **模板健壮性**：所有图片和数据引用均增加空值保护

### 代码适配（Django 1.8 → 3.2）
- `MIDDLEWARE_CLASSES` → `MIDDLEWARE`
- `django.core.urlresolvers` → `django.urls`
- `django.conf.urls.url()` → `django.urls.re_path()`
- `ForeignKey(on_delete)` 必填
- `user.is_authenticated()` → `user.is_authenticated` 属性
- `{% load staticfiles %}` → `{% load static %}`
- `itsdangerous.TimedJSONWebSignatureSerializer` → `URLSafeTimedSerializer`
- 所有 app URL 配置增加 `app_name`
- 移除 `SessionAuthenticationMiddleware`（Django 2.0 已删除）
- `include(namespace=)` 需配合 `app_name`

### 已删除内容
- "日夜兼程 · 急速送达" 等旧文案
- 硬编码的"手机生鲜/抽奖"导航
- "首页"分类（无实际意义）

---

## 项目布局

```
dailyfresh-master/
├── apps/                   # Django 应用
│   ├── user/               # 用户模块（注册/登录/地址）
│   ├── goods/              # 商品模块（首页/详情/列表/搜索）
│   ├── cart/               # 购物车模块
│   └── order/              # 订单模块
├── dailyfresh/             # Django 配置
│   ├── settings.py         # 项目设置
│   ├── urls.py             # 根路由
│   └── wsgi.py             # WSGI 入口
├── templates/              # Django 模板
├── static/                 # 静态文件（CSS/JS/图片）
├── utils/                  # 工具模块
├── celery_tasks/           # Celery 异步任务
├── db/                     # 数据库基类
├── manage.py               # Django 管理入口
└── README.md
```

---

## 测试账号

启动项目后运行以下命令创建管理员：

```bash
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"
```

管理员后台：**http://127.0.0.1:8000/admin**

---

## 生产环境部署

生产环境需要配置以下服务：

- MySQL 数据库（修改 `settings.py` 中的 `DATABASES`）
- Redis 缓存（取消 `CACHES` 中的 Redis 配置注释）
- Celery 异步任务队列（需 Redis broker）
- FastDFS + Nginx（图片存储）
- 支付宝密钥配置

详见 `configurationFile/` 目录下的原始配置文档。

---

> 原项目：天天生鲜（传智播客 Python 教程）  
> 修改时间：2026-06-06
