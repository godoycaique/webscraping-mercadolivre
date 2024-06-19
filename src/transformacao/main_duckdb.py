import duckdb
import datetime

df = duckdb.sql("""
                select * 
                from read_csv("data/data.csv", AUTO_DETECT=FALSE, sep=',', 
                columns=
                        {
                            'title':VARCHAR, 
                            'rating': 'VARCHAR',
                            'old_price':VARCHAR, 
                            'old_cents':VARCHAR, 
                            'new_price':VARCHAR,
                            'new_cents':VARCHAR,
                            'is_free_ship':VARCHAR,
                            'is_full':VARCHAR,
                            'is_ads':VARCHAR,
                            'page': VARCHAR
                        }
                )
                """).show()