# analyze_chen_transits.py - 分析陈慧军的当日运势
import requests
import json
from datetime import datetime, timezone
import time

class TransitAnalyzer:
    def __init__(self, base_url="http://localhost:9021", token="12345678"):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_current_date(self):
        """获取当前日期"""
        # 获取当前北京时间
        now = datetime.now()
        # 转换为北京时间 (UTC+8)
        beijing_offset = 8 * 3600  # 8小时转为秒
        beijing_time = datetime.fromtimestamp(now.timestamp() + beijing_offset)
        
        return {
            "year": beijing_time.year,
            "month": beijing_time.month,
            "day": beijing_time.day,
            "hour": beijing_time.hour,
            "minute": beijing_time.minute
        }
    
    def analyze_daily_transit(self, birth_info, transit_date=None):
        """
        分析每日运势
        
        Args:
            birth_info (dict): 出生信息
            transit_date (dict): 运势日期，默认为今天
        
        Returns:
            dict: 运势分析结果
        """
        if transit_date is None:
            transit_date = self.get_current_date()
        
        url = f"{self.base_url}/transits/daily"
        
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
            "transit_year": transit_date["year"],
            "transit_month": transit_date["month"],
            "transit_day": transit_date["day"],
            "transit_hour": transit_date["hour"],
            "transit_minute": transit_date["minute"]
        }
        
        # 移除 None 值
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            print(f"📡 正在调用每日运势接口: {url}")
            print(f"📋 查询参数: {params}")
            
            response = self.session.get(url, params=params, timeout=30)
            print(f"📊 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                error_detail = response.text[:300] if response.text else "无错误详情"
                print(f"❌ 运势分析错误: {response.status_code} - {error_detail}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ 运势分析超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 运势分析网络错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 运势分析未知错误: {e}")
            return None
    
    def format_transit_report(self, data, person_name="用户", transit_date=None):
        """格式化运势报告"""
        if not data:
            return "无法获取运势数据"
        
        if transit_date is None:
            transit_date = self.get_current_date()
        
        meta = data.get("meta", {})
        composite_changes = data.get("composite_changes", {})
        planetary_transits = data.get("planetary_transits", {})
        
        output = []
        output.append("=" * 60)
        output.append(f"🔮 {person_name}的 {transit_date['year']}-{transit_date['month']:02d}-{transit_date['day']:02d} 运势分析 🔮")
        output.append("=" * 60)
        
        # 基本信息
        output.append(f"\n👤 个人信息:")
        output.append(f"   能量类型: {meta.get('energy_type', 'N/A')}")
        output.append(f"   内在权威: {meta.get('inner_authority', 'N/A')}")
        output.append(f"   策略: {meta.get('strategy', 'N/A')}")
        output.append(f"   签名: {meta.get('signature', 'N/A')}")
        output.append(f"   当前年龄: {meta.get('age', 'N/A')}岁")
        
        # 运势日期信息
        output.append(f"\n📅 运势日期:")
        output.append(f"   本地时间: {meta.get('transit_date_local', 'N/A')}")
        output.append(f"   UTC时间: {meta.get('transit_date_utc', 'N/A')}")
        output.append(f"   计算地点: {meta.get('calculation_place', 'N/A')}")
        output.append(f"   星座: {meta.get('zodiac_sign', 'N/A')}")
        
        # 复合变化分析
        output.append(f"\n🔄 复合变化分析:")
        if composite_changes:
            for key, value in composite_changes.items():
                if isinstance(value, dict):
                    output.append(f"   {key}:")
                    for sub_key, sub_value in value.items():
                        output.append(f"     {sub_key}: {sub_value}")
                else:
                    output.append(f"   {key}: {value}")
        else:
            output.append("   暂无复合变化数据")
        
        # 行星运势
        output.append(f"\n🪐 行星运势:")
        if planetary_transits and isinstance(planetary_transits, list):
            for transit in planetary_transits:
                if isinstance(transit, dict):
                    planets = transit.get('planets', 'Unknown')
                    gate = transit.get('gate', 'N/A')
                    line = transit.get('line', 'N/A')
                    description = transit.get('description', '')
                    output.append(f"   {planets}: 闸门{gate} 第{line}线 {description}")
                else:
                    output.append(f"   {transit}")
        else:
            output.append("   暂无行星运势数据")
        
        # 中心状态变化
        defined_centers = meta.get('defined_centers', [])
        undefined_centers = meta.get('undefined_centers', [])
        if defined_centers or undefined_centers:
            output.append(f"\n⚡ 中心状态:")
            if defined_centers:
                output.append(f"   已定义中心: {', '.join(defined_centers)}")
            if undefined_centers:
                output.append(f"   未定义中心: {', '.join(undefined_centers)}")
        
        output.append("=" * 60)
        return "\n".join(output)

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
    
    print("🔮 陈慧军每日运势分析器")
    print("=" * 50)
    
    # 创建分析器实例
    analyzer = TransitAnalyzer()
    
    # 获取今日运势
    print(f"\n👤 分析对象: 陈慧军")
    print(f"🕐 出生时间: {chen_info['year']}-{chen_info['month']}-{chen_info['day']} {chen_info['hour']}:{chen_info['minute']}")
    print(f"📍 出生地点: {chen_info['place']}")
    
    current_date = analyzer.get_current_date()
    print(f"📅 分析日期: {current_date['year']}-{current_date['month']:02d}-{current_date['day']:02d}")
    print(f"⏰ 当前时间: {current_date['hour']:02d}:{current_date['minute']:02d}")
    
    print("\n🔄 开始运势分析...")
    
    # 分析运势
    transit_data = analyzer.analyze_daily_transit(chen_info, current_date)
    
    if transit_data:
        print(f"\n✅ 运势分析完成")
        
        # 显示原生 JSON 输出
        print(f"\n📄 原生 JSON 输出:")
        print("=" * 60)
        print(json.dumps(transit_data, indent=2, ensure_ascii=False))
        print("=" * 60)
        
        # 格式化报告
        report = analyzer.format_transit_report(transit_data, "陈慧军", current_date)
        print(report)
        
        # 保存原始数据
        filename = f'chen_huijun_transit_{current_date["year"]}_{current_date["month"]:02d}_{current_date["day"]:02d}.json'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(transit_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 运势数据已保存到 {filename}")
        except Exception as e:
            print(f"\n⚠️  保存文件失败: {e}")
            
    else:
        print("\n❌ 运势分析失败")
        print("\n🔧 故障排除建议:")
        print("1. 检查 Docker 容器是否正常运行")
        print("2. 验证 API 认证令牌")
        print("3. 检查网络连接")
        print("4. 查看容器日志: docker logs humandesignapi")

if __name__ == "__main__":
    main()