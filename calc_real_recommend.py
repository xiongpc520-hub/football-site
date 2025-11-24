import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

print("🚀 正在加载真实数据...")

# 1. 读取你之前爬下来的真实 B 站数据
with open('data.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

# 转成 DataFrame 方便处理
df = pd.DataFrame(videos)
print(f"✅ 加载了 {len(df)} 个视频")

# ==========================================
# 核心算法：TF-IDF (自然语言处理)
# ==========================================
# 我们要分析 'title' (标题)。
# analyzer='char' 表示按字分析，这样不用分词也能处理中文（比如 "足球" 和 "足坛"）
tfidf = TfidfVectorizer(analyzer='char', ngram_range=(1, 2))

# 计算每个标题的“特征向量”
tfidf_matrix = tfidf.fit_transform(df['title'])

# 计算余弦相似度 (和之前一样，只是数据源变了)
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# ==========================================
# 生成推荐结果并存入数据
# ==========================================
print("🧠 正在计算推荐关系...")

# 这里的逻辑是：给每个视频加一个 'related_videos' 字段
for idx, row in df.iterrows():
    # 拿到当前视频的相似度分数
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # 按分数排序 (从高到低)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # 取前 3 名 (排除掉第 0 名，因为第 0 名是它自己)
    sim_scores = sim_scores[1:4]
    
    # 找到这 3 个视频的 ID 和 标题
    recommendations = []
    for i, score in sim_scores:
        rec_video = {
            "title": df.iloc[i]['title'],
            "pic": df.iloc[i]['pic'],
            "score": round(score, 2) # 保留两位小数
        }
        recommendations.append(rec_video)
    
    # 把推荐结果写回原始数据
    videos[idx]['related'] = recommendations

# 3. 保存成新的文件，供前端使用
with open('data_with_ai.json', 'w', encoding='utf-8') as f:
    json.dump(videos, f, ensure_ascii=False, indent=2)

print("🎉 成功！已生成 'data_with_ai.json'，里面包含了 AI 推荐结果！")