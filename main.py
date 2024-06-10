import os
import logging
import yaml
import schedule
import asyncio
from pkg.core.app import Application
from pkg.plugin.events import *
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from mirai import *
from plugins.AutoTask.pkg.Weather import get_weather
from plugins.AutoTask.pkg.bilibili import bilibili_popular
# 注册插件
@register(name="AutoTask", description="自动发送天气预报", version="0.1", author="logos")
class AutoTask(BasePlugin):

    cfg: dict = None

    def __init__(self, plugin_host: APIHost):
        global process
        with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r', encoding='utf-8') as f:
            self.cfg = yaml.safe_load(f)
    
        self.plugin_host = plugin_host
        asyncio.create_task(self.initialize_task())  # 启动初始化任务
    
    # 定义发送消息的异步独立函数
    async def send_message(self, target_type: str, target_id: str, message_content: str):
        try:
            await asyncio.sleep(5)

            platform_mgr = self.plugin_host.ap.platform_mgr
            adapter = platform_mgr.adapters[0]
            message = MessageChain([
            Plain(message_content),
            ])
            # 找到 aiocqhttp 适配器
            #adapter = next((adapter for adapter in adapters if isinstance(adapter, CQHttp)), None)
            #print(adapters)
            if adapter is None:
                logging.error("adapter not found")

            await adapter.send_message(target_type,target_id, message)    

            print(f"Message sent successfully to {target_type} {target_id}!")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

    async def initialize_task(self):
        
        schedule.every().day.at("08:00").do(lambda: asyncio.create_task(self.weather_report()))  # 自动启动定时任务
        schedule.every().day.at("08:00").do(lambda: asyncio.create_task(self.bilibili_report()))  # 自动启动定时任务
        #asyncio.create_task(self.weather_report())
        #asyncio.create_task(self.bilibili_report())
        
        asyncio.create_task(self.run_schedule())
        



    async def weather_report(self):
        print(f"-------------mission start-----------------")
        api_key = self.cfg["weather_api_key"]
        citys = self.cfg["citys"]
        target_types = self.cfg["target_types"]
        target_ids = self.cfg["target_ids"]
        for your_city, target_type, target_id in zip(citys, target_types, target_ids):
            
            weather_report = get_weather(your_city, api_key )            
            await self.send_message( target_type, target_id, weather_report)

    async def bilibili_report(self):
        print(f"-------------bilibili start----------------")
        popular_video = bilibili_popular()
        target_types = self.cfg["bili_target_types"]
        target_ids = self.cfg["bili_target_ids"]
        for target_type, target_id in zip(target_types, target_ids):          
            await self.send_message( target_type, target_id, popular_video)

    
    async def run_schedule(self):
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)

    def __del__(self):
        pass

# 自动实例化插件
#plugin_host = APIHost(Application())
#plugin = Weather(plugin_host)
