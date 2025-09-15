-- 1. AI 角色表
CREATE TABLE AIs (
    ai_id SERIAL PRIMARY KEY,                                 -- AI 唯一 ID
    profile TEXT                                              -- 存 YAML（profile）
);

-- 2. 场景表
CREATE TABLE scenes (
    scene_id SERIAL PRIMARY KEY,                              -- 场景唯一 ID
    ai_id INT REFERENCES AIs(ai_id),                          -- 关联 AI
    scene TEXT                                                -- 存 YAML（scene）
);

-- 3. 好感度表（只解决好感度的prompt的存储）
CREATE TABLE affection_levels (
    af_id SERIAL PRIMARY KEY,                                 -- 好感度唯一 ID
    ai_id INT REFERENCES AIs(ai_id),                          -- 关联 AI
    affection_level TEXT                                      -- 存 YAML（affection level）
);
-- 4. 会话表
CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,                            -- 会话唯一 ID
    user_id INT NOT NULL,                                     -- 外部传入的用户 ID
    ai_id INT REFERENCES AIs(ai_id),                          -- AI 配置 ID（来自 YAML）
    scene INT REFERENCES scenes(scene_id),                    -- 场景 ID（来自 YAML）
    current_affection INT DEFAULT 0,                          -- 当前情感值
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,           -- 会话开始时间
    end_time TIMESTAMP,                                       -- 会话结束时间（可空）
    is_active BOOLEAN DEFAULT TRUE,                           -- 是否正在进行中
    metadata JSONB DEFAULT '{}'                               -- 扩展信息
);

-- 5. 消息表
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,                            -- 消息唯一 ID
    session_id INT REFERENCES sessions(session_id),           -- 关联会话
    role VARCHAR(10) CHECK (role IN ('user','ai','system')),  -- 消息角色
    text TEXT,                                                -- 主要文本
    content JSONB NOT NULL,                                   -- 完整消息结构
    affection_snapshot INT,                                   -- 当时情感值快照
    token_count INT,                                          -- token 数
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,            -- 消息时间
    model_name VARCHAR(255) DEFAULT '{}',                     -- 模型名称
    error_info JSONB DEFAULT '{}'                             -- 消息级错误
);

-- 6. 错误日志表
CREATE TABLE error_logs (
    error_id SERIAL PRIMARY KEY,                              -- 错误唯一 ID
    session_id INT REFERENCES sessions(session_id),           -- 出错所属会话
    error_type VARCHAR(50) NOT NULL,                          -- 错误类别
    error_message TEXT,                                       -- 错误描述
    details JSONB DEFAULT '{}',                               -- 错误上下文
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,          -- 错误时间
    resolved BOOLEAN DEFAULT FALSE                            -- 是否已解决
);

-- 7. 对话简表
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,                                                -- 平台（微信/QQ/网页等）
    user_id VARCHAR(100) NOT NULL,                                                -- 用户ID
    ai_id INT REFERENCES AIs(ai_id) ON DELETE SET NULL,                           -- 外键: AI角色
    scene_id INT REFERENCES Scenes(scene_id) ON DELETE SET NULL,                  -- 外键: 场景
    affection_level_id INT REFERENCES Affection_levels(af_id) ON DELETE SET NULL, -- 外键: 好感度
    role VARCHAR(20) NOT NULL,                                                    -- user/ai/system
    content TEXT NOT NULL,                                                        -- 聊天内容
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
