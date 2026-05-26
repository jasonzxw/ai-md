# microgpt.py 原理学习规划

## Context（背景）

用户希望系统性地学习 `E:\microgpt\microgpt.py`（Karpathy 的零依赖纯 Python GPT 实现）涉及的所有原理性知识，最终目标是能独立搭建 nanoGPT（用 PyTorch 训练真正的 GPT 模型，理解工程优化）。

**用户画像**
- 数学基础：高数/线代/概率基本忘光，需要"刚刚好"路线快速捡回核心
- 编程基础：Python 入门级，无 NumPy/PyTorch 经验
- 学习时间：每天 1-2 小时
- 偏好资源：视频课程 + 文字教程/博客
- 学习方式：知识 + 动手并重

**规划设计原则**
1. **从简到难**：每个阶段都建立在前一个的基础上
2. **理论 + 实操配对**：每学一段就有可验收的代码产出
3. **以 microgpt.py 为锚点**：每个阶段都能回到这份代码理解某一块
4. **里程碑可见**：每阶段结束你都能解释清楚某个具体概念

**总周期**：约 18–22 周（4–5 个月，按每天 1-2 小时）

---

## 学习路线总览

```
Phase 0  数学地基              (3-4 周)  ┐
Phase 1  Python + NumPy 升级   (1-2 周) │  打底
Phase 2  自动求导与反向传播     (2 周)   ┘
─────────────────────────────────────────
Phase 3  神经网络基础           (2 周)   ┐
Phase 4  优化器原理             (1 周)   │  机器学习内核
Phase 5  分词与嵌入             (1 周)   ┘
─────────────────────────────────────────
Phase 6  注意力机制             (2-3 周) ┐
Phase 7  Transformer 与 GPT     (2 周)   │  Transformer 时代
Phase 8  PyTorch + nanoGPT      (3-4 周) ┘
```

---

## Phase 0：数学地基（3-4 周）

**目标**：捡回理解神经网络所必需的最小数学集合。

### 0.1 微积分核心（1 周）
**要懂的概念**
- 函数、极限、导数的几何意义（切线斜率）
- 链式法则（**这是反向传播的灵魂**）
- 偏导数、梯度的方向意义
- 简单的求导公式（多项式、exp、log、复合函数）

**推荐资源**
- 视频：3Blue1Brown《微积分的本质》（B 站全网都有，约 12 集，每集 10–20 分钟）
- 文字：可汗学院 / 宋浩《高等数学》关键章节

**动手任务**
- ✅ 手算：$f(x) = (3x+1)^2$ 的导数，分别用展开法和链式法则
- ✅ 手算：$L = -\log(\text{softmax}(z)_k)$ 对 $z_i$ 的偏导（这就是 microgpt.py 里的损失梯度！）

### 0.2 线性代数核心（1.5 周）
**要懂的概念**
- 向量、矩阵的几何意义（线性变换）
- 矩阵乘法是什么（行 × 列、组合变换）
- 转置、内积、外积
- 矩阵 × 向量 = 线性层（这就是 `linear(x, w)` 的本质）

**推荐资源**
- 视频：3Blue1Brown《线性代数的本质》（15 集左右，强烈推荐）
- 文字：MIT 18.06 Strang 课程笔记的精华部分

**动手任务**
- ✅ 手算：一个 3×2 矩阵乘以一个 2 维向量
- ✅ 对照 `microgpt.py` 第 94-95 行的 `linear` 函数，画出形状变化

### 0.3 概率与信息论入门（0.5-1 周）
**要懂的概念**
- 概率分布（离散）、条件概率
- 期望
- Softmax 是怎么把分数变成概率的
- 交叉熵损失（Cross-Entropy）的含义：为什么是 $-\log p_{\text{target}}$

**推荐资源**
- 视频：3Blue1Brown 的"Softmax & Cross-Entropy"短视频
- 文字：Chris Olah 博客《Visual Information Theory》

**动手任务**
- ✅ 用计算器算：对 logits `[2.0, 1.0, 0.1]` 做 softmax
- ✅ 解释 `microgpt.py` 第 167 行 `loss_t = -probs[target_id].log()` 为什么这么写

### Phase 0 验收
- [ ] 能在纸上推导：$L = -\log(\text{softmax}(z)_k)$ 对 $z$ 的梯度公式
- [ ] 能用一句话解释链式法则、softmax、交叉熵分别在做什么

