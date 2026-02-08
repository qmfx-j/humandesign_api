# generate_chen_bodygraph.py - 生成陈慧军的身体图谱图像
import requests
import json
from datetime import datetime
import os

class BodyGraphGenerator:
    def __init__(self, base_url="http://localhost:9021", token="12345678"):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def generate_bodygraph(self, birth_info, format_type="png"):
        """
        生成身体图谱图像
        
        Args:
            birth_info (dict): 出生信息
            format_type (str): 图像格式 (png, svg, jpg)
        
        Returns:
            bytes: 图像数据，如果失败返回None
        """
        url = f"{self.base_url}/bodygraph"
        
        # 构建查询参数
        params = {
            "year": birth_info["year"],
            "month": birth_info["month"],
            "day": birth_info["day"],
            "hour": birth_info["hour"],
            "minute": birth_info["minute"],
            "place": birth_info["place"],
            "latitude": birth_info.get("latitude"),
            "longitude": birth_info.get("longitude"),
            "fmt": format_type
        }
        
        # 移除 None 值
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            print(f"📡 正在调用身体图谱接口: {url}")
            print(f"📋 查询参数: {params}")
            
            response = self.session.get(url, params=params, timeout=30)
            print(f"📊 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                return response.content
            else:
                error_detail = response.text[:300] if response.text else "无错误详情"
                print(f"❌ 图像生成错误: {response.status_code} - {error_detail}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ 图像生成超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 图像生成网络错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 图像生成未知错误: {e}")
            return None
    
    def save_image(self, image_data, filename):
        """保存图像文件"""
        try:
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f"✅ 图像已保存到: {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存图像失败: {e}")
            return False
    
    def verify_image(self, filename):
        """验证图像文件"""
        if not os.path.exists(filename):
            print(f"❌ 文件不存在: {filename}")
            return False
            
        file_size = os.path.getsize(filename)
        if file_size == 0:
            print(f"❌ 文件为空: {filename}")
            return False
            
        # 检查文件扩展名对应的内容类型
        if filename.endswith('.png'):
            # PNG文件应该以PNG签名开头
            with open(filename, 'rb') as f:
                header = f.read(8)
                if header != b'\x89PNG\r\n\x1a\n':
                    print(f"❌ 文件不是有效的PNG格式: {filename}")
                    return False
                    
        elif filename.endswith('.svg'):
            # SVG文件应该是XML格式
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read(100)  # 读取前100个字符
                if '<?xml' not in content and '<svg' not in content:
                    print(f"❌ 文件不是有效的SVG格式: {filename}")
                    return False
                    
        elif filename.endswith(('.jpg', '.jpeg')):
            # JPEG文件应该以JPEG签名开头
            with open(filename, 'rb') as f:
                header = f.read(2)
                if header != b'\xff\xd8':
                    print(f"❌ 文件不是有效的JPEG格式: {filename}")
                    return False
        
        print(f"✅ 图像文件验证通过: {filename} ({file_size} 字节)")
        return True

def main():
    # 陈慧军的出生信息
    chen_info = {
        "year": 1998,
        "month": 3,
        "day": 3,
        "hour": 9,
        "minute": 45,
        "place": "Taiyuan, China",
        "latitude": 37.8571,
        "longitude": 112.5629
    }
    
    print("🎨 陈慧军身体图谱生成器")
    print("=" * 50)
    
    # 创建生成器实例
    generator = BodyGraphGenerator()
    
    # 显示基本信息
    print(f"\n👤 生成对象: 陈慧军")
    print(f"🕐 出生时间: {chen_info['year']}-{chen_info['month']}-{chen_info['day']} {chen_info['hour']}:{chen_info['minute']}")
    print(f"📍 出生地点: {chen_info['place']}")
    print(f"🌐 坐标: {chen_info['latitude']}, {chen_info['longitude']}")
    
    # 支持的格式列表
    formats = ["png", "svg", "jpg"]
    
    generated_files = []
    
    print(f"\n🔄 开始生成身体图谱...")
    
    for fmt in formats:
        print(f"\n🖼️  生成 {fmt.upper()} 格式图像...")
        
        # 生成图像
        image_data = generator.generate_bodygraph(chen_info, fmt)
        
        if image_data:
            # 生成文件名
            filename = f'chen_huijun_bodygraph.{fmt}'
            
            # 保存图像
            if generator.save_image(image_data, filename):
                # 验证图像
                if generator.verify_image(filename):
                    generated_files.append(filename)
                    print(f"🎉 {fmt.upper()} 格式图像生成成功!")
                else:
                    print(f"⚠️  {fmt.upper()} 格式图像验证失败")
            else:
                print(f"❌ {fmt.upper()} 格式图像保存失败")
        else:
            print(f"❌ {fmt.upper()} 格式图像生成失败")
    
    # 总结结果
    print(f"\n📊 生成结果总结:")
    print("=" * 50)
    
    if generated_files:
        print(f"✅ 成功生成 {len(generated_files)} 个图像文件:")
        for filename in generated_files:
            file_size = os.path.getsize(filename)
            print(f"   📄 {filename} ({file_size} 字节)")
    else:
        print("❌ 没有成功生成任何图像文件")
        print("\n🔧 故障排除建议:")
        print("1. 检查 Docker 容器是否正常运行")
        print("2. 验证 API 认证令牌")
        print("3. 检查网络连接")
        print("4. 查看容器日志: docker logs humandesignapi")
        print("5. 确认身体图谱服务是否启用")

if __name__ == "__main__":
    main()