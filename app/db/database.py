# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
"""
create_async_engine → 创建数据库引擎（类似 DataSource）
async_sessionmaker → 创建会话工厂（类似 EntityManagerFactory）
AsyncSession → 数据库会话（类似 EntityManager / SqlSession）
DeclarativeBase → ORM 基类（类似 JPA 的 @Entity 基类）
settings → 刚才讲的配置对象
"""
# 1. 拼出 MySQL 连接 URL
# 注意格式：mysql+aiomysql://用户名:密码@主机:端口/数据库名
DATABASE_URL = (f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
                f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8mb4")

# 2. 创建异步引擎
# echo=True 会在控制台打印 SQL 语句，方便调试（对标 MyBatis 的 StdOutImpl）
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. 创建异步会话工厂
# 每次调用 async_session() 得到一个数据库会话
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 4. ORM 基类 —— 所有 Model 都要继承它
# 对标 MyBatis 里每个 Entity 类
"""

"""

class Base(DeclarativeBase):
    pass

# 5. 依赖函数 —— 给 FastAPI 路由用的
# 每次请求进来，自动创建一个数据库会话，请求结束后自动关闭
async def get_db():
    async with async_session() as session:
        # yield 有 return 交出值的效果，但函数不会终止，还能在调用方用完之后回来继续执行剩余代码，这是 return 做不到的。
        yield session
        # session.close()  # 调用方用完后，回来继续执行这里,不过使用了with as 自动执行了