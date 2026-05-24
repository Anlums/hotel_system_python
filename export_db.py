"""导出本地 MySQL 数据到 SQL 文件"""
import pymysql, os
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "hotel_system"),
    charset="utf8mb4",
)

tables = ["rooms", "bookings", "cleaning_tasks", "service_menu",
          "room_service_orders", "price_history", "members", "payments"]

with open("full_data.sql", "w", encoding="utf8") as f:
    f.write("-- 天玺尊邸酒店管理系统 - 完整数据导出\n\n")
    for table in tables:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]

            sql_cols = ", ".join(f"`{c}`" for c in cols)

            f.write(f"TRUNCATE TABLE `{table}`;\n")
            for row in rows:
                vals = []
                for col_name, v in zip(cols, row):
                    if v is None:
                        # 处理 NOT NULL 列的 NULL 值
                        if col_name in ("check_out_date",):
                            vals.append("'2000-01-01 00:00:00'")
                        elif col_name in ("total_amount",):
                            vals.append("0.00")
                        else:
                            vals.append("NULL")
                    elif isinstance(v, (int, float)):
                        vals.append(str(v))
                    else:
                        escaped = str(v).replace("\\", "\\\\").replace("'", "\\'")
                        vals.append(f"'{escaped}'")
                sql_vals = ", ".join(vals)
                f.write(f"INSERT INTO `{table}` ({sql_cols}) VALUES ({sql_vals});\n")
            f.write(f"-- {table}: {len(rows)} rows\n\n")

conn.close()
print(f"已导出 {sum(1 for _ in open('full_data.sql'))} 行到 full_data.sql")
