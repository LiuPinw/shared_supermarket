#!/usr/bin/env python
"""初始化商品分类和商品数据"""
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from goods.models import GoodsType, Goods, GoodsSKU, GoodsImage

# --- 生成占位图片 ---
def make_placeholder(text, color, size=(400, 400)):
    """生成纯色占位图片，中间画个圆形"""
    img = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(img)
    # 画一个简单的圆形作为占位标识
    cx, cy = size[0] // 2, size[1] // 2
    r = min(size) // 6
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline='white', width=4)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return File(buf, name=f'{text}.png')

# --- 分类数据 ---
categories = [
    {'name': '家居家装', 'logo': 'home',      'color': (231, 76, 60)},
    {'name': '美妆护肤', 'logo': 'beauty',    'color': (255, 105, 180)},
    {'name': '医疗保健', 'logo': 'health',    'color': (46, 204, 113)},
    {'name': '生活旅行', 'logo': 'travel',    'color': (52, 152, 219)},
    {'name': '运动户外', 'logo': 'sport',     'color': (243, 156, 18)},
    {'name': '电脑办公', 'logo': 'computer',  'color': (52, 73, 94)},
]

created_types = []

for cat in categories:
    gt, created = GoodsType.objects.get_or_create(
        name=cat['name'],
        defaults={'logo': cat['logo']}
    )
    if created:
        img = make_placeholder(cat['name'], cat['color'])
        gt.image.save(f'{cat["logo"]}.png', img)
        print(f'[OK] 分类: {gt.name}')
    else:
        print(f'[SKIP] 分类已存在: {gt.name}')
    created_types.append(gt)

