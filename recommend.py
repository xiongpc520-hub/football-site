import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

print("🤖 正在启动推荐引擎...")

# ==========================================
# 1. 准备数据 (模拟用户行为矩阵)
# ==========================================
# 假设我们有 5 个用户 (User A-E) 对 6 个视频的评分 (0-5分)
# 这些视频就像是你 data.json 里的那些
data = {
    #              梅西集锦,  C罗集锦,  瓜帅战术,  穆帅大巴,  搞笑失误,  装备评测
    'User_A':     [5,       5,       2,       1,       0,       0],   # 球星粉
    'User_B':     [4,       5,       0,       0,       1,       0],   # 球星粉
    'User_C':     [0,       0,       5,       5,       0,       1],   # 战术控
    'User_D':     [1,       0,       5,       4,       0,       0],   # 战术控
    'User_E':     [0,       1,       0,       0,       5,       5],   # 娱乐党
}

# 转换成 Pandas 表格 (DataFrame)
# .T 是转置，把用户变成行，视频变成列，这是算法的标准格式
df = pd.DataFrame(data).T 
print("\n--- 1. 用户评分矩阵 (我们有的数据) ---")
print(df)

# ==========================================
# 2. 计算相似度 (算法核心)
# ==========================================
# 核心思想：Item-based Collaborative Filtering
# 计算“视频”和“视频”之间的余弦相似度
cosine_sim = cosine_similarity(df.T) 

# 转成表格方便人类阅读
video_names = ['梅西集锦', 'C罗集锦', '瓜帅战术', '穆帅大巴', '搞笑失误', '装备评测']
sim_df = pd.DataFrame(cosine_sim, index=video_names, columns=video_names)

print("\n--- 2. 视频相似度矩阵 (AI 计算出的关系) ---")
# 这里的数字越接近 1，说明两个视频越相关
print(sim_df.round(2)) 

# ==========================================
# 3. 模拟推荐 (应用场景)
# ==========================================
def get_recommendations(video_name):
    # 拿到这个视频的相似度列表，按分数从高到低排序
    similar_scores = sim_df[video_name].sort_values(ascending=False)
    # 排除掉自己 (排第一的肯定是自己)，取前2名
    return similar_scores.iloc[1:3] 

# 场景测试 1：用户正在看梅西
current_watching = '梅西集锦'
recommendations = get_recommendations(current_watching)

print(f"\n--- 3. 模拟推荐结果 ---")
print(f"👁️  用户正在看: [{current_watching}]")
print(f"💡 AI 猜你喜欢:")
for video, score in recommendations.items():
    print(f"   -> {video} (相似度: {score:.2f})")

# 场景测试 2：用户正在看瓜迪奥拉
current_watching_2 = '瓜帅战术'
recommendations_2 = get_recommendations(current_watching_2)
print(f"\n👁️  用户正在看: [{current_watching_2}]")
print(f"💡 AI 猜你喜欢:")
for video, score in recommendations_2.items():
    print(f"   -> {video} (相似度: {score:.2f})")