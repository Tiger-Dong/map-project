import requests
import json
import csv

# 关键词列表，包含各种设施类型
combined_list_GD = [
    "ATM",                # 银行ATM
    "Beauty-Salon",       # 美容美发店
    "Clinic",             # 诊所
    "CVS",                # 便利店
    "Fire-Department",    # 消防站
    "Gas-Station",        # 加油站
    "Government",         # 政府机关相关
    "Hospital",           # 医院
    "Hotel",              # 酒店/旅馆
    "KFC",                # 肯德基
    "Kindergarten",       # 幼儿园
    "Laundry",            # 洗衣店
    "Library",            # 图书馆
    "Logistics",          # 物流速递
    "McDonald's",         # 麦当劳
    "Middle-School",      # 中学
    "Movie-Theater",      # 影剧院
    "Museum",             # 博物馆
    "Newsstand",          # 报刊亭
    "Police",             # 警察局
    "Post-Office",        # 邮局
]

def get_nearby_poi_for_keywords(api_key):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"  # Google Places API 基本URL
    all_results = []  # 用于存储所有结果的列表

    # 遍历每个关键词，进行API请求
    for keyword in combined_list_GD:
        params = {
            'key': api_key,  # API密钥
            'keyword': keyword,  # 搜索关键词
            'location': '37.7749,-122.4194',  # 搜索位置（例如：旧金山）
            'radius': 1000  # 搜索半径（以米为单位）
        }
        while True:
            response = requests.get(base_url, params=params)  # 发送GET请求
            if response.status_code == 200:  # 检查响应状态码是否为200（成功）
                results = response.json().get('results', [])  # 获取结果列表
                for result in results:
                    # 过滤结果，只保留名称、位置和评分
                    filtered_result = {
                        'keyword': keyword,
                        'name': result.get('name'),
                        'location': result['geometry']['location'],
                        'rating': result.get('rating')
                    }
                    all_results.append(filtered_result)  # 将过滤后的结果添加到总结果列表中
                next_page_token = response.json().get('next_page_token')  # 获取下一页的token
                if not next_page_token:  # 如果没有下一页，退出循环
                    break
                params['pagetoken'] = next_page_token  # 更新请求参数，添加分页token
            else:
                print(f"Error fetching data for {keyword}: {response.status_code}")  # 打印错误信息
                break

    # 如果有结果，保存到CSV文件中
    if all_results:
        csv_file = 'SanFrancisco_poi_data.csv'
        csv_columns = ['keyword', 'name', 'location', 'rating']

        try:
            with open(csv_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in all_results:
                    writer.writerow(data)
            print("Data saved to SanFrancisco_poi_data.csv")
        except IOError:
            print("I/O error")

        # 打印保存成功信息
        print("Data saved to SanFrancisco_poi_data.csv")  # 打印保存成功信息
    else:
        print("No data to save")  # 如果没有结果，打印提示信息
        

# 获取实际的Google API密钥
api_key = "AIzaSyBTfH6wqUcn8PzR4KmlXFEL5fJH5OAKk5o"  # 替换为实际API密钥
# 调用函数
get_nearby_poi_for_keywords(api_key)