---

## Phase 1：Python + NumPy 升级（1-2 周）

**目标**：让 Python 从"会写脚本"升级到"能读懂科学计算代码"，并掌握 NumPy（PyTorch 的前置）。

### 1.1 Python 进阶（3-5 天）
**要懂的概念**
- 列表推导、生成器、`zip`、`enumerate`
- 类与方法（`__init__`、`__add__`、`__slots__`）
- 闭包与装饰器基础
- 递归（拓扑排序里用到）

**推荐资源**
- 视频：B 站《廖雪峰 Python 教程》进阶章节
- 文字：Real Python 网站精选文章

**动手任务**
- ✅ 重读 `microgpt.py` 第 30-72 行的 `Value` 类，逐行能说出在做什么
- ✅ 自己实现一个简化版的 `Value`，只支持加法和乘法

### 1.2 NumPy 入门（1 周）
**要懂的概念**
- `ndarray`：什么是张量，shape/dtype
- 广播（broadcasting）规则
- 矩阵运算：`@`、`np.dot`、`np.matmul`
- 索引、切片、reshape
- `axis` 参数的含义

**推荐资源**
- 视频：B 站搜索"NumPy 教程"任一系列
- 文字：官方《NumPy: the absolute basics for beginners》

**动手任务**
- ✅ 用 NumPy **重写** `microgpt.py` 的 `linear`、`softmax`、`rmsnorm` 三个函数
- ✅ 比较 NumPy 版和原版在 100 次调用上的速度差异

### Phase 1 验收
- [ ] 能独立读懂任何使用 NumPy 的科学计算代码
- [ ] 理解"为什么 PyTorch 一定要用张量而不是 Python list"

---

## Phase 2：自动求导与反向传播（2 周）

**目标**：彻底搞懂 `microgpt.py` 第 29-72 行的 `Value` 类——这是整份代码最精华、也是 PyTorch 的灵魂。

### 2.1 反向传播原理（1 周）
**要懂的概念**
- 计算图（Computation Graph）是什么
- 前向传播 vs 反向传播
- 局部梯度 × 上游梯度 = 当前梯度（链式法则的代码化）
- 拓扑排序为什么是必要的（保证上游先算完）
- 梯度累加（`+=`）为什么必要

**推荐资源**（**这是本阶段的灵魂资源**）
- 视频：**Andrej Karpathy《The spelled-out intro to neural networks and backpropagation: building micrograd》**（YouTube/B 站搜，2.5 小时，看 2-3 遍）
- 文字：CS231n 的反向传播章节笔记

**动手任务**
- ✅ 跟着 Karpathy 视频，从零写出 micrograd（约 100 行）
- ✅ 在你的 micrograd 上画一个 `(a * b + c).backward()` 的计算图

### 2.2 对照 microgpt 深度阅读（3-5 天）
**动手任务**
- ✅ 给 `microgpt.py` 第 30-72 行**每一行加中文注释**
- ✅ 手工追踪：`Value(2) * Value(3) + Value(1)` 调用 `.backward()` 后每个节点的 `grad` 值
- ✅ 给 `Value` 添加 `tanh()` 方法（练手扩展）

### Phase 2 验收
- [ ] 能向别人讲清楚 backward 函数 12 行代码里每一行的作用
- [ ] 能解释为什么 `loss.backward()` 一次调用，就能算出所有参数的梯度

---

## Phase 3：神经网络基础（2 周）

**目标**：理解 GPT 里"非 Attention 的那一半"——线性层、激活函数、归一化、残差连接。

### 3.1 从感知机到 MLP（1 周）
**要懂的概念**
- 单个神经元做的事：$y = f(Wx + b)$
- 为什么需要激活函数（破除线性）
- 常见激活函数：Sigmoid、Tanh、ReLU、GeLU 的差异
- 多层感知机（MLP）的表达能力
- 损失曲面、梯度下降的直观图像

**推荐资源**
- 视频：3Blue1Brown《But what is a neural network?》系列 4 集
- 视频：Karpathy 第二集《Building makemore: bigram → MLP》
- 文字：CS231n《Neural Networks Part 1》

**动手任务**
- ✅ 用 `Value` 类搭一个 2-3-1 结构的 MLP，训练它学习 XOR
- ✅ 对照 `microgpt.py` 第 135-141 行，画出 MLP block 的数据流

