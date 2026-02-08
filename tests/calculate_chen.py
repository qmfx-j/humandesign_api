# calculate_chen_final.py - 最终优化版本，包含详细错误处理和故障排除
import requests
import json
from datetime import datetime

class HumanDesignCalculator:
    def __init__(self, base_url="http://localhost:9021", token="AAAAbbbb8888"):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def test_connection(self):
        """测试 API 连接和健康状态"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ API 健康检查通过")
                print(f"   版本: {health_data.get('version', 'Unknown')}")
                print(f"   瑞士星历表: {health_data.get('dependencies', {}).get('pyswisseph', 'Unknown')}")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")
            return False
    
    def calculate_v1(self, birth_info):
        """使用 V1 版本计算 Human Design 数据"""
        url = f"{self.base_url}/calculate"
        
        # 构建查询参数
        params = {
            "year": birth_info["year"],
            "month": birth_info["month"], 
            "day": birth_info["day"],
            "hour": birth_info["hour"],
            "minute": birth_info["minute"],
            "place": birth_info["place"]
        }
        
        try:
            print(f"📡 正在调用 V1 API: {url}")
            response = self.session.get(url, params=params, timeout=30)
            print(f"📊 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                error_detail = response.text[:200] if response.text else "无错误详情"
                print(f"❌ V1 API 错误: {response.status_code} - {error_detail}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ V1 API 超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ V1 API 网络错误: {e}")
            return None
        except Exception as e:
            print(f"❌ V1 API 未知错误: {e}")
            return None
    
    def calculate_v2(self, birth_info):
        """使用 V2 旗舰版本计算 Human Design 数据"""
        url = f"{self.base_url}/v2/calculate"
        
        # 构建请求体 - 包含经纬度
        payload = {
            "year": birth_info["year"],
            "month": birth_info["month"], 
            "day": birth_info["day"],
            "hour": birth_info["hour"],
            "minute": birth_info["minute"],
            "place": birth_info["place"],
            "latitude": birth_info.get("latitude"),
            "longitude": birth_info.get("longitude")
        }
        
        # 移除 None 值
        payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            print(f"📡 正在调用 V2 API: {url}")
            print(f"📋 请求参数: {payload}")
            response = self.session.post(url, json=payload, timeout=30)
            print(f"📊 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                error_detail = response.text[:200] if response.text else "无错误详情"
                print(f"❌ V2 API 错误: {response.status_code} - {error_detail}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ V2 API 超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ V2 API 网络错误: {e}")
            return None
        except Exception as e:
            print(f"❌ V2 API 未知错误: {e}")
            return None
    
    def format_output(self, data, person_name="用户", version="Unknown"):
        """格式化输出结果"""
        if not data:
            return "无法获取数据"
        
        output = []
        output.append("=" * 60)
        output.append(f"✨ {person_name}的 Human Design {version} 数据 ✨")
        output.append("=" * 60)
        
        # 根据版本格式化输出
        if version == "V2":
            self._format_v2_output(data, output)
        else:
            self._format_v1_output(data, output)
        
        output.append("=" * 60)
        return "\n".join(output)
    
    def _format_v2_output(self, data, output):
        """格式化 V2 输出"""
        general = data.get("general", {})
        centers = data.get("centers", {})
        gates = data.get("gates", {})
        variables = data.get("variables", {})
        advanced = data.get("advanced", {})
        
        # 基本信息
        output.append(f"\n📅 基本信息:")
        output.append(f"   出生日期: {general.get('birth_date', 'N/A')}")
        output.append(f"   设计日期: {general.get('create_date', 'N/A')}")
        output.append(f"   出生地点: {general.get('birth_place', 'N/A')}")
        output.append(f"   年龄: {general.get('age', 'N/A')}岁")
        output.append(f"   星座: {general.get('zodiac_sign', 'N/A')}")
        
        # 核心特征
        output.append(f"\n🎯 核心特征:")
        output.append(f"   能量类型: {general.get('energy_type', 'N/A')}")
        output.append(f"   内在权威: {general.get('inner_authority', 'N/A')}")
        output.append(f"   策略: {general.get('strategy', 'N/A')}")
        output.append(f"   签名: {general.get('signature', 'N/A')}")
        output.append(f"   化身交叉: {general.get('inc_cross', 'N/A')}")
        output.append(f"   档案: {general.get('profile', 'N/A')}")
        output.append(f"   定义: {general.get('definition', 'N/A')}")
        
        # 中心状态
        if centers:
            output.append(f"\n⚡ 中心状态:")
            defined = centers.get('defined', [])
            undefined = centers.get('undefined', [])
            output.append(f"   已定义: {', '.join(defined) if defined else '无'}")
            output.append(f"   未定义: {', '.join(undefined) if undefined else '无'}")
        
        # 变量配置
        if variables:
            output.append(f"\n🔄 变量配置:")
            output.append(f"   简码: {variables.get('short_code', 'N/A')}")
            for key in ['top_right', 'bottom_right', 'top_left', 'bottom_left']:
                if key in variables:
                    var = variables[key]
                    output.append(f"   {var.get('name', key)}: {var.get('value', 'N/A')} ({var.get('def_type', 'N/A')})")
        
        # 高级功能
        if advanced:
            output.append(f"\n🚀 高级功能:")
            dream_rave = advanced.get('dream_rave', {})
            if dream_rave:
                output.append(f"   Dream Rave:")
                output.append(f"     状态: {dream_rave.get('status', 'N/A')}")
                output.append(f"     激活中心: {', '.join(dream_rave.get('activated_centers', []))}")
            
            global_cycle = advanced.get('global_cycle', {})
            if global_cycle:
                output.append(f"   Global Cycle:")
                output.append(f"     循环交叉: {global_cycle.get('cycle_cross', 'N/A')}")
    
    def _format_v1_output(self, data, output):
        """格式化 V1 输出"""
        general = data.get("general", {})
        
        # 基本信息
        output.append(f"\n📅 基本信息:")
        output.append(f"   出生日期: {data.get('birth_date', 'N/A')}")
        output.append(f"   设计日期: {data.get('create_date', 'N/A')}")
        output.append(f"   出生地点: {data.get('place', 'N/A')}")
        output.append(f"   年龄: {general.get('age', 'N/A')}岁")
        output.append(f"   星座: {general.get('zodiac_sign', 'N/A')}")
        
        # 核心特征
        output.append(f"\n🎯 核心特征:")
        output.append(f"   能量类型: {general.get('energy_type', 'N/A')}")
        output.append(f"   内在权威: {general.get('inner_authority', 'N/A')}")
        output.append(f"   化身交叉: {general.get('inc_cross', 'N/A')}")
        output.append(f"   档案: {general.get('profile', 'N/A')}")
        output.append(f"   定义: {general.get('definition', 'N/A')}")
        
        # 中心状态
        if 'active_chakras' in general:
            output.append(f"\n⚡ 中心状态:")
            output.append(f"   激活: {', '.join(general.get('active_chakras', []))}")
            output.append(f"   未激活: {', '.join(general.get('inactive_chakras', []))}")
        
        # 变量
        if 'variables' in general:
            variables = general['variables']
            output.append(f"\n🔄 变量配置:")
            output.append(f"   简码: {variables.get('short_code', 'N/A')}")
            for key in ['top_right', 'bottom_right', 'top_left', 'bottom_left']:
                if key in variables:
                    var = variables[key]
                    output.append(f"   {var.get('name', key)}: {var.get('value', 'N/A')} ({var.get('def_type', 'N/A')})")

def main():
    # 陈慧军的信息 - 使用经纬度绕过地理编码
    chen_info = {
        "year": 1998,
        "month": 3,
        "day": 3,
        "hour": 9,
        "minute": 45,
        "place": "Taiyuan, China",
        "latitude": 37.8571,  # 太原市纬度
        "longitude": 112.5629  # 太原市经度
    }
    
    print("🎯 Human Design 数据计算器 - 优化版本")
    print("=" * 50)
    
    # 创建计算器实例
    calculator = HumanDesignCalculator()
    
    # 测试连接
    if not calculator.test_connection():
        print("\n❌ 无法连接到 API 服务")
        print("请检查:")
        print("1. Docker 容器是否正在运行")
        print("2. 端口 9021 是否正确映射")
        print("3. 网络连接是否正常")
        return
    
    print(f"\n👤 计算对象: 陈慧军")
    print(f"🕐 出生时间: {chen_info['year']}-{chen_info['month']}-{chen_info['day']} {chen_info['hour']}:{chen_info['minute']}")
    print(f"📍 出生地点: {chen_info['place']}")
    print("\n🔄 开始计算...")
    
    # 优先尝试 V2
    print("\n🧪 尝试 V2 版本...")
    data = calculator.calculate_v2(chen_info)
    version = "V2"
    
    # 如果 V2 失败，尝试 V1
    if not data:
        print("\n🧪 V2 失败，尝试 V1 版本...")
        data = calculator.calculate_v1(chen_info)
        version = "V1"
    
    if data:
        print(f"\n✅ 成功使用 {version} 版本获取数据")
        
        # 显示原生 JSON 输出
        print(f"\n📄 {version} 原生 JSON 输出:")
        print("=" * 60)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=" * 60)
        
        # 格式化输出
        result = calculator.format_output(data, "陈慧军", version)
        print(result)
        
        # 保存原始数据
        filename = f'chen_huijun_{version.lower()}_data.json'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 原始数据已保存到 {filename}")
        except Exception as e:
            print(f"\n⚠️  保存文件失败: {e}")
        
        # 显示版本特性
        print(f"\n📊 版本信息:")
        if version == "V2":
            print("   🌟 V2 特性:")
            print("      • 结构化的 JSON 响应")
            print("      • 语义增强的字段名称")
            print("      • 高级分析功能")
            print("      • 更好的错误处理")
        else:
            print("   📋 V1 特性:")
            print("      • 经典的 Human Design 计算")
            print("      • 基础数据结构")
            print("      • 稳定可靠的计算")
    else:
        print("\n❌ 所有版本都计算失败")
        print("\n🔧 故障排除建议:")
        print("1. 检查 Docker 容器日志: docker logs humandesignapi")
        print("2. 验证地理编码服务是否可用")
        print("3. 尝试使用英文地名")
        print("4. 检查网络连接和防火墙设置")
        print("5. 重启 Docker 容器: docker restart humandesignapi")

if __name__ == "__main__":
    main()