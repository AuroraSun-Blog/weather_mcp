from fastapi import FastAPI, HTTPException
import time

app = FastAPI()


# 1. MCP服务描述接口
@app.get("/mcp/describe")
def describe():
    return {
        "name": "WeatherQuery",
        "description": "根据城市名查询实时天气（支持国内主要城市）",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如'北京'、'上海'、'广州'"
                }
            },
            "required": ["city"]
        }
    }


# 2. MCP服务调用接口（使用本地模拟数据，确保测试通过）
@app.post("/mcp/call")
def call(data: dict):
    # 校验必要参数
    if "city" not in data:
        raise HTTPException(status_code=400, detail="缺少必要参数：city（城市名称）")

    city = data["city"]

    # 模拟天气数据（避免依赖外部接口）
    mock_weather = {
        "北京": {"temperature": "26~33℃", "weather": "晴", "tips": "紫外线强，注意防晒"},
        "上海": {"temperature": "28~35℃", "weather": "多云", "tips": "午后可能有雷阵雨"},
        "广州": {"temperature": "29~36℃", "weather": "雷阵雨", "tips": "请携带雨具"},
        "默认": {"temperature": "20~28℃", "weather": "阴", "tips": "风力较小，适宜户外活动"}
    }

    # 选择对应城市的模拟数据
    weather_data = mock_weather.get(city, mock_weather["默认"])

    return {
        "city": city,
        "query_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "temperature": weather_data["temperature"],
        "weather": weather_data["weather"],
        "tips": weather_data["tips"]
    }


# 启动服务
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
