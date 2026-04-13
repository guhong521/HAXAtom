import sqlite3
import json

conn = sqlite3.connect('data/db/haxatom.db')
cursor = conn.cursor()

# 获取所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print(f"数据库中有 {len(tables)} 个表: {tables}\n")

# 检查每个表的 JSON 字段
for table in tables:
    print(f"\n检查表：{table}")
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    
    # 查找 JSON 类型的列
    json_columns = [col[1] for col in columns if col[2].upper() == 'JSON']
    
    if json_columns:
        print(f"  JSON 字段：{json_columns}")
        
        for json_col in json_columns:
            # 查找 NULL 或空值的记录
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {json_col} IS NULL OR {json_col} = ''")
            null_count = cursor.fetchone()[0]
            
            if null_count > 0:
                print(f"    - {json_col}: {null_count} 条空值记录")
                
                # 修复：设置为 [] 或 {}
                if 'disabled' in json_col or 'selected' in json_col or 'plugins' in json_col or 'bases' in json_col:
                    cursor.execute(f"UPDATE {table} SET {json_col} = '[]' WHERE {json_col} IS NULL OR {json_col} = ''")
                    print(f"      ✓ 已修复为 []")
                elif 'params' in json_col or 'variables' in json_col or 'overrides' in json_col:
                    cursor.execute(f"UPDATE {table} SET {json_col} = '{{}}' WHERE {json_col} IS NULL OR {json_col} = ''")
                    print(f"      ✓ 已修复为 {{}}")
                else:
                    cursor.execute(f"UPDATE {table} SET {json_col} = '[]' WHERE {json_col} IS NULL OR {json_col} = ''")
                    print(f"      ✓ 已修复为 []")
            else:
                print(f"    - {json_col}: OK")

conn.commit()
conn.close()

print("\n✓ 数据库修复完成")