### 3.2 归一化与残差（1 周）
**要懂的概念**
- 为什么深层网络难训练（梯度消失/爆炸）
- LayerNorm vs BatchNorm vs **RMSNorm**（理解 `microgpt.py` 用 RMSNorm 的原因）
- 残差连接（Residual Connection）的"高速公路"作用
- 为什么 RMSNorm 用 `1e-5` 做数值稳定

**推荐资源**
- 文字：李沐《动手学深度学习》归一化与残差章节
- 论文（轻读）：《Root Mean Square Layer Normalization》前 3 页

**动手任务**
- ✅ 拆解 `microgpt.py` 第 103-106 行的 `rmsnorm`，手算一个 4 维向量的输出
- ✅ 解释：第 116 行 `x_residual = x`、第 134 行 `x = [a + b for a, b in zip(x, x_residual)]` 在做什么

### Phase 3 验收
- [ ] 能解释为什么 Transformer 里要做 `RMSNorm → 算东西 → 加残差`
- [ ] 能讲清楚 ReLU 的导数为什么是 0 或 1

---

## Phase 4：优化器原理（1 周）

**目标**：理解 `microgpt.py` 第 146-149 行和第 174-182 行的 Adam 优化器。

**要懂的概念**
- SGD（随机梯度下降）：最简单的更新规则 `p -= lr * grad`
- 动量（Momentum）：为什么"惯性"能加速训练
- RMSProp：自适应学习率的思想
- **Adam = Momentum + RMSProp + 偏差修正**
- 学习率衰减（Learning Rate Schedule）
- 为什么要 `grad = 0` 清零

**推荐资源**
- 视频：吴恩达《深度学习专项课》优化算法章节（约 1.5 小时）
- 文字：Sebastian Ruder《An overview of gradient descent optimization algorithms》

**动手任务**
- ✅ 用纯 Python 实现 SGD、Momentum、Adam 三个优化器
- ✅ 在 Phase 3 的 XOR MLP 上对比三者的收敛速度
- ✅ 解释 `microgpt.py` 第 179-180 行的"偏差修正"为什么必要

### Phase 4 验收
- [ ] 能向别人讲清楚 Adam 的 5 行更新公式
- [ ] 能复述：β1/β2/ε 三个超参数分别是什么意思

---

## Phase 5：分词与嵌入（1 周）

**目标**：理解"文字怎么变成模型能吃的数字"。

**要懂的概念**
- 字符级 vs 词级 vs **子词（BPE）**分词
- 词嵌入（Word Embedding）的几何意义：相似词在向量空间近
- 位置嵌入（Position Embedding）：为什么 Transformer 需要它
- BOS/EOS/PAD 等特殊 token 的作用
- One-hot 编码 vs 嵌入查表

**推荐资源**
- 视频：**Andrej Karpathy《Let's build the GPT Tokenizer》**（2 小时，必看）
- 文字：Jay Alammar《The Illustrated Word2vec》

**动手任务**
- ✅ 阅读 `microgpt.py` 第 23-27 行的字符分词器，并扩展支持大小写
- ✅ 用 `tiktoken` 或 `sentencepiece` 跑一遍 BPE，对比和字符级的差异
- ✅ 解释 `microgpt.py` 第 109-111 行 `tok_emb + pos_emb` 为什么是相加而不是拼接

### Phase 5 验收
- [ ] 能解释 BPE 的核心算法（合并最高频字节对）
- [ ] 能讲清楚位置嵌入解决了什么问题

---

## Phase 6：注意力机制（2-3 周）⭐ 重中之重

**目标**：彻底吃透 Self-Attention 与 Multi-Head Attention，这是 GPT 的灵魂。

### 6.1 为什么需要 Attention（3 天）
**要懂的概念**
- RNN/LSTM 的瓶颈（不能并行、长距离依赖差）
- Attention 的核心思想：动态加权聚合上下文
- "Query、Key、Value" 的图书馆类比

**推荐资源**
- 文字：**Jay Alammar《The Illustrated Transformer》**（必读，多读几遍）

### 6.2 Self-Attention 数学（1 周）
**要懂的概念**
- 公式 $\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$ 每一步在做什么
- 为什么除以 $\sqrt{d_k}$（数值稳定 + 梯度健康）
- 因果掩码（Causal Mask）：GPT 为什么不能"偷看未来"
- 在 microgpt 中因果性是怎么"天然"实现的（只 append 历史 K/V）

