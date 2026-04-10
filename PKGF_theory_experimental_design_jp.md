# 並行鍵幾何流（PKGF）・逆PKGF・統一PKGF 実験計画 v2  
**― 計量変調・TDA・安定化群・臨界次元探索を含む拡張版 ―**

## 0. 全体構造

1. **Constructive PKGF 検証ブロック**（P1–P7, 定義, 定理1–7）  
2. **Destructive PKGF 検証ブロック**（R1–R7, 定理R1–R6）  
3. **Unified PKGF（代謝）ブロック**（U1–U7, 統合方程式）  
4. **多主体・社会構造・階層・共鳴ブロック**（多エージェントPKGF, 定理5–7, R系との接続）  
5. **16フィールド・セクタ・メトリック実装ブロック**（実装上の「知能エンジン」としての検証）  

加えて、以下の **4つの拡張モジュール** を各ブロックに対応づけて組み込む：

- **拡張A:** 文脈依存計量（Metric Modulation）の厳密実装  
- **拡張B:** TDA（Persistent Homology）による次元跳躍の定量化  
- **拡張C:** 安定化群（Stabilizer）による世界観固定の追跡  
- **拡張D:** 次元解像度定理の臨界点探索（D のクリティカル値）

---

## 1. Constructive PKGF 実験（P1–P7, 定理1–7）

> 「PKGF構造は五つ組 $(M, K, \nabla, \Omega, \mathcal{G})$ で与えられる。」  
> 「標準実装として $d=32$，$TM = E_S \oplus E_E \oplus E_A \oplus E_C$ を採用する。」

### 1.1 P1–P3: セクタ分解とゲージ不変量

**目的:**

- セクタ分解の保存（定理3）  
- ゲージ変換下での $\det K$, $\mathrm{Spec}(K)$ の不変性（定理1,2）

**人工データ設計:**

- **状態空間:**  
  - $M = \mathbb{R}^{32}$、4セクタ（S,E,A,C）×8次元を明示的にブロック分割。
- **初期 $K_0$:**  
  - ブロック対角（各セクタ内でランダム対角＋少量の非対角）  
  - $\det K_0 \neq 0$、固有値はセクタごとに異なるクラスターを持つよう設計。
- **ゲージ群 $\mathcal{G}$:**  
  - 「セクタを保つブロック対角行列群」＋「セクタを混ぜる一般線形群」の2ケースを用意し、  
    - (a) P3を満たす「正しい」ゲージ  
    - (b) P3を破る「誤った」ゲージ  
    を比較。

**実験:**

