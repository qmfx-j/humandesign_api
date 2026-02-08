# Human Design API 完整接口文档

**版本**: 3.4.1  
**最后更新**: 2026 年 2 月 8 日  
**基础 URL**: `http://localhost:8000`

---

## 📋 目录

1. [认证机制](#认证机制)
2. [主要计算接口](#主要计算接口)
3. [运势分析接口](#运势分析接口)
4. [关系分析接口](#关系分析接口)
5. [系统接口](#系统接口)
6. [错误处理](#错误处理)
7. [最佳实践](#最佳实践)

---

## 🔐 认证机制

所有 API 接口都需要 Bearer Token 认证。

### 请求头格式

```
Authorization: Bearer <your_api_token>
```

### 获取 Token

请通过官方渠道申请您的 API Token 并妥善保管。

> ⚠️ **安全提醒**: 不要在客户端代码中暴露您的 `HD_API_TOKEN`

---

## 🧮 主要计算接口

### POST /v2/calculate ⭐【旗舰接口】

**功能描述**: 高保真度 Human Design 计算引擎，返回语义化分层 JSON 响应

#### 请求参数

```json
{
  "year": 1990,
  "month": 1,
  "day": 12,
  "hour": 8,
  "minute": 0,
  "second": 0,
  "place": "New York, USA",
  "gender": "male",
  "islive": true,
  "latitude": null,
  "longitude": null,
  "include": ["general", "gates.personality"],
  "exclude": ["channels"]
}
```

#### 参数说明

| 字段        | 类型    | 必填 | 描述                       | 默认值 |
| ----------- | ------- | ---- | -------------------------- | ------ |
| `year`      | integer | 是   | 出生年份                   | -      |
| `month`     | integer | 是   | 出生月份 (1-12)            | -      |
| `day`       | integer | 是   | 出生日期 (1-31)            | -      |
| `hour`      | integer | 是   | 出生小时 (0-23)            | -      |
| `minute`    | integer | 是   | 出生分钟 (0-59)            | -      |
| `second`    | integer | 否   | 出生秒数                   | 0      |
| `place`     | string  | 是   | 出生地点 "城市, 国家"      | -      |
| `gender`    | string  | 否   | 性别                       | "male" |
| `islive`    | boolean | 否   | 是否在世                   | true   |
| `latitude`  | float   | 否   | 显式纬度（跳过地理编码）   | null   |
| `longitude` | float   | 否   | 显式经度（跳过地理编码）   | null   |
| `include`   | array   | 否   | 包含字段列表（支持点语法） | null   |
| `exclude`   | array   | 否   | 排除字段列表（支持点语法） | null   |

#### 响应示例

```json
{
  "general": {
    "birth_date": "1990-01-12T08:00:00Z",
    "create_date": "1989-04-23T14:32:18Z",
    "birth_place": "New York, USA",
    "age": 36,
    "gender": "male",
    "islive": true,
    "zodiac_sign": "Capricorn",
    "energy_type": "Generator",
    "strategy": "Wait to Respond",
    "signature": "Satisfaction",
    "not_self": "Frustration",
    "aura": "Open & Enveloping",
    "inner_authority": "Sacral Authority",
    "inc_cross": "The Right Angle Cross of Planning (37/40 | 9/16)",
    "profile": "4/6: Opportunist Role Model",
    "definition": "Split Definition"
  },
  "centers": {
    "defined": ["Sacral", "Root"],
    "undefined": [
      "Head",
      "Ajna",
      "Throat",
      "G_Center",
      "Heart",
      "Solar Plexus",
      "Spleen"
    ]
  },
  "channels": [
    {
      "name": "The Channel of Mating",
      "gates": [6, 59],
      "meaning": "A Design Focused on Reproduction"
    }
  ],
  "variables": {
    "top_right": {
      "value": "PRL",
      "name": "Personality Right Line",
      "aspect": "Conscious",
      "def_type": "Undefined"
    },
    "bottom_right": {
      "value": "DRR",
      "name": "Design Right Reference",
      "aspect": "Unconscious",
      "def_type": "Defined"
    },
    "short_code": "PRL DRR"
  },
  "gates": {
    "personality": {
      "Sun": {
        "gate": 61,
        "line": 1,
        "color": 4,
        "tone": 6,
        "base": 3,
        "lon": 282.45,
        "gate_name": "The Gate of Inner Truth",
        "gate_summary": "Inner knowing and truth",
        "line_name": "The Initiator",
        "line_description": "One who begins anew",
        "fixation": {
          "type": "Exalted",
          "value": "Up"
        }
      }
    },
    "design": {
      "Sun": {
        "gate": 57,
        "line": 3,
        "color": 2,
        "tone": 4,
        "base": 1,
        "lon": 278.12
      }
    }
  },
  "advanced": {
    "dream_rave": {
      "activated_centers": ["Sacral", "Root"],
      "activated_gates": [61, 57],
      "status": "Active"
    },
    "global_cycle": {
      "great_cycle": "Age of Individualization",
      "cycle_cross": "Cross of the Sleeping Phoenix",
      "gates": [1, 2, 3, 4],
      "description": "Period of awakening consciousness"
    }
  }
}
```

### GET /calculate 【经典接口】

**功能描述**: 传统的 Human Design 计算接口

#### 查询参数

```
?year=1990&month=1&day=12&hour=8&minute=0&second=0&place=New York, USA&gender=male&islive=true
```

#### 响应结构

```json
{
  "general": {
    "birth_date": "1990-01-12T08:00:00Z",
    "create_date": "1989-04-23T14:32:18Z",
    "birth_place": "New York, USA",
    "energy_type": "Generator",
    "inner_authority": "Sacral Authority",
    "inc_cross": "The Right Angle Cross of Planning",
    "profile": "4/6",
    "active_chakras": ["SL", "RT"],
    "inactive_chakras": ["HD", "AA", "TT", "GC", "HT", "SN", "SP"],
    "definition": "2",
    "variables": {
      /* 变量数据 */
    },
    "age": 36,
    "zodiac_sign": "Capricorn",
    "gender": "male",
    "islive": true
  },
  "channels": [
    {
      "name": "The Channel of Mating",
      "gates": [6, 59],
      "meaning": "A Design Focused on Reproduction"
    }
  ],
  "gates": {
    "Sun": [
      {
        "gate": 61,
        "line": 1,
        "color": 4,
        "tone": 6,
        "base": 3,
        "is_active": true
      }
    ]
  }
}
```

### GET /bodygraph 【可视化接口】

**功能描述**: 生成 Human Design 身体图图像

#### 查询参数

```
?year=1990&month=1&day=12&hour=8&minute=0&second=0&place=New York, USA&fmt=png
```

#### 支持格式

- `png` (默认)
- `svg`
- `jpg` 或 `jpeg`

#### 响应

返回相应格式的图像二进制数据

---

## 🌌 运势分析接口

### GET /transits/daily 【日常运势】

**功能描述**: 分析指定日期的"当日天气"，支持旅行模式

#### 查询参数

```
?place=London,UK
&year=1990&month=1&day=1&hour=12&minute=0&second=0
&transit_year=2025&transit_month=1&transit_day=1
&current_place=New York,USA
&transit_hour=9&transit_minute=0
```

#### 参数说明

| 参数                                     | 必填 | 描述                           |
| ---------------------------------------- | ---- | ------------------------------ |
| `place`                                  | 是   | 出生地点                       |
| `year,month,day,hour,minute,second`      | 是   | 出生时间                       |
| `transit_year,transit_month,transit_day` | 是   | 目标分析日期                   |
| `current_place`                          | 否   | 当前位置（用于时区感知的运势） |
| `transit_hour,transit_minute`            | 否   | 目标小时分钟（当地时间）       |

#### 响应示例

```json
{
  "meta": {
    "birth_date": "1990-01-01T12:00:00Z",
    "create_date": "1989-04-12T08:45:30Z",
    "place": "London, UK",
    "age": 35,
    "gender": "male",
    "islive": true,
    "zodiac_sign": "Capricorn",
    "energy_type": "Generator",
    "strategy": "Wait to Respond",
    "signature": "Satisfaction",
    "not_self": "Frustration",
    "aura": "Open & Enveloping",
    "inner_authority": "Sacral Authority",
    "inc_cross": "The Right Angle Cross of Planning",
    "profile": "4/6: Opportunist Role Model",
    "definition": "Split Definition",
    "transit_date_local": "2025-01-01 09:00",
    "transit_date_utc": "2025-01-01T14:00:00Z",
    "calculation_place": "New York, USA",
    "defined_centers": ["Sacral", "Root"],
    "undefined_centers": [
      "Head",
      "Ajna",
      "Throat",
      "G_Center",
      "Heart",
      "Solar Plexus",
      "Spleen"
    ],
    "channels": {
      "Channels": [
        {
          "channel": "6/59: The Channel of Mating (A Design Focused on Reproduction)"
        }
      ]
    }
  },
  "composite_changes": {
    "new_channels": [
      {
        "gates": "20-34",
        "name": "The Channel of Community",
        "description": "Focus on collective belonging"
      }
    ],
    "new_centers": ["Heart"]
  },
  "planetary_transits": [
    {
      "planets": "Mars",
      "gate": 40,
      "line": 3,
      "color": 1,
      "tone": 5,
      "base": 2,
      "lon": 120.45
    }
  ]
}
```

### GET /transits/solar_return 【太阳回归】

**功能描述**: 计算年度主题（太阳回归）

#### 查询参数

```
?place=London,UK
&year=1990&month=1&day=1&hour=12&minute=0&second=0
&sr_year_offset=0
```

#### 特殊参数

- `sr_year_offset`: 年偏移量
  - `0`: 出生年太阳回归
  - `1`: 第一次生日回归（1991 年）
  - `35`: 2025 年回归

#### 响应结构

类似 `daily` 接口的复合分析结果

---

## 👥 关系分析接口

### POST /analyze/maia-penta ⭐【旗舰接口】

**功能描述**: 统一的关系力学引擎，结合 Maia 矩阵和 Penta 动力学

#### 请求体示例

```json
{
  "participants": {
    "Alice": {
      "place": "London, UK",
      "year": 1990,
      "month": 1,
      "day": 1,
      "hour": 12,
      "minute": 0,
      "second": 0,
      "gender": "female",
      "islive": true
    },
    "Bob": {
      "place": "New York, USA",
      "year": 1992,
      "month": 5,
      "day": 20,
      "hour": 18,
      "minute": 30,
      "second": 0,
      "gender": "male",
      "islive": true
    }
  },
  "group_type": "family",
  "verbosity": "all"
}
```

#### 参数说明

| 字段           | 类型   | 必填 | 描述                    | 可选值               |
| -------------- | ------ | ---- | ----------------------- | -------------------- |
| `participants` | object | 是   | 参与者字典（至少 2 人） | -                    |
| `group_type`   | string | 否   | 群组类型                | "family", "business" |
| `verbosity`    | string | 否   | 详细程度                | "all", "partial"     |

#### 响应特性

- **协同性分析**: 电磁、妥协、支配、陪伴连接类型
- **行星触发器**: 哪个行星激活哪个通道
- **节点共振**: 环境和谐度分析
- **Penta 动力学**: 3 人以上群组的功能角色分析

### POST /analyze/composite 【双人复合】

**功能描述**: 为恰好 2 人计算复合图表特征

#### 请求体示例

```json
{
  "person1": {
    "place": "Berlin, Germany",
    "year": 1985,
    "month": 6,
    "day": 15,
    "hour": 14,
    "minute": 30
  },
  "person2": {
    "place": "Munich, Germany",
    "year": 1988,
    "month": 11,
    "day": 22,
    "hour": 9,
    "minute": 15
  }
}
```

#### 响应结构

```json
{
  "participants": ["person1", "person2"],
  "new_channels": [
    {
      "gate": 20,
      "ch_gate": 34,
      "meaning": ["The Channel of Community", "Focus on collective belonging"]
    }
  ],
  "duplicated_channels": [
    {
      "gate": 6,
      "ch_gate": 59,
      "meaning": ["The Channel of Mating", "A Design Focused on Reproduction"]
    }
  ],
  "new_chakras": ["Heart"],
  "composite_chakras": ["Sacral", "Root", "Heart"]
}
```

### POST /analyze/penta 【群体分析】

**功能描述**: 专用的群体功能分析（3-5 人）

#### 请求体示例

```json
{
  "participants": {
    "PersonA": {
      /* 数据 */
    },
    "PersonB": {
      /* 数据 */
    },
    "PersonC": {
      /* 数据 */
    }
  },
  "group_type": "business"
}
```

#### 响应特点

返回层级化语义 JSON 结构，包含：

- 通道分析
- 功能缺口识别
- 上下功能区域划分
- 群体定义中心统计

---

## 🏥 系统接口

### GET /health 【健康检查】

**功能描述**: 检查 API 运行状态和系统信息

#### 响应示例

```json
{
  "status": "ok",
  "version": "3.4.1",
  "timestamp": "2026-02-08T10:30:00.123456",
  "dependencies": {
    "pyswisseph": "healthy"
  }
}
```

---

## ❌ 错误处理

### 状态码说明

| 状态码 | 描述           | 示例场景                   |
| ------ | -------------- | -------------------------- |
| `200`  | 成功           | 正常响应                   |
| `400`  | 错误请求       | 参数验证失败、地理编码失败 |
| `401`  | 未授权         | 缺少或无效的 Token         |
| `422`  | 无法处理的实体 | 输入格式问题               |
| `500`  | 内部服务器错误 | 计算异常、系统故障         |

### 错误响应格式

```json
{
  "detail": "具体的错误信息描述"
}
```

---

## 💡 最佳实践

### 1. 参数优化建议

#### 地理编码优化

```python
# 推荐：提供明确坐标以避免地理编码
params = {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "place": "New York, USA"  # 仍需提供用于时区判断
}
```

#### 时间精度

- 秒数参数可选，但建议提供精确到分钟
- 使用 24 小时制表示小时

### 2. 性能优化

#### 批量请求

对于多用户场景，考虑：

- 合理控制并发请求数量
- 实现适当的重试机制
- 使用连接池管理 HTTP 连接

#### 缓存策略

- 出生图表数据可以缓存（不会改变）
- 运势分析结果可根据时效性缓存
- 关系分析结果建议按组合键缓存

### 3. 安全建议

#### Token 管理

- 不要在客户端存储 Token
- 实现 Token 刷新机制
- 定期轮换 API 密钥

#### 请求频率限制

- 遵循 API 速率限制
- 实现指数退避重试策略
- 监控异常访问模式

### 4. 开发建议

#### 测试环境

- 使用测试 Token 进行开发
- 在生产环境前充分测试
- 记录关键请求和响应

#### 错误处理

```python
import requests

def calculate_hd(params, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(
            "http://localhost:8000/v2/calculate",
            json=params,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("认证失败，请检查 Token")
        elif e.response.status_code == 400:
            print(f"参数错误: {e.response.json()}")
        else:
            print(f"服务器错误: {e}")
    except requests.exceptions.RequestException as e:
        print(f"网络错误: {e}")
```

---

## 📚 相关资源

- **API 文档**: `docs/API_DOCUMENTATION.md`
- **OpenAPI 规范**: `openapi.yaml`
- **技术栈**: Python 3.12 + FastAPI + pyswisseph
- **项目架构**: 参见项目功能树内存

---

_本文档基于 Human Design API v3.4.1 生成，如有更新请及时查阅最新版本_