**推荐资源**
- 视频：**Andrej Karpathy《Let's build GPT: from scratch》**（约 2 小时，必看 2 遍）
- 视频：3Blue1Brown《Attention in transformers, visually explained》

**动手任务**
- ✅ 在纸上手算：3 个 token、每个 4 维的 Q/K/V，算出 attention 输出
- ✅ 用 NumPy 实现单头 self-attention，验证结果

### 6.3 Multi-Head Attention + KV Cache（1 周）
**要懂的概念**
- 为什么要多头（不同头学不同关系）
- 头的拆分与拼接：`n_embd = n_head * head_dim`
- **KV Cache** 推理优化：为什么训练不需要、推理需要
- microgpt 第 121-122 行 `keys[li].append(k)` 就是 KV cache

**动手任务**
- ✅ 给 `microgpt.py` 第 114-133 行的多头注意力**逐行加注释**
- ✅ 手工追踪：n_head=2, head_dim=2, 已有 2 个历史 token, 当前是第 3 个 token，整个注意力计算流程
- ✅ 把多头注意力用 NumPy 重写一遍

### Phase 6 验收
- [ ] 能在白板上从空白写出 self-attention 的伪代码
- [ ] 能解释 KV cache 把推理复杂度从 O(n²) 降到 O(n) 的原因

---

## Phase 7：Transformer 与 GPT 整体（2 周）

**目标**：把前 6 个 phase 的零件拼成完整 GPT，吃透 `microgpt.py` 整份代码。

### 7.1 Transformer Block 全景（1 周）
**要懂的概念**
- Encoder-Decoder vs Decoder-Only（GPT 是后者）
- 一个 Block = Attention + 残差 + Norm + MLP + 残差 + Norm
- Pre-Norm vs Post-Norm
- 参数量怎么估算

**推荐资源**
- 文字：再读 Jay Alammar《The Illustrated GPT-2》
- 论文（必读）：《Attention Is All You Need》（建议精读 3、4 节）

**动手任务**
- ✅ 把 `microgpt.py` 的 `gpt` 函数（第 108-144 行）画成完整数据流图
- ✅ 算出 `microgpt.py` 默认配置下的参数量，验证和第 90 行打印的一致

### 7.2 训练与采样（1 周）
**要懂的概念**
- 自回归训练：每个位置都预测下一个 token
- Teacher Forcing（训练时用真实 token，推理时用上一步输出）
- 采样策略：
  - Greedy（取最大）
  - Temperature（控制创造性）
  - Top-K / Top-P（截断低概率）
- 过拟合的早期信号

**动手任务**
- ✅ 阅读 `microgpt.py` 第 153-184 行训练循环，逐行加注释
- ✅ 修改第 187 行 `temperature` 为 0.1 / 1.0 / 2.0，观察生成名字的差异
- ✅ 增加 top-k 采样到推理循环
- ✅ **运行 microgpt.py，让它跑出 20 个名字！** 这是阶段性的最大成就

### Phase 7 验收
- [ ] 能从头到尾讲解 `microgpt.py` 200 行代码每一段在做什么
- [ ] 能解释 temperature/top-k/top-p 三种采样的差异和适用场景

---

## Phase 8：PyTorch + nanoGPT（3-4 周）⭐ 最终目标

**目标**：从纯 Python 跨入工业级框架，搭建并训练 nanoGPT。

### 8.1 PyTorch 入门（1.5 周）
**要懂的概念**
- `torch.Tensor` vs NumPy（GPU 加速、自动求导）
- `torch.autograd`（PyTorch 自带的"Value 类"）
- `nn.Module`、`nn.Linear`、`nn.Embedding`
- `DataLoader`、batch 训练
- `optimizer.step()` / `loss.backward()` / `optimizer.zero_grad()`
- GPU 使用：`.cuda()` / `.to(device)`

**推荐资源**
- 视频：PyTorch 官方《Deep Learning with PyTorch: A 60 Minute Blitz》
- 文字：PyTorch 官方 Tutorial 前 5 篇

**动手任务**
- ✅ 用 PyTorch 重写 `microgpt.py`：每个 `Value` 替换成 `nn.Module` / `Tensor`
- ✅ 在 CPU 上跑通 PyTorch 版的 microgpt
- ✅ 如果有 GPU，对比 CPU 和 GPU 的训练速度