# --- 商品数据 ---
products = [
    # 家居家装
    {'type': '家居家装', 'goods_name': '简约北欧沙发', 'sku_name': '北欧布艺沙发 三人位 深灰色',
     'desc': '高密度回弹海绵，实木框架，透气棉麻面料', 'price': 2899.00, 'unit': '套', 'stock': 200,
     'color': (180, 160, 140)},
    {'type': '家居家装', 'goods_name': '智能LED吸顶灯', 'sku_name': '现代简约客厅吸顶灯 60W 三色调光',
     'desc': '高亮LED芯片，遥控调光调色，节能省电', 'price': 369.00, 'unit': '个', 'stock': 500,
     'color': (255, 230, 150)},
    {'type': '家居家装', 'goods_name': '天然乳胶枕', 'sku_name': '泰国进口天然乳胶枕 人体工学护颈',
     'desc': '天然乳胶含量93%，透气防螨，柔软回弹', 'price': 199.00, 'unit': '个', 'stock': 800,
     'color': (240, 240, 220)},
    {'type': '家居家装', 'goods_name': '实木书柜', 'sku_name': '北欧简约实木书架 四层开放式',
     'desc': '进口白橡木，环保水性漆，承重力强', 'price': 1599.00, 'unit': '个', 'stock': 150,
     'color': (200, 170, 130)},

    # 美妆护肤
    {'type': '美妆护肤', 'goods_name': '保湿补水面膜', 'sku_name': '玻尿酸深层补水面膜 10片装',
     'desc': '三重玻尿酸精华，深层补水锁水，轻薄服帖', 'price': 69.90, 'unit': '盒', 'stock': 2000,
     'color': (200, 220, 255)},
    {'type': '美妆护肤', 'goods_name': '防晒霜SPF50', 'sku_name': '清爽水感防晒霜 SPF50+ PA++++',
     'desc': '轻薄不油腻，防水防汗，全波段防护', 'price': 129.00, 'unit': '支', 'stock': 1500,
     'color': (255, 240, 200)},
    {'type': '美妆护肤', 'goods_name': '精华液', 'sku_name': '烟酰胺亮肤精华液 30ml',
     'desc': '5%烟酰胺，淡化痘印，提亮肤色', 'price': 189.00, 'unit': '瓶', 'stock': 1200,
     'color': (255, 220, 230)},
    {'type': '美妆护肤', 'goods_name': '口红套装', 'sku_name': '丝绒哑光口红 六色套装',
     'desc': '丝绒哑光质地，持久不脱色，显白百搭', 'price': 259.00, 'unit': '套', 'stock': 600,
     'color': (220, 50, 50)},

    # 医疗保健
    {'type': '医疗保健', 'goods_name': '电子血压计', 'sku_name': '上臂式全自动电子血压计',
     'desc': '智能加压，大屏显示，语音播报，一键测量', 'price': 299.00, 'unit': '台', 'stock': 400,
     'color': (220, 240, 255)},
    {'type': '医疗保健', 'goods_name': '维生素C片', 'sku_name': '天然维生素C咀嚼片 100片',
     'desc': '天然针叶樱桃提取，每片含VC 500mg', 'price': 89.00, 'unit': '瓶', 'stock': 3000,
     'color': (255, 200, 100)},
    {'type': '医疗保健', 'goods_name': '医用口罩', 'sku_name': '一次性医用外科口罩 50只装',
     'desc': '三层防护，BFE≥95%，透气舒适', 'price': 29.90, 'unit': '盒', 'stock': 5000,
     'color': (180, 210, 255)},
    {'type': '医疗保健', 'goods_name': '蛋白粉', 'sku_name': '乳清蛋白粉 增肌健身 900g',
     'desc': '进口乳清蛋白，低脂低糖，易吸收', 'price': 259.00, 'unit': '罐', 'stock': 800,
     'color': (230, 230, 240)},

    # 生活旅行
    {'type': '生活旅行', 'goods_name': '旅行背包', 'sku_name': '大容量户外旅行背包 40L 防水',
     'desc': '防泼水面料，人体工学背负，多隔层收纳', 'price': 299.00, 'unit': '个', 'stock': 600,
     'color': (80, 130, 180)},
    {'type': '生活旅行', 'goods_name': '保温杯', 'sku_name': '不锈钢真空保温杯 500ml',
     'desc': '316不锈钢内胆，12小时保温，便携设计', 'price': 129.00, 'unit': '个', 'stock': 1500,
     'color': (180, 190, 200)},
    {'type': '生活旅行', 'goods_name': '旅行收纳套装', 'sku_name': '旅行收纳袋六件套 防水',
     'desc': '分类收纳，防水面料，轻便实用', 'price': 49.90, 'unit': '套', 'stock': 2000,
     'color': (150, 200, 180)},
    {'type': '生活旅行', 'goods_name': '自拍杆三脚架', 'sku_name': '蓝牙自拍杆三脚架 手机通用',
     'desc': '360度旋转，伸缩自如，蓝牙遥控', 'price': 79.00, 'unit': '个', 'stock': 1000,
     'color': (60, 60, 60)},

    # 运动户外
    {'type': '运动户外', 'goods_name': '瑜伽垫', 'sku_name': '加厚防滑瑜伽垫 NBR材质 10mm',
     'desc': '双面防滑，高密度NBR材质，柔软回弹', 'price': 99.00, 'unit': '条', 'stock': 1200,
     'color': (180, 130, 200)},
    {'type': '运动户外', 'goods_name': '运动跑鞋', 'sku_name': '轻便透气跑步鞋 网面减震',
     'desc': '飞织网面，EVA缓震中底，防滑耐磨大底', 'price': 459.00, 'unit': '双', 'stock': 500,
     'color': (50, 50, 50)},
    {'type': '运动户外', 'goods_name': '运动水壶', 'sku_name': 'Tritan材质运动水壶 750ml',
     'desc': '食品级Tritan材质，防漏设计，单手开盖', 'price': 59.00, 'unit': '个', 'stock': 1800,
     'color': (100, 200, 100)},
    {'type': '运动户外', 'goods_name': '跳绳', 'sku_name': '高速轴承跳绳 专业健身',
     'desc': '钢丝绳芯，PVC包裹，360度旋转轴承', 'price': 39.00, 'unit': '根', 'stock': 2500,
     'color': (240, 180, 50)},

    # 电脑办公
    {'type': '电脑办公', 'goods_name': '机械键盘', 'sku_name': '机械键盘 红轴 87键 RGB背光',
     'desc': 'Cherry MX红轴，RGB背光，全键无冲', 'price': 399.00, 'unit': '个', 'stock': 350,
     'color': (40, 40, 40)},
    {'type': '电脑办公', 'goods_name': '无线鼠标', 'sku_name': '静音无线鼠标 双模蓝牙+2.4G',
     'desc': '人体工学设计，静音按键，长续航', 'price': 99.00, 'unit': '个', 'stock': 1000,
     'color': (100, 100, 110)},
    {'type': '电脑办公', 'goods_name': '移动硬盘', 'sku_name': 'USB3.0移动硬盘 2TB 便携',
     'desc': '高速传输，即插即用，防震抗摔', 'price': 459.00, 'unit': '个', 'stock': 300,
     'color': (30, 30, 60)},
    {'type': '电脑办公', 'goods_name': '笔记本电脑支架', 'sku_name': '铝合金笔记本支架 可升降',
     'desc': '全铝合金材质，多角度调节，散热设计', 'price': 159.00, 'unit': '个', 'stock': 700,
     'color': (180, 180, 190)},
]

created_count = 0
for p in products:
    # 找分类
    gt = next((t for t in created_types if t.name == p['type']), None)
    if not gt:
        print(f'[ERR] 分类未找到: {p["type"]}')
        continue

    # 创建 Goods SPU
    goods, _ = Goods.objects.get_or_create(
        name=p['goods_name'],
        defaults={'detail': f'<p>{p["desc"]}</p>'}
    )

    # 创建 GoodsSKU
    sku, created = GoodsSKU.objects.get_or_create(
        name=p['sku_name'],
        defaults={
            'type': gt,
            'goods': goods,
            'desc': p['desc'],
            'price': p['price'],
            'unite': p['unit'],
            'stock': p['stock'],
            'sales': 0,
            'status': 1,
        }
    )
    if created:
        img = make_placeholder(p['goods_name'], p['color'], (400, 400))
        sku.image.save(f"{p['goods_name']}.png", img)
        created_count += 1
        print(f'[OK] 商品: [{gt.name}] {sku.name} ¥{p["price"]}')
    else:
        print(f'[SKIP] 商品已存在: {sku.name}')

print(f'\nDone! 共创建 {len(categories)} 个分类、{created_count} 个商品')
