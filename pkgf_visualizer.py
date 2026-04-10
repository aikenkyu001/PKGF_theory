#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import ListedColormap

def load_log(filename="pkgf_log_python.json"):
    with open(filename, "r") as f:
        return json.load(f)["PKGF_LOG"]

def plot_destructive_flow(log):
    """図 1: 解体フロー（定理 R1, R2, R4）"""
    data = log["Destructive"]
    steps = range(len(data["det_sequence"]))
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:red'
    ax1.set_xlabel('Steps (Time)')
    ax1.set_ylabel('Log Determinant (det K)', color=color)
    ax1.plot(steps, np.log10(np.array(data["det_sequence"]) + 1e-100), color=color, label="det K")
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Effective Rank / Entropy', color=color)
    ax2.plot(steps, data["effective_rank_sequence"], '--', color=color, label="Effective Rank")
    ax2.plot(steps, data["entropy_sequence"], ':', color='tab:green', label="Entropy S[Phi]")
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title("Fig 1: Destructive Flow - Rank Decay and Entropy Increase")
    fig.tight_layout()
    plt.savefig("pkgf_fig1_destructive.png")
    print("Saved: pkgf_fig1_destructive.png")

def plot_unified_breathing(log):
    """図 2: 呼吸する論理体積（定理 U5）"""
    data = log["Unified"]
    steps = range(len(data["det_sequence"]))
    
    plt.figure(figsize=(10, 5))
    plt.plot(steps, data["core_det_sequence"], label="$\det(K_{core})$ (Logical Volume)", color='blue')
    plt.fill_between(steps, 0, data["fluct_norm_sequence"], alpha=0.2, color='red', label="Fluctuation Norm ($||K_{fluct}||$)")
    
    plt.title("Fig 2: Breathing Logical Volume (Metabolic Cycle)")
    plt.xlabel("Steps")
    plt.ylabel("Volume / Norm")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("pkgf_fig2_breathing.png")
    print("Saved: pkgf_fig2_breathing.png")

def plot_phase_diagram(log):
    """図 3: PKGF 相図 (Phase Diagram)"""
    data = log["PhaseDiagram"]
    matrix = np.array(data["phase_matrix"])
    
    plt.figure(figsize=(8, 7))
    # 0: Constructive (Blue), 1: Metabolic (Green), 2: Destructive (Red)
    cmap = ListedColormap(['#d0f0ff', '#e8ffe0', '#ffe0e0'])
    
    sns.heatmap(matrix, annot=True, cmap=cmap, cbar=False,
                xticklabels=[f"{x:.1f}" for x in data["omega_scale_range"]],
                yticklabels=[f"{x:.2f}" for x in data["lambda_range"]])
    
    plt.title("Fig 3: PKGF Phase Diagram ($\lambda$ - A Plane)")
    plt.xlabel("Internal Tension / Omega Scale (A)")
    plt.ylabel("Dissipation Intensity ($\lambda$)")
    
    # Legend manually
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#d0f0ff', label='Constructive (Stable)'),
        Patch(facecolor='#e8ffe0', label='Metabolic (Breathing)'),
        Patch(facecolor='#ffe0e0', label='Destructive (Collapse)')
    ]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.3, 1))
    
    plt.tight_layout()
    plt.savefig("pkgf_fig3_phase_diagram.png")
    print("Saved: pkgf_fig3_phase_diagram.png")

def plot_tda_transition(log):
    """図 4: TDA とトポロジカル相転移（定理 U6）"""
    data = log["TDA"]
    steps = range(len(data["betti_1_sequence"]))
    
    plt.figure(figsize=(10, 5))
    plt.step(steps, data["betti_1_sequence"], where='post', label="Betti 1 ($b_1$): Topological Holes", color='purple')
    plt.step(steps, data["betti_2_sequence"], where='post', label="Betti 2 ($b_2$): Voids", color='cyan')
    
    if data["tda_critical_step"] is not None:
        plt.axvline(x=data["tda_critical_step"], color='red', linestyle='--', label="Dimension Jump (Critical Step)")
    
    plt.title("Fig 4: Topological Phase Transition (Dimension Jump)")
    plt.xlabel("Steps")
    plt.ylabel("Betti Numbers")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig("pkgf_fig4_tda.png")
    print("Saved: pkgf_fig4_tda.png")

def plot_multiagent_critical(log):
    """図 5: マルチエージェント臨界次元（定理 6）"""
    data = log["MultiAgent"]
    d_range = data["d_range"]
    # 各 D における最終ステップのエネルギーを抽出
    final_energies = [seq[-1] for seq in data["social_resonance_energy_sequence"]]
    
    plt.figure(figsize=(10, 5))
    plt.plot(d_range, final_energies, 'o-', color='black', linewidth=2)
    
    if data["critical_dimension_value"] is not None:
        plt.axvline(x=data["critical_dimension_value"], color='blue', linestyle=':', label=f"Detected $D^*$ = {data['critical_dimension_value']}")
    
    plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label="Stability Threshold")
    
    plt.title(f"Fig 5: Multi-Agent Critical Dimension (n_agents = {data['num_agents']})")
    plt.xlabel("Dimension D")
    plt.ylabel("Final Social Resonance Energy ($||[K, F]||$)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("pkgf_fig5_critical_D.png")
    print("Saved: pkgf_fig5_critical_D.png")

def generate_fields_table(log):
    """表 1: 16フィールド寄与度要約"""
    data = log["Fields"]
    df = pd.DataFrame(data).T
    df.index.name = "Field"
    df = df.sort_values(by="final_rank", ascending=False)
    
    print("\n--- Table 1: Sixteen Fields Ablation Analysis ---")
    print(df.to_markdown())
    df.to_csv("pkgf_table1_fields.csv")
    print("\nSaved: pkgf_table1_fields.csv")

def main():
    try:
        log = load_log()
        sns.set_theme(style="whitegrid")
        
        plot_destructive_flow(log)
        plot_unified_breathing(log)
        plot_phase_diagram(log)
        plot_tda_transition(log)
        plot_multiagent_critical(log)
        generate_fields_table(log)
        
        print("\nAll figures and tables generated successfully.")
    except Exception as e:
        print(f"Error during visualization: {e}")

if __name__ == "__main__":
    main()
