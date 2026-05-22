from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
# .env 文件位于项目根目录（config.py 的父目录的父目录的父目录）
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

"""  代码讲解
BaseSettings 做了 4 件事：
自动读取配置文件 (.env)
自动类型转换 ("3306" → 3306)
提供默认值 (如果 .env 没有就用默认值)
数据验证 (可以限制范围、格式等)

创建 Settings 对象
  ↓
读取 model_config 配置
  ↓
加载 .env 文件 (env_file=".env")
  ↓
读取系统环境变量
  ↓
合并配置（优先级：环境变量 > .env > 默认值）
  ↓
类型转换（"3306" → 3306）
  ↓
数据验证（validate_default=True）
  ↓
检查未知字段（extra="ignore/forbid"）
  ↓
返回 settings 对象


"""
class Settings(BaseSettings):
    """"""
    """
    DB_PORT: int = Field(gt=0, lt=65536, description="端口号必须 1-65535")
    DB_HOST: str = Field(min_length=1, description="主机名不能为空")
    """
    # 数据库
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "hotel_system"

    # DB_PORT: int = Field(gt=0, lt=65536, default=99999)  # ← 超过范围
    # ❌ 报错！默认值 99999 不在 0-65536 范围内

    # DeepSeek AI
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_MODEL: str = "deepseek-v4-flash"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/chat/completions"

    # test
    # 没有 UNKNOWN_CONFIG 字段

    model_config = {"env_file": str(ENV_FILE),
                    "env_file_encoding": "utf-8",
                    "case_sensitive": False,  # ← 不区分大小写（默认）
                    "extra": "ignore",  # ← 忽略未知字段（默认）
                    # "extra": "forbid",  # ← 遇到未知字段就报错
                    # "extra": "allow",  # ← 允许并保存未知字段
                    "validate_default": True,  # ← 验证默认值是否合法
                     }


settings = Settings()