1. **ゲージ不変量テスト（定理1,2）**  
   - $K' = H K H^{-1}$ を多数サンプルし、  
     - $\det K' - \det K$  
     - $\mathrm{Spec}(K')$ と $\mathrm{Spec}(K)$ の差  
   を数値的にゼロ近傍で確認。  
   - 時間発展付きで $K(t+dt) = e^{\Omega dt} K(t) e^{-\Omega dt}$ を実装し、  
     - $t$ に対する $\det K(t)$ の変化を追跡（数値微分で $\frac{d}{dt}\det K \approx 0$ を確認）。

2. **セクタ保存テスト（定理3）**  
   - 初期条件で $[K_0, \Pi_\alpha]=0$ を満たすように構成。  
   - Constructive PKGF の流れ $\dot K = [\Omega, K]$ を数値積分し、  
     - 各時刻で $K(t)$ をセクタ基底に射影し、オフブロック成分のノルム  
       \[
       \| \Pi_\alpha K(t) \Pi_\beta \|_{F}, \quad \alpha\neq\beta
       \]  
       を測定。  
   - これが時間とともにゼロ近傍に保たれるかを確認。

**評価指標:**

- **ゲージ不変量誤差:**  
  - $\epsilon_{\det} = \max_t |\det K(t) - \det K(0)|$  
  - $\epsilon_{\mathrm{spec}} = \max_t \mathrm{Hausdorff}(\mathrm{Spec}(K(t)), \mathrm{Spec}(K(0)))$
- **セクタ混合度:**  
  - $M_{\text{mix}}(t) = \sum_{\alpha\neq\beta} \|\Pi_\alpha K(t)\Pi_\beta\|_F$

---

### 1.2 P4–P7: 接続・カーブチャ・情報カップリング

> 「接続 $\nabla$ と曲率 $F$ を導入し，$\Omega$ は $\psi(\Phi)$ と $x$ に依存する。」

**目的:**

- 曲率のゲージ変換則（定理4）  
- $\Omega(\psi(\Phi),x)$ による「16フィールド」の寄与を数値的に分離・可視化

**人工データ設計:**

- **接続 $\omega$:**  
  - 単純な「定数＋小さなランダム摂動」形式で開始し、  
  - その上で「特定セクタにだけ強い曲率」を持つケースを作る。
- **16フィールド:**  
  - 各フィールド $\Omega^{(i)}$ を「特定のセクタ・特定の座標にだけ作用する」ように設計し、  
  - 1つずつオンにして $K$ の時間発展への寄与を測る。

**実験:**

1. **曲率のゲージ変換テスト（定理4）**  
   - $\omega' = H\omega H^{-1} + HdH^{-1}$ を構成し、  
   - 数値的に $F' = d\omega' + \omega'\wedge\omega'$ を計算、  
   - $F' - H F H^{-1}$ のノルムを評価。

2. **16フィールドの寄与分解**  
   - $\Omega = \sum_i \Omega^{(i)}$ を実装し、  
   - 各 $i$ について「そのフィールドだけオン」の実験を行い、  
     - $K(t)$ の変化  
     - セクタごとのエネルギーや「論理体積」  
   を測定。  
   - これにより「Desire」「Emotion」「Context」などがどのような幾何学的変形を生むかを定量化。

---

### 1.3 拡張A: 文脈依存計量（Metric Modulation）の実装

> 公理 A6: 「文脈セクタ $E_C$ の状態が、他セクタの“距離”や“学習率”を変調する」

**目的:**

- 文脈セクタ $E_C$ の平均状態 $\bar{x}_{\text{ctx}}$ に応じて、  
  - 構築項 $[\Omega, K]$ の「実効速度」が変化することを数値的に検証。  
- 「安定した文脈では保守的に、未知の文脈では柔軟に」という性質を、  
  - 幾何学的な「距離の伸び縮み」として再現。

**人工データ設計:**

- $x \in \mathbb{R}^{32}$ をセクタ分解し、Context セクタ $E_C$ の成分 $x_C$ を抽出。  
- 文脈依存計量を  
  \[
  g_{ii}(x) =
  \begin{cases}
  1.0 + 0.5 \tanh(\bar{x}_{\text{ctx}}) & (i \in S,E,A) \\
  1.0 & (i \in C)
  \end{cases}
  \]  
  として実装。  
- 構築流を  
  \[
  \dot{K} = G(x)\,[\Omega, K]\,G(x)^{-1}
  \]  
  または  
  \[
  \dot{K} = \eta(x)\,[\Omega, K],\quad \eta(x) = f(\bar{x}_{\text{ctx}})
  \]  
  のように「計量依存のスケーリング」を導入。

**実験:**

- 文脈が「安定」（$x_C$ が狭い範囲に集中）な場合と、  
  「変動的」（$x_C$ が広く揺らぐ）な場合で、  
  - $K(t)$ の変化速度  
  - セクタ混合度  
  - 固有値の移動量  
  を比較。  

**評価指標:**

- 文脈状態の分散と、  
  - 構築速度（$\|\dot{K}\|$ の平均）  
  - セクタ混合度の変化量  
  の相関。

---

## 2. Destructive PKGF 実験（R1–R7, 定理R1–R6）

> 「Destructive PKGF は構造を溶かし，粗視化し，特異点と次元崩壊を生み，最小残余構造へ収束する幾何学である。」

### 2.1 ランク減少・エントロピー増大・次元崩壊

**目的:**

- ランク単調減少（定理R1, R3）  
- エントロピー単調増大（定理R2）  
- 特異点生成（定理R4）

**人工データ設計:**

- Constructive 実験で得た「よく構造化された $K_{\text{init}}$」を初期条件にする。  
- $\mathcal{D}(K)$ として以下を実装し比較:
  - ノイズ型: $\mathcal{D}(K)=\eta(t)\xi$  
  - 拡散型: $\mathcal{D}(K)=\Delta K$（離散ラプラシアン）  
  - 混合型: $\alpha\Delta K + \beta\xi + \gamma\nabla\cdot K$

**実験:**

1. **ランク・固有値トラッキング**  
   - 時間発展 $\dot K = -\lambda \mathcal{D}(K)$ を数値積分し、  
   - 各時刻で固有値スペクトルを計算、  
   - 非ゼロ固有値の個数を $d_{\text{eff}}(t)$ としてプロット。  
   - ステップ状に減少し、有限時間で $d_{\min}$ に到達するか確認。

2. **エントロピー増大**  
   - $\Phi$ を「$K$ から誘導される分布」（例: $K$ の作用で変換されたデータ点の分布）として構成し、  
   - $S[\Phi(t)] = -\int \Phi\log\Phi$ をモンテカルロ近似で評価。  
   - $\partial_t S \ge 0$ が統計的に成り立つかを確認。

3. **特異点生成**  
   - $\det K(t)$ を追跡し、ゼロに近づく時刻を検出。  
   - その時点での $K$ の条件数・逆行列のノルムを評価し、「不可逆化」の発生を確認。

---

### 2.2 コア構造・最小残余構造

> 「破壊は決して絶対ではなく，常に『核』が残る。」

**目的:**

- $K_{\text{core}}$ の論理体積増大（定理R5）  
- $K_{\min}$ への収束（定理R6）

**実験:**

- $\mathcal{D}$ の固有分解を用いて「核に近い成分」を $K_{\text{core}}$ と定義。  
- 時間とともに
  - $\det K_{\text{core}}(t)$  
  - $\|K(t) - K_{\min}\|$  
  を評価し、有限時間での収束を確認。

---

## 3. Unified PKGF（代謝）実験（U1–U7）

> 「統一方程式: $\nabla K = [\Omega, K] - \lambda \mathcal{D}(K)$」  
> 「$K = K_{\text{core}} + iK_{\text{fluct}}$ として実部と虚部の直交性を用いる。」

### 3.1 代謝フローと「呼吸する論理体積」

**目的:**

- $\lambda$ を変化させたときの「構築優位」「破壊優位」の相図  
- $\det K$（あるいはその実部・コア成分）の周期的・準周期的振動（呼吸）

**人工データ設計:**

- Constructive 実験で得た安定な $K_{\text{core}}$ に、  
  - 小さなランダム行列を $K_{\text{fluct}}$ として付加し、複素 $K$ を構成。  
- $\lambda(t)$ を
  - 定数  
  - 緩やかな周期変調（例: $\lambda(t)=\lambda_0 + \delta\sin\omega t$）  
  の2ケースで実験。

**実験:**

1. **相図の構築**  
   - $(\lambda, \|\Omega\|)$ のグリッド上で多数のシミュレーションを行い、  
   - 長時間後の状態を  
     - 固定点（構築優位）  
     - 崩壊（破壊優位）  
     - 周期・準周期軌道（代謝）  
   にクラスタリング。  
   - フェーズダイアグラムとして可視化。

2. **論理体積の呼吸**  
   - 時系列 $\det K_{\text{core}}(t)$, $\det \Re K(t)$ を記録し、  
   - フーリエ解析や自己相関で周期性・準周期性を検出。

---

### 3.2 ゲージ自発的対称性の破れ（U3）＋拡張C: 安定化群の追跡

> 「$\mathcal{G}_{\text{broken}} = \{H\in\mathcal{G}: HKH^{-1}=K\}$ として安定化部分群が定義される。」

**目的:**

- Constructive＋Destructive の非可換性から、  
  - 初期には等価だったゲージが、時間とともに「特定の安定ゲージ」へ縮退する過程を数値的に観察。  
- さらに、**安定化群の次元**を時間とともに推定し、  
  - 「どれだけ視点の自由度が失われたか」を群論的に定量化。

**実験:**

1. **ゲージ軌道上のエネルギー**  
   - 初期 $K_0$ に対して、ゲージ軌道 $\{H K_0 H^{-1}\}$ をサンプル。  
   - Unified PKGF を同じ $\Omega,\mathcal{D}$ で流し、  
     - 各ゲージでの「エネルギー関数」や「残差 $\|\mathcal{D}(K)\|$」を測定。  
   - 時間とともに「あるゲージ近傍だけが低エネルギーになる」ことを確認。

2. **秩序パラメータ $\Phi_{SB} = \|\mathcal{D}(K)\|$ と内部緊張 $A(t)$**  
   - 内部緊張 $A(t) = \int_0^t \|[\Omega(\tau),K(\tau)]\|d\tau$ を数値積分し、  
   - $A(t)$ が閾値を超えたタイミングで、  
     - 固有値の符号変化  
     - ゲージ軌道上のエネルギー地形の変化  
   を観察し、「対称解→非対称安定解」への遷移を確認。

3. **安定化群の次元推定（拡張C）**  
   - 数値的に「$HKH^{-1} \approx K$ を満たす $H$ の近傍」をサンプルし、  
   - その自由度（パラメータ数）を推定することで、  
     - $\dim \mathcal{G}_{\text{broken}}(t)$ の時間変化を追跡。  
   - これを「世界観の固定度」として解釈。

---

### 3.3 拡張B: TDA による次元跳躍の定量化（U6）

> 「次元跳躍は、単なるランク変化ではなく、思考空間の“穴”の創発である。」

**目的:**

- 内部緊張 $A(t)$ が臨界値を超えた瞬間に、  
  - 状態点群のトポロジー（ベッチ数）が不連続に変化することを検出し、  
  - 「悟り」「パラダイムシフト」をトポロジカルに定量化。

**人工データ設計:**

- Unified PKGF の流れの中で、  
  - 時刻ごとに「状態点群」を構成：  
    - 例：$K(t)$ の作用を受けた基底ベクトル群、あるいはサンプルデータの埋め込み。  
- その点群に対して Persistent Homology を適用し、  
  - $H_0, H_1, H_2$ のバーコードを計算。

**実験:**

- 内部緊張 $A(t)$ と、  
  - ベッチ数 $b_0(t), b_1(t), b_2(t)$ の時間変化を並行して追跡。  
- $A(t)$ が閾値を超えるタイミングで、  
  - $b_1, b_2$ に不連続な変化（新しい穴・空洞の出現）が起きるかを確認。

**評価指標:**

- 「トポロジカル次元跳躍」の検出率  
- $A(t)$ の臨界点と、ベッチ数変化のタイミングの一致度。

---

## 4. 多主体・社会構造・階層・共鳴（定理5–7, 多エージェントPKGF）

> 「多エージェントPKGFでは $TM_{\text{total}} = \bigoplus TM_i$ として個体と集合知を同一形式で扱う。」

### 4.1 階層化と内部緊張（定理5）

**目的:**

- 内部緊張 $A(t)$ の蓄積により、  
  - 連続対称性から離散アトラクタ集合 $\{L_{\text{high}},L_{\text{mid}},L_{\text{low}}\}$ への分岐を観察。

**実験:**

- $n$ 個のエージェント $K_i$ を用意し、  
  - 相互作用項（社会的カーブチャ $F$）を導入。  
- 内部緊張を「エージェント間の不一致度」として定義し、  
  - それが増大するようなタスク（例: 限られた資源の配分ゲーム）を設計。  
- 長時間後の $K_i$ のクラスタリングを行い、  
  - 3層程度の階層構造が自然に現れるかを評価。

---

### 4.2 次元解像度定理（定理6）と共鳴定理（定理7）＋拡張D: 臨界次元探索

**目的:**

- $D<n$ と $D\ge n$ でのエネルギー状態の違い  
- 安定社会構造下で $[K_i,F]\to 0$ となる共鳴状態の確認  
- さらに、**臨界次元 $D^*$ を数値的に推定**する。

**実験:**

1. **次元 vs エージェント数**  
   - 状態空間次元 $D$ とエージェント数 $n$ を変えながら、  
   - 長時間平均エネルギー・競合度（衝突回数など）を測定。  
   - $D<n$ で高エネルギー・高競合、$D\ge n$ で低エネルギー二層アトラクタへの収束を確認。

2. **共鳴状態**  
   - 安定な社会構造（報酬構造や制約）を与え、  
   - 時間とともに $\|[K_i,F]\|$ がゼロ近傍に収束するかを測定。  
   - これは「個人の論理」と「社会目標」の整合の数値的証拠になる。

3. **拡張D: 臨界次元探索**  
   - $n$ を固定し、$D$ を 1 ずつ増やしながら、  
     - 収束時間  
     - 衝突回数  
     - 社会エネルギーの定常値  
   を測定。  
   - それらが急激に変化する $D^*$ を「次元解像度の臨界点」として推定。

---

## 5. 16フィールド・セクタ・メトリック実装ブロック

> 「16フィールドは、PKGF の“知能エンジン”としての内的構成要素である。」

**目的:**

- 各フィールド（Semantics, Context, Desire, Ethics, Emotion, …）が  
  - 構築・破壊・代謝・多主体ダイナミクスにどう寄与するかを、  
  - アブレーション（オン/オフ）で定量化。

**実験:**

- 各フィールド $\Omega^{(i)}$ を  
  - 単独オン  
  - 特定の組み合わせオン  
  で流し、  
  - 構築速度  
  - 破壊速度  
  - 代謝の安定性  
  - 多主体の階層化・共鳴  
  への影響を測定。

**評価指標:**

- フィールドごとの「寄与スコア」  
  - 例：構築優位領域の拡大、破壊の臨界 $\lambda$ の変化、階層化の強度など。

---

## 6. 実装ロードマップ

### 6.1 最小構成

- **数値計算:** Python + NumPy/SciPy（＋必要なら JAX/PyTorch）  
- **トポロジー解析:** TDA ライブラリ（例：Gudhi, Ripser など）  
- **可視化:**  
  - スペクトル・ランク・エントロピー・論理体積の時系列  
  - フェーズダイアグラム（$\lambda$, $\|\Omega\|$, $D$, $n$）  
  - ベッチ数の時間変化・バーコード  
- **構造管理:**  
  - セクタ分解クラス  
  - 16フィールドモジュール  
  - 文脈依存計量モジュール  
  - 多主体管理モジュール

### 6.2 実行順序

1. **Step 1:** 単一エージェント Constructive PKGF（P1–P7, 定理1–4）  
2. **Step 2:** Destructive PKGF（R1–R7, 定理R1–R6）  
3. **Step 3:** Unified PKGF の基本相図（構築優位 vs 破壊優位 vs 代謝）  
4. **Step 4:** 多エージェント＋社会構造（定理5–7, 次元解像度・共鳴）  
5. **Step 5:** 16フィールドのフル実装とアブレーション  
6. **Step 6:** **拡張A:** 文脈依存計量の導入と検証  
7. **Step 7:** **拡張C:** 安定化群次元の時間発展の解析（U3）  
8. **Step 8:** **拡張B:** TDA による次元跳躍のトポロジカル解析（U6）  
9. **Step 9:** **拡張D:** 多主体系における臨界次元 $D^*$ の探索  

---

## 7. 実装

### 7.1 実験プログラム構造

PKGF_Full_Experiments
│
├── 0. Global Constants / Parameters
│     - DIM = 32
│     - NSECT = 4
│     - SECSZ = 8
│     - dt, T, λ, etc.
│
├── 1. Sector System & Gauge Group
│   ├── sector_projector(α)
│   ├── gauge_generator(preserve_sectors)
│   └── gauge_action(K, H) = H K H^{-1}
│
├── 2. Differential Geometry Core
│   ├── init_connection() → ω
│   ├── curvature(ω) = dω + ω∧ω
│   └── covariant_derivative(K, ω) = ωK − Kω
│
├── 3. PKGF Operators
│   ├── constructive_term(K, Ω) = [Ω, K]
│   ├── destructive_operator(K)  (self-adjoint, negative-definite)
│   ├── unified_operator(K, Ω, λ)
│   └── complex_K = K_core + i K_fluct
│
├── 4. Sixteen Fields Ω^(1..16)
│   ├── semantics
│   ├── context
│   ├── metric
│   ├── transformation
│   ├── desire
│   ├── ethics
│   ├── emotion
│   ├── value
│   ├── learning
│   ├── memory
│   ├── metacognition
│   ├── meta-update
│   ├── self-reference
│   ├── awareness
│   ├── strategy
│   └── social
│
├── 5. PKGF Flows (time integrators)
│   ├── constructive_flow(K, Ω)
│   ├── destructive_flow(K, λ)
│   └── unified_flow(K, Ω, λ)
│
├── 6. Metrics & Observables
│   ├── det(K)
│   ├── Spec(K)
│   ├── sector_mixing(K)
│   ├── entropy(K)
│   ├── effective_rank(K)
│   ├── gauge_breaking_order_parameter Φ_SB(K)
│   └── logical_volume_breathing(K(t))
│
├── 7. Experiments
│   ├── Exp1: Constructive PKGF (P1–P7, Thm 1–7)
│   ├── Exp2: Destructive PKGF (R1–R7, Thm R1–R6)
│   ├── Exp3: Unified PKGF (U1–U7)
│   ├── Exp4: Gauge Symmetry Breaking
│   ├── Exp5: Multi-agent PKGF
│   └── Exp6: 16 Fields Ablation
│
└── 8. main() — 全実験を順番に実行

### 7.2 ログ形式

```
PKGF_LOG_v2:
  experiment_id: <string>
  timestamp: <YYYY-MM-DD HH:MM:SS>
  language: <Python | Fortran>
  dim: 32
  sector_size: 8
  num_sectors: 4
```

---

#### 1. Constructive PKGF（P1–P7）

```
Constructive:
  det_initial: <float>
  det_final: <float>
  sector_mixing_initial: <float>
  sector_mixing_final: <float>
  max_comm_norm: <float>
  steps: <int>
```

---

#### 2. Destructive PKGF（R1–R7）

```
Destructive:
  det_sequence: [float]
  entropy_sequence: [float]
  effective_rank_sequence: [int]
  steps: <int>
```

---

#### 3. Unified PKGF（U1–U7）＋拡張A（文脈依存計量）

```
Unified:
  det_sequence: [float]              # det(K)
  core_det_sequence: [float]         # det(Re(K))
  fluct_norm_sequence: [float]       # ||Im(K)||
  lambda_sequence: [float]
  order_parameter_sequence: [float]  # Φ_SB(t)
  metric_scaling_sequence: [float]   # η(x) or g-scaling (拡張A)
  steps: <int>
```

---

#### 4. Gauge Symmetry Breaking（U3）＋拡張C（安定化群）

```
GaugeBreaking:
  order_parameter_initial: <float>
  order_parameter_final: <float>
  critical_step: <int>
  stabilizer_dim_sequence: [float]   # dim G_broken(t)
  steps: <int>
```

---

#### 5. Multi-agent PKGF（定理5–7）＋拡張D（臨界次元探索）

```
MultiAgent:
  num_agents: <int>
  dimension: <int>                   # D
  social_energy_sequence: [float]
  agent_comm_norms:
    agent_1: [float]
    agent_2: [float]
    ...
  critical_dimension_detected: <bool>
  critical_dimension_value: <int or null>
  steps: <int>
```

---

#### 6. Sixteen Fields Ablation（16フィールド寄与）

```
Fields:
  field_contributions:
    semantics: <float>
    context: <float>
    metric: <float>
    transformation: <float>
    desire: <float>
    ethics: <float>
    emotion: <float>
    value: <float>
    learning: <float>
    memory: <float>
    metacognition: <float>
    meta_update: <float>
    self_reference: <float>
    awareness: <float>
    strategy: <float>
    social: <float>
```

---

#### 7. 拡張B: TDA（Persistent Homology）

```
TDA:
  betti_0_sequence: [int]
  betti_1_sequence: [int]
  betti_2_sequence: [int]
  tda_critical_step: <int or null>
  barcode_snapshots: <optional>
```

---

#### 8. Metadata

```
Metadata:
  random_seed: <int>
  machine: <string>
  compiler_or_interpreter: <string>
```

---