### 8.2 进入 nanoGPT（2-2.5 周）

**项目仓库**：https://github.com/karpathy/nanoGPT

**推荐资源（必看）**
- 视频：**Andrej Karpathy《Let's reproduce GPT-2 (124M)》**（4 小时，逐行讲 nanoGPT）

**要懂的概念（在 microgpt 基础上新增的工程优化）**
- Batch 维度：一次处理多个序列
- Mixed Precision (FP16/BF16) 训练
- Gradient Accumulation（小显存训大 batch）
- 学习率 Warmup + Cosine Decay
- 权重初始化（Xavier、He）
- AdamW（带正确权重衰减的 Adam）
- DDP（分布式数据并行，多卡训练）
- `torch.compile()` 加速

**动手任务**（按顺序逐步加难度）
- ✅ 第一步：克隆 nanoGPT 仓库，运行 `python train.py config/train_shakespeare_char.py`（字符级莎士比亚）
- ✅ 第二步：通读 `model.py`，对照 microgpt 找出每个组件
- ✅ 第三步：通读 `train.py`，理解 batch、scheduler、checkpoint 怎么做
- ✅ 第四步：在莎士比亚上训练 30 分钟，生成一段莎翁风文本
- ✅ 第五步（进阶）：换数据集（如《三国演义》或自己的语料）训练一个属于你的模型
- ✅ 第六步（进阶）：尝试改架构（增减层数、改 head 数、换激活），对比效果

### Phase 8 验收（**最终目标达成！**）
- [ ] 能从零写一个 PyTorch 版 GPT（不照抄）
- [ ] 能解释 nanoGPT 比 microgpt 多出来的每一项工程优化解决了什么问题
- [ ] 在自己的数据集上跑出一个能输出像样文本的模型
- [ ] 能向别人讲清楚"GPT 是怎么训练出来的"

---

## 关键资源清单（一次性收藏）

### 视频（按优先级）
1. **Andrej Karpathy "Neural Networks: Zero to Hero" 系列**（YouTube/B 站）—— 全程的精神支柱，覆盖 Phase 2、3、5、6、7、8
2. 3Blue1Brown《微积分的本质》《线性代数的本质》《Neural Networks》
3. 吴恩达《深度学习专项课》（B 站）
4. PyTorch 官方 60-Minute Blitz

### 文字
1. Jay Alammar 博客（The Illustrated Transformer/GPT-2/Word2vec）
2. 李沐《动手学深度学习》(d2l.ai 中文版)
3. CS231n / CS224n 课程笔记
4. PyTorch / NumPy 官方文档

### 论文（按学习顺序）
1. 《Attention Is All You Need》(2017, Vaswani)
2. 《Language Models are Unsupervised Multitask Learners》(GPT-2)
3. （可选）《Root Mean Square Layer Normalization》

### 代码仓库
1. `E:\microgpt\microgpt.py`（本仓库，全程的对照基准）
2. https://github.com/karpathy/micrograd（Phase 2 跟练）
3. https://github.com/karpathy/makemore（Phase 3-5 跟练）
4. https://github.com/karpathy/nanoGPT（Phase 8 终极目标）

---

## 每周节奏建议（每天 1-2 小时）

- **周一 / 周三 / 周五**：看视频或读教程（45-60 分钟）+ 笔记
- **周二 / 周四**：动手敲代码、做练习
- **周六**：阶段性回顾，把这周学的对照 `microgpt.py` 找位置
- **周日**：休息或自由探索（读博客、看相关视频）

**关键原则**
1. **不要跳阶段**：每个 phase 的验收清单都打勾再前进
2. **代码必须自己敲**：看懂 ≠ 写得出
3. **回看 microgpt.py 是必备动作**：它是你的锚点
4. **遇到卡点先动手**：别陷入"再多看一篇文章"的拖延陷阱
5. **每周写学习笔记**：能写出来才是真的懂了

---

## 验证整个学习是否成功

最终能做到这三件事，规划就算完成：
1. ✅ **能解释**：向一个非技术朋友讲清楚 GPT 是怎么工作的
2. ✅ **能复现**：白板上不查资料写出 self-attention 的核心代码
3. ✅ **能创造**：在自己感兴趣的数据集上训练出一个有趣的小 GPT