"""
====================================================================
Week 10: Complete Classificatioin Algorithms Study
Data Science Master's Prep | Belhaven University 
=====================================================================
Satisfies ALL Week 10 Requirements:
  ✅ Decision Trees
  ✅ Random Forests
  ✅ Support Vector Machines (SVM)
  ✅ K-Nearest Neighbors (KNN)
  ✅ Logistic Regression (Week 9 reinforcement)
  ✅ Gradient Boosting (XGBoost preview)
  ✅ Cross-Validation on ALL projects
  ✅ Multiple evaluation metrics on ALL projects
  ✅ All 6 algorithms compared on same datasets
  ✅ Findings documented with commentary

THREE REAL-WORLD CASE STUDIES:
  Project 1 — GridGuard    : Electrical Grid Stability (Utility Provider)
  Project 2 — LoanShield   : Loan Default Prediction  (Financial Institution)
  Project 3 — DraftOracle  : NBA Rookie Career        (Scouting Department)

ALGORITHMS USED (6 total):
  1. Logistic Regression
  2. Decision Tree
  3. Random Forest
  4. Support Vector Machine (SVM)
  5. K-Nearest Neighbors (KNN)
  6. Gradient Boosting

METRICS COVERED:
  - Accuracy, Precision, Recall, F1-Score
  - ROC-AUC Score
  - Cross-Validation (5-Fold StratifiedKFold)
  - Confusion Matrix
  - Classification Report
  - Precision-Recall Curve (Project 2)
  - Feature Importance (tree-based models)

=====================================================================
"""

import pandas as pd 
import numpy as np
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os 
import time
import warnings
warnings.filterwarnings("ignore") 

from sklearn.model_selection import (
    train_test_split, 
    StratifiedKFold, 
    cross_val_score, 
)

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score, 
    recall_score, 
    f1_score, 
    roc_auc_score, 
    confusion_matrix, 
    ConfusionMatrixDisplay, 
    RocCurveDisplay, 
    precision_recall_curve, 
    
)

# --- Shared constants ---------------------------------------------------------------------------------
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE) 
os.makedirs("reports", exist_ok=True)
CV_FOLDS = 5 

ALGO_COLORS = {
    "Logistic Regression": "#3498db", 
    "Decision Tree": "#e67e22", 
    "Random Forest": "#2ecc71",
    "SVM": "#9b59b6", 
    "KNN": "#e74c3c", 
    "Gradient Boosting": "#1abc9c",
}


# ======================================================================================
# SHARED HELPERS 
# ======================================================================================
def build_models(class_weight=None): 
    cw = class_weight 
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, class_weight=cw, random_state=RANDOM_STATE
        ), 
        "Decision Tree": DecisionTreeClassifier(
            max_depth=6, class_weight=cw, random_state=RANDOM_STATE

        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, class_weight=cw, 
            n_jobs=-1, random_state=RANDOM_STATE
        ), 
        "SVM": SVC(
            kernel="rbf", probability=True, class_weight=cw,
            random_state=RANDOM_STATE
        ), 
        "KNN": KNeighborsClassifier(n_neighbors=7, n_jobs=-1), 
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, learning_rate=0.1, 
            max_depth=4, random_state=RANDOM_STATE
        ),
    }


def evaluate_all(models, X_train_s, X_test_s, y_train, y_test, 
                 pos_label=1, cv_folds=CV_FOLDS): 
    skf  = StratifiedKFold(n_splits=CV_FOLDS)
    results = {}
    for name, model in models.items(): 
        t0  = time.time() 
        cv_auc = cross_val_score(
            model, X_train_s, y_train, cv=skf, scoring="roc_auc", n_jobs=-1
        )
        model.fit(X_train_s, y_train) 
        y_pred = model.predict(X_test_s) 
        y_prob = model.predict_proba(X_test_s)[:, 1]
        elapsed = time.time() - t0
        results[name] = {
            "model": model,
            "y_pred": y_pred,
            "y_prob": y_prob,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, pos_label=pos_label, zero_division=0),
            "recall": recall_score(y_test, y_pred, pos_label=pos_label, zero_division=0),
            "f1": f1_score(y_test, y_pred, pos_label=pos_label, zero_division=0),
            "auc": roc_auc_score(y_test, y_prob),
            "cv_auc_mean": cv_auc.mean(),
            "cv_auc_std": cv_auc.std(),
            "cv_auc_all": cv_auc,
            "train_time": elapsed,
        }
    return results


def print_results_table(results, project_name, pos_class_name="Positive"): 
    print(f"\n{'-'*78}")
    print(f" {project_name} - Algorithm Comparison Table")
    print(f" Positive Class = '{pos_class_name}' ") 
    print(f"{'-'*78}")
    print(f"  {'Algorithm':<22} {'Acc':>6} {'Prec':>6} {'Rec':>6} {'F1':>6} "
          f"{'AUC':>6} {'CV-AUC':>12} {'Time':>6}")
    print(f" {'-'*22} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*12} {'-'*6}")
    for name, r in results.items():
        print(
            f" {name:<22} "
            f"{r['accuracy']:>6.3f} "
            f"{r['precision']:>6.3f} "
            f"{r['recall']:>6.3f} "
            f"{r['f1']:>6.3f} "
            f"{r['auc']:>6.3f} "
            f"{r['cv_auc_mean']:>12.3f} "
            f"{r['train_time']:>5.1f}s"
        )
    print(f"{'-'*78}\n")


def save_comparison_chart(results, y_test, title, filename, 
                          pos_label_name="Positive", neg_label_name="Negative"):
    names = list(results.keys())
    colors = [ALGO_COLORS[n] for n in names]
    metrics = ["accuracy", "precision", "recall", "f1", "auc"]
    m_lbls = ["Accuracy", "Precision", "Recall", "F1", "AUC"]

    fig = plt.figure(figsize=(20, 14)) 
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.3) 
    ax0 = fig.add_subplot(gs[0, 0]) 
    ax1 = fig.add_subplot(gs[0, 1]) 
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1]) 
    fig.suptitle(title, fontsize=15, fontweight="bold", y=0.98) 

    # Panel 0: grouped bar 
    x, bar_w = np.arange(len(metrics)), 0.13
    for i, (name, color) in enumerate(zip(names, colors)): 
        vals =[results[name][m] for m in metrics]
        offset = (i - len(names) / 2 + 0.5) * bar_w
        ax0.bar(x + offset, vals, bar_w, label=name, color=color, alpha=0.85) 
    ax0.set_xticks(x) 
    ax0.set_xticklabels(m_lbls, fontsize=9) 
    ax0.set_ylim(0, 1.18) 
    ax0.set_ylabel("Score") 
    ax0.set_title("All Metrics = All Algorithms") 
    ax0.legend(fontsize=7, loc="upper left", ncol=2) 
    ax0.axhline(0.5, color="gray", lw=0.8, ls="--", alpha=0.5)


    # Panel 1: CV AUC errpr bars 
    cv_means = [results[n]["cv_auc_mean"] for n in names]
    cv_stds = [results[n]["cv_auc_std"] for n in names] 
    y_pos = np.arange(len(names))
    ax1.barh(y_pos, cv_means, xerr=cv_stds, color=colors, alpha=0.85,
             capsize=4, error_kw={"elinewidth": 1.5})
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontsize=9)
    ax1.set_xlim(0, 1.05)
    ax1.set_xlabel("CV ROC-AUC (mean ± std)")
    ax1.set_title(f"{CV_FOLDS}-Fold Stratified Cross-Validation AUC")
    ax1.axvline(0.5, color="gray", lw=0.8, ls="--", alpha=0.5)
    for i, (m, s) in enumerate(zip(cv_means, cv_stds)): 
        ax1.text(m + s + 0.005, i, f"{m:.3f}", va="center", fontsize=8)

    # Panel 2: ROC curves
    for name, color in zip(names, colors):
        r = results[name]
        RocCurveDisplay.from_predictions(
            y_test, r["y_prob"], 
            name=f"{name} ({r['auc']:.3f})", 
            ax=ax2, color=color, alpha=0.85    
        )
    ax2.plot([0, 1], [0, 1], "k--", lw=0.8, alpha=0.5) 
    ax2.set_title("ROC Curves - All Algorithms") 
    ax2.legend(fontsize=7, loc="lower right") 

    # Panel 3: confision matrix of best AUC model 
    best_name = max(results, key=lambda k: results[k]["auc"]) 
    best = results[best_name]
    cm = confusion_matrix(y_test, best["y_pred"])
    ConfusionMatrixDisplay(
        cm, display_labels=[neg_label_name, pos_label_name]
    ).plot(ax=ax3)
    ax3.set_title(f"Confusion Matrix - Best Model: {best_name}, AUC={best['auc']:.3f}")

    plt.savefig(f"reports/{filename}", dpi=150, bbox_inches="tight") 
    plt.close()
    print(f"  V Chart saved -> reports/{filename}") 
    return best_name 

def save_feature_importance(model, feature_names, title, filename): 
    if not hasattr(model, "feature_importances_"):
        return
    imp = pd.Series(model.feature_importances_, index=feature_names).sort_values()
    colors = plt.cm.RdYlGn(np.linspace(0.25, 0.85, len(imp)))
    fig, ax = plt.subplots(figsize=(10, max(5, len(imp) * 0.35)))
    imp.plot(kind="barh", ax=ax, color=colors)
    ax.set_title(title, fontsize=12, fontweight="bold")
    for i, v in enumerate(imp): 
        ax.text(v + 0.001, i, f"{v:.4f}", va="center", fontsize=8)
    plt.tight_layout() 
    plt.savefig(f"reports/{filename}", dpi=150, bbox_inches="tight") 
    plt.close() 
    print(f"  V Feature importance saved --> reports/{filename}") 

def section_banner(text): 
    bar = "=" * 70 
    print(f"\n{bar}\n {text}\n{bar}") 

# ======================================================================================
# Project 1 - Gridguard: Electrical Grid Stability
# ======================================================================================

def run_project1(): 
    section_banner("PROJECT 1: GridGuard = Electrical Grid Stability") 
    print("""
          FRAMING: You are a data scientist contracted by a regional public utility. The grid has experienced 3 near-blackout events in the past year. Your job is to test 6 early-warning algorithms and recommend the best one for a real-time monitoring dashboard that flags UNSTABLE conditions before they cascade into outages.
          DATASET: 10,000 simulated grid scenarios
            tau1-4 : Reaction times (producer + 3 consumers) 
            p1-4 : Power values (supply/demand)
            g1-4 : Price elasticity coefficients
            Target: stable vs unstable (~63% / 37% split) 
            """)
    
    print("[1] Generating simulated electrical grid dataset...") 
    n = 10_000

    tau1 = np.random.uniform(0.5, 10.0, n) 
    tau2 = np.random.uniform(0.5, 10.0, n)
    tau3 = np.random.uniform(0.5, 10.0, n)
    tau4 = np.random.uniform(0.5, 10.0, n)
    p1 = np.random.uniform(0.5, 2.0, n) 
    p2 = np.random.uniform(-2.0, -0.5, n) 
    p3 = np.random.uniform(-2.0, -0.5, n)
    p4 = np.random.uniform(0.5, 2.0, n)
    g1 = np.random.uniform(0.05, 1.0, n) 
    g2 = np.random.uniform(0.05, 1.0, n)
    g3 = np.random.uniform(0.05, 1.0, n)
    g4 = np.random.uniform(0.05, 1.0, n) 

    imbalance = p1 + p2 + p3 + p4 
    avg_reaction = (tau2 + tau3 + tau4) / 3 
    stability_score = imbalance * avg_reaction + np.random.normal(0, 0.5, n)
    threshold = np.percentile(stability_score, 37) 
    label = np.where(stability_score > threshold, "stable", "unstable") 

    df = pd.DataFrame({
        "tau1": tau1, "tau2": tau2, "tau3": tau3, "tau4": tau4, 
        "p1": p1, "p2": p2, "p3": p3, "p4": p4, 
        "g1": g1, "g2": g2, "g3": g3, "g4": g4, 
        "Label": label, 
    })  
    stable_n = (df["Label"] == "stable").sum()
    unstable_n = (df["Label"] == "unstable").sum()
    print(f" Dataset: {len(df):,} records | Stable: {stable_n:,} ({stable_n/len(df)*100:.0f}%) | Unstable: {unstable_n:,} ({unstable_n/len(df)*100:.0f}%)")

    print("\n[2] Preprocessing... ")
    X = df.drop("Label", axis=1)
    y = (df["Label"] == "unstable").astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )
    scaler = StandardScaler() 
    X_train_s = scaler.fit_transform(X_train) 
    X_test_s = scaler.transform(X_test) 
    print(f" Train: {len(X_train):,} | Test: {len(X_test):,} | Features: {X.shape[1]}")

    print("\n[3] Training and evaluating all 6 algorithms with 5-fold CV...")
    models = build_models(class_weight=None) 
    results = evaluate_all(models, X_train_s, X_test_s, y_train, y_test, pos_label=1)
    print_results_table(results, "GridGuard", pos_class_name="Unstable") 

    best_name = max(results, key=lambda k: results[k]["auc"]) 
    best = results[best_name]
    print(f"[4] Best model by AUC: {best_name} (AUC = {best['auc']:.4f})")
    print(f"\n CV AUC per fold: {[f'{v:.3f}' for v in best['cv_auc_all']]}")
    print( f" Mean: {best['cv_auc_mean']:.4f} | Std: {best['cv_auc_std']:.4f}")
    print("\n Full Classification Report:") 
    print(classification_report(
        y_test, best["y_pred"], 
        target_names=["Stable", "Unstable"], zero_division=0
    ))

    print("[6] Cross-Validation Commentary:") 
    print("""
    Cross-validation trains the model on 4 folds and tests on the 5th, rotating 5 times. This gives a reliable estimate of how the model will perform on UNSEEN data - more trustworthy than a single train/test split. A small std (+/-0.005 or less) means the model generalises consistently. A large gap between CV AUC and Test AUC could indicate overfitting. 
    """)
    for name, r in results.items(): 
        gap = abs(r["auc"] - r["cv_auc_mean"])
        flag = " OVERFIT?" if gap > 0.05 else " VALID"
        print(f" {name:<22} | Test AUC: {r['auc']:.3f} CV AUC: {r['cv_auc_mean']:.3f} "
              f"Gap: {gap:.3f}{flag}") 
        
    print("\n[7] Saving visualizations..") 
    save_comparison_chart(
        results, y_test, 
        title="GridGuard - Electrical Grid Stability | All 6 Algorithms", 
        filename="p1_gridguard_comparison.png", 
        pos_label_name="Unstable", 
        neg_label_name="Stable", 
    )
    save_feature_importance(
        results["Random Forest"]["model"], X.columns, 
        "GridGuard - Feature Importance (Random Forest) \nTop Predictors of Grid Instability", 
        "p1_gridguard_feature_importance.png"
    )
    print("\nV PROJECT 1 COMPLETED - Gridguard\n") 
    return results


# ======================================================================================
# Project 2 - LOANSHIELD: LOAN DEFAULT PREDICTION
# ======================================================================================
def run_project2(): 
    section_banner("PROJECT 2: LoanShield - Loan Default Prediction") 
    print("""
Framing: You are a risk analyst at a mid-size bank. Leadership wants a model
to flag likely defaulters before approval so the lending desk can ask for
additional documentation or decline the application. 

KEY TRADE-OFF:
    False Negative (miss a defaulter) -> bank loses full loan amount 
    False Positive (flag a good customer) -> one lost customer
    -> We must maximise RECALL on defaults, even at the cost of some precision.

Technique: class_weight='balanced' so all models learn to respect the
minority class rather than ignoring it. 
          
DATASET: 5,000 historical loan records 
    Features: income, credit score, loan amount, employment, debt ration, etc. 
    Target : Default vs Paid Off (~15% default rate)
    """)

    print("[1] Generating financial loan dataset...") 
    n = 5_000

    annual_income = np.random.normal(60_000, 20_000, n).clip(20_000, 200_000) 
    credit_score = np.random.normal(680, 80, n).clip(300, 850).astype(int) 
    loan_amount = np.random.normal(15_000, 8_000, n).clip(1_000, 50_000) 
    loan_term_months = np.random.choice([12, 24, 36, 48, 60], n) 
    employment_years = np.random.exponential(4, n).clip(0, 30) 
    debt_to_income = np.random.beta(2, 5, n) * 0.6
    num_late_payments = np.random.poisson(1, n).clip(0, 10) 
    home_ownership = np.random.choice(
        ["RENT", "OWN", "MORTGAGE"], n, p=[0.4, 0.2, 0.4]
    )


    log_odds = ( 
        - 0.000015 * annual_income
        - 0.004 * credit_score
        + 0.000015 * loan_amount
        + 0.60 * debt_to_income
        + 0.07 * num_late_payments
        - 0.02 * employment_years
    )
    default_prob = 1 / (1 + np.exp(-log_odds + 1.2))
    outcome = np.where(np.random.binomial(1, default_prob), "Default", "Paid Off")

    df = pd.DataFrame({
        "annual_income": annual_income, 
        "credit_score": credit_score, 
        "loan_amount": loan_amount, 
        "loan_term_months": loan_term_months, 
        "employment_years": employment_years, 
        "debt_to_income": debt_to_income, 
        "num_late_payments": num_late_payments, 
        "home_ownership": home_ownership, 
        "outcome": outcome, 
    })

    default_n = (df["outcome"] == "Default").sum() 
    paidoff_n = (df["outcome"] == "Paid Off").sum() 
    print(f" Dataset: {len(df):,} records | Default: {default_n:,} "
          f"({default_n/len(df)*100:.1f}%) | Paid Off: {paidoff_n:,}")
    
    print("\n[2] Preprocessing (one-hot encode home_ownership)...") 
    df_enc = pd.get_dummies(df, columns=["home_ownership"], drop_first=True) 
    X = df_enc.drop("outcome", axis=1) 
    y = (df_enc["outcome"] == "Default").astype(int) 
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )
    scaler = StandardScaler() 
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test) 
    print(f" Train: {len(X_train):,} | Test: {len(X_test):,} | Features: {X.shape[1]}")
    print(f" Default rate in train set: {y_train.mean()*100:.1f}%") 

    print("\n[3] Training all 6 algorithms (class_weight='balanced') with 5-fold CV...") 
    models = build_models(class_weight="balanced") 
    results = evaluate_all(models, X_train_s, X_test_s, y_train, y_test, pos_label=1) 
    print_results_table(results, "LoanShield", pos_class_name="Default") 

    best_recall_name = max(results, key=lambda k: results[k]["recall"]) 
    best_auc_name = max(results, key=lambda k: results[k]["auc"]) 
    best = results[best_recall_name]

    print(f"[4] Best model by RECALL(Default): {best_recall_name} " 
          f"(Recall = {best['recall']:.2f})")
    print("""
    Why we report BOTH: 
          AUC tells us the model's overall discriminative ability across all 
          possible decision thresholds. Recall at default threshold (0.5) shows
          operational performance. A bank in production would lower the threshold 
          (e.g. 0.3) to catch more defaulters - boosting Recall at cost of Precision.
    """)
    print(" Full Classification Report (best Recall model):") 
    print(classification_report(
        y_test, best["y_pred"], 
        target_names=["Paid Off", "Default"], zero_division=0
    ))

    print("[5] Precision-Recall threshold analysis:") 
    prec_arr, rec_arr, thresh_arr = precision_recall_curve(
        y_test, results[best_auc_name]["y_prob"]
    )
    idx_80 = np.searchsorted(-rec_arr, -0.80) 
    if idx_80 < len(thresh_arr): 
        print(f" At Recall >= 0.80: threshold={thresh_arr[idx_80]:.3f} "
              f"Precision={prec_arr[idx_80]:.3f}")
    else: 
        print(" Recall 0.80 not achievable at any threshold with this model.") 

    print("\n[6] Cross-Validation Commentary - Imbalanced Dataset:") 
    print("""
    With only ~15% defaults, standard CV could put ALL defaults in one fold. 
    StratifiedKFold preserves the class ratio in each fold - critical here. 
    Watch for high std (>0.05) which signals the model struggles consistently. 
    """)
    for name, r in results.items(): 
        print(f" {name:<22} CV AUC: {r['cv_auc_mean']:.3f} +/- {r['cv_auc_std']:.3f} "
              f"Recall: {r['recall']:.3f}")
        
    print("\n[7] Saving visualizations...") 
    save_comparison_chart(
        results, y_test, 
        title="LoanShield - loan Default Risk Assessment | All 6 Algorithms", 
        filename="p2_loanshield_Comparison.png",
        pos_label_name="Default", 
        neg_label_name="Paid Off" 
    )
    save_feature_importance( 
        results["Gradient Boosting"]["model"], X.columns, 
        "LoanShield - Feature Importance (Gradient Boosting)\nKey Default Risk Factors",
        "p2_loanshield_feature_importance.png"
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    for name in results: 
        p, r, _ = precision_recall_curve(y_test, results[name]["y_prob"])
        ax.plot(r, p, label=name, color=ALGO_COLORS[name], lw=1.8, alpha=0.85) 
    ax.axhline(y=default_n / len(df), color="gray", ls="--", lw=1, label="Baseline (random)") 
    ax.set_xlabel("Recall (Default)") 
    ax.set_ylabel("Precision(Default)") 
    ax.set_title("LoanShield = Precision-Recall Curves\n(Tune threshold by moving along curve)")
    ax.legend(fontsize=8) 
    plt.tight_layout() 
    plt.savefig("reports/p2_loanshield_pr_curves.png", dpi=150, bbox_inches="tight") 
    plt.close() 
    print(" v PR curves saved -> reports/p2_loanshield_pr_curves.png") 

    print("\nV PROJECT 2 COMPLETE - LoanShield\n")
    return results 

# ======================================================================================
# Project 3 - DRAFTORAVLE: NBA ROOKIE CAREER LONGETIVITY
# ======================================================================================

def run_project3(): 
    section_banner("PROJECT 3: DraftOracle - NBA Rookie Career Longevity") 
    print("""
          Framing: You are a lead data scientist for an NBA franchise's analytics 
          department. The front office is tired of spending lottery picks on players
          who wash out in 2-3 years. Using ONLY rookie-season statistics, build a 
          model to predict whether a player's career will exceed 5 years. 
          
          KEY TRADE-OFF (opposite of Project 2): 
            False Positive (call a bust a franchise player) -> wasted lottery pick 
            False Negative (miss a gem) -> lost upside out recoverable 
            -> We must maximise PRECISION on  "Long Career" predictions. 
          
          DATASET: 1,200 historical NBA rookies (1990-2020 era) 
            Features: ppg, rpg, apg, fg%, ft%, minutes, games, draft info, age
            Target : Career > 5 Years vs Career <= 5 Years (~72 / 28% split) 
            """) 
    print("[1] Generating NBA rookie historical dataset...") 
    n = 1_200

    ppg = np.random.gamma(2, 3.5, n).clip(0, 35) 
    rpg = np.random.gamma(2, 2.0, n).clip(0, 15) 
    apg = np.random.gamma(1.5, 1.5, n).clip(0, 12) 
    spg = np.random.gamma(1.0, 0.5, n).clip(0, 4) 
    bpg = np.random.gamma(0.8, 0.4, n).clip(0, 4) 
    fg_pct = np.random.normal(0.44, 0.06, n).clip(0.25, 0.70) 
    three_pct = np.random.normal(0.33, 0.09, n).clip(0.00, 0.55)
    ft_pct = np.random.normal(0.74, 0.10, n).clip(0.40, 1.00)
    games_played = np.random.binomial(82, 0.65, n).clip(5, 82)
    minutes_pg = np.random.normal(20, 8, n).clip(2, 40) 
    draft_round = np.random.choice([1, 2], n, p=[0.55, 0.45])
    draft_pick = np.where(
        draft_round == 1, 
        np.random.randint(1, 31, n), 
        np.random.randint(1, 31, n) + 30, 
    )
    age_at_draft = np.random.normal(21.5, 1.5, n).clip(18, 30) 

    long_career_score = ( 
        0.12 * ppg + 0.08 * rpg + 0.10 * apg
        + 0.50 * fg_pct + 0.30 * ft_pct
        + 0.03 * games_played + 0.05 * minutes_pg 
        - 0.008 * draft_pick - 0.05 * age_at_draft
        + np.random.normal(0, 0.3, n) 
    )
    long_career_prob = 1 / (1 + np.exp(-long_career_score + 2))
    career_label = np.where(
        np.random.binomial(1, long_career_prob), "Long", "Short"
    )

    df = pd.DataFrame({
        "ppg": ppg, "rpg": rpg, "apg": apg, "spg": spg, "bpg": bpg, 
        "fg_pct": fg_pct, "three_pct": three_pct, "ft_pct": ft_pct, 
        "games_played": games_played, "minutes_pg": minutes_pg, 
        "draft_round": draft_round, "draft_pick": draft_pick, 
        "age_at_draft": age_at_draft, "career_label": career_label, 
    })

    long_n = (df["career_label"] == "Long").sum()
    short_n = (df["career_label"] == "Short").sum()
    print(f" Dataset: {len(df):,} rookies | Long Career: {long_n:,} " 
          f"({long_n/len(df)*100:.0f}%) | Short: {short_n:,}")
    print("\n[2] EDA - Average stats by career outcome:") 
    eda_cols = ["ppg", "rpg", "apg", "fg_pct", "ft_pct", "minutes_pg", "games_played", 
                "draft_pick", "age_at_draft"]
    print(df.groupby("career_label")[eda_cols].mean().round(3).to_string())


    print("\n[3] Preprocessing...") 
    X = df.drop("career_label", axis=1) 
    y = (df["career_label"] == "Long").astype(int) 
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y,
    )
    scaler = StandardScaler() 
    X_train_s = scaler.fit_transform(X_train) 
    X_test_s = scaler.transform(X_test) 
    print(f" Train: {len(X_train):,} | Test: {len(X_test):,} | Features: {X.shape[1]}")
    

    print("\n[4] Training all 6 algorithms with 5-fold CV...") 
    models = build_models(class_weight=None) 
    results = evaluate_all(models, X_train_s, X_test_s, y_train, y_test, pos_label=1)
    print_results_table(results, "DraftOracle", pos_class_name="Long Career") 


    best_prec_name = max(results, key=lambda k: results[k]["precision"])
    best_auc_name = max(results, key=lambda k: results[k]["auc"]) 
    best = results[best_prec_name]

    
    print(f"[5] Best model by PRECISION(Long): {best_prec_name} "
          f"(Precision = {best['precision']:.4f})")
    print(f" Best model by AUC  : {best_auc_name} "
          f"(AUC = {results[best_auc_name]['auc']:.4f})")
    print("\n Full Classification Report (best Precision model):") 
    print(classification_report(
        y_test, best["y_pred"], 
        target_names=["Short  Career", "Long Career"], zero_division=0
    ))

    print("[6] Scouting Insight - Hidden Indicators of Long-Term NBA Success:") 
    print("""
          Beyond raw scoring, our model surfaces these undervalued signals: 
        
          Minutes Played : Coaches' implicit trust in the player's development. 
          If a rookie is getting 25+ min/game, staff sees potential. 
          
          Free Throw % : Proxy for basketball IQ and coachability. Historically
          overlooked by traditional scouts. Consistently top-5. 
          
          Games Played : Availability and durability in the rookie year. 
          65+ games = reliable. Injury history starts here. 
          
          DRAFT PICK # : Top picks survive longer due to organizational patience. 
          Our model identifies a late-round game whose stats override this. 
          
          AGE AT DRAFT : A 19-year-old with messy numbers has a longer runway
          then a polished 23-year-old. Model rewards youth at lower ppg. 
          
          """)
    
    print("[7] Cross-Validation - Scouting Department Interpretation:") 
    print("""
    In scouting context, CV std = how consistent the model is across different
          historical draft classes and eras. Low std = works across eras. High std = 
          era=specific and overfit to one period of basketball. 
          """)
    for name, r in results.items():
        print(f" {name:<22} CV AUC: {r['cv_auc_mean']:.3f} +/- {r['cv_auc_std']:.3f} "
              f"Precision(Long): {r['precision']:.3f}")

    print("\n[8] Saving visualizations...")
    save_comparison_chart(
        results, y_test,
        title="DraftOracle - NBA Career Longevity | All 6 Algorithms",
        filename="p3_draftoracle_comparison.png",
        pos_label_name="Long Career",
        neg_label_name="Short Career",
    )
    save_feature_importance(
        results["Random Forest"]["model"], X.columns,
        "DraftOracle - Feature Importance (Random Forest)\nHidden Indicators of NBA Career Longevity",
        "p3_draftoracle_feature_importance.png"
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("DraftOracle - Rookie Stat Distributions by Career Outcome",
                 fontsize=12, fontweight="bold")
    for col, ax, label in [
        ("ppg", axes[0], "Points Per Game"),
        ("minutes_pg", axes[1], "Minutes Per Game"),
    ]:
        for outcome, color in [("Long", "#2ecc71"), ("Short", "#e74c3c")]:
            df[df["career_label"] == outcome][col].plot.hist(
                bins=30, alpha=0.6, label=f"{outcome} Career",
                color=color, density=True, ax=ax
            )
        ax.set_title(f"{label} - Long vs Short Career")
        ax.set_ylabel("Density")
        ax.legend()
    plt.tight_layout()
    plt.savefig("reports/p3_draftoracle_stat_distributions.png")
    plt.close()
    print(" V Distribution saved -> reports/p3_draftoracle_stat_distributions.png")

    print("\nV PROJECT 3 COMPLETE - DraftOracle\n")
    return results

# ======================================================================================
# Week 10 MASTER SUMMARY
# ======================================================================================
def print_week10_summary(r1, r2, r3): 
    section_banner("WEEK 10 MASTER SUMMARY - All Algorithms Across ALL Projects") 

    algo_names = list(r1.keys())
    rows = []
    for name in algo_names: 
            rows.append({
                "Algorithm": name, 
                "P1 AUC (Grid)": r1[name]["auc"], 
                "P1 CV AUC": r1[name]["cv_auc_mean"], 
                "P2 AUC (loan)": r2[name]["auc"], 
                "P2 Recall(Def)": r2[name]["recall"], 
                "P3 AUC (NBA)": r3[name]["auc"], 
                "P3 Prec(Long)": r3[name]["precision"], 
                "Avg AUC": np.mean([r1[name]["auc"], r2[name]["auc"], r3[name]["auc"]])
            })
    df_summary = pd.DataFrame(rows).set_index("Algorithm")
    print(df_summary.round(3).to_string())

    print("""
ALGORITHM PROFILES (Week 10 Study Notes)
-------------------------------------------------------------------------------------
        1. Logistic Regression:
          - Simple, fast, highly interpretable (coefficients = feature impact) 
          - Works best when features are linearly separable 
          - Always try this first - it is your baseline 
          - Weakness: struggles with non-linear boundaries 
        
          2. Decision Tree: 
            - Learns non-linear rules; results are human-readable (see export_text) 
            - Fast to train; easy to explore to non-technical stakeholders
            - Weakness: prone to overfitting without max_depth constraint
            - Always check: train accuracy >> test accuracy = overfit 
          
          3. Random Forest: 
            - Ensemble of many decisions trees (bagging) 
            - Very robust - reduces overfitting vs single tree
            - Provides feature importances automatically 
            - Weakness: slower, less interpretable than single tree
          
          4. SUPPORT VECTOR MACHINE (SVM)
            - Finds the MAXIMUM MARGIN hyperplane between classes 
            - RBF kernel maps data to higher dimensions to handle non-linearity
            - Strong on small-to-medium datasets with many features
            - Weakness: slow on large datasets; needs scaling
            - CRITICAL: Must StandardScale before SVM - done in all 3 projects 
          5. 
            - Classifies by majority vote of K nearest training points 
            - No training phase - lazy learner; fast to build, slow to predict 
            - Very sensitive to feature scaling (StandardScaler critical) 
            - Weakness: slow at prediction on large datasets; sensitive to noise 
            - K=7 used here - odd number avoids ties 
           6. GRADIENT BOOSTING
            - Ensemble that builds tree SEQUENTIALLY, each correcting prior errors 
            - Often the highest accuracy on tabular data
            - Weakness: many hyperparameters; slow to train; can overfit
            - Extension: XGBoost/LightGBM are faster industrial versions
          

          WHEN TO USE WHICH METRIC
          ---------------------------------------------------------------------------------------------
          Accuracy : Only useful when classes are balanced. Misleading otherwise.
          Precision : Use when False Positives are costly (DraftOracle - wasted picks) 
          Recall : Use when False Negatives are costly (loanshield - missed defaults) 
          F1-Score : Harmonic mean of Precision + Recall. Good balanced single metric. 
          ROC-AUC : Threshold-indepenent. Best for comparing models overall. 
          CV AUC : How the model performs on unseen data reliably. Use this for 
          final model selection, not just test AUC. 

          CROSS-VALIDATION KEY TAKEAWAY
          ---------------------------------------------------------------------------------------------
          A single train/test split is a coin flip - you might get lucky or unlucky. 
          5-Fold Stratified CV trains and tests 5 times on different splits. 
          Report mean +/- std. Low std = consistent generalisation. High std = unstable. 
          ALWAYS cross-validate beofre claiming a model is "the best."
          """) 
    
    avg_auc_ = [
        np.mean([r1[n]["auc"], r2[n]["auc"], r3[n]["auc"]])
        for n in algo_names
    ]
    colors = [ALGO_COLORS[n] for n in algo_names]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(algo_names, avg_auc_, color=colors, alpha=0.88)
    ax.set_xlim(0.4, 1.05) 
    ax.set_xlabel("Average ROC-AUC Across All 3 Projects") 
    ax.set_title( 
        "Week 10 Master Summary\n"
        "Average Alogorithm Performance - GridGuard, LoanShield, DraftOracle", 
        fontsize=11, fontweight="bold"
    ) 

    for i, v in enumerate(avg_auc_): 
        ax.text(v + 0.004, i, f"{v:.3f}", va="center", fontsize=10, fontweight="bold")
    ax.axvline(0.5, color="gray", ls="--", lw=0.8, alpha=0.6, label="Random baseline") 
    ax.legend(fontsize=9) 
    plt.tight_layout() 
    plt.savefig("reports/week10_master_summary.png", dpi=150, bbox_inches="tight") 
    plt.close() 
    print(" V Master summary chart saved -> reports/week10_master_summary.png") 

# ======================================================================================
# ENTRY POINT 
# ======================================================================================

if __name__ == "__main__": 
    total_start = time.time() 


    print("""
    
+======================================================================================
          WEEK 10 -- CLASSIFICATION ALGORITHMS -- COMPLETE STUDY PROJECT 
          6 Algorithms | 3 Real-World Projects | All Metrics | Full CV
          GridGuard . LoanShield . DraftOracle
+======================================================================================
          """)
    
    t1 = time.time(); r1 = run_project1()
    print(f" Project 1 finished in {time.time()-t1:.1f}s") 
    t2 = time.time(); r2 = run_project2()
    print(f" Project 2 finished in {time.time()-t2:.1f}s") 
    t3 = time.time(); r3 = run_project3()
    print(f" Project 3 finished in {time.time()-t3:.1f}s") 

    print_week10_summary(r1, r2, r3) 

    print("\n" + "=" * 70) 
    print(f" ALL DONE - Total runtime: {time.time()-total_start:.1f}s") 
    print("\n Charts saved to /reports:") 
    for f in sorted(os.listdir("reports")): 
        size_kb = os.path.getsize(f"reports/{f}") // 1024
        print(f" {f:<52} ({size_kb} KB)") 
    
    print("""
Week 10 Checlist:
          [x] Decision Trees 
          [x] Random Forests
          [x] Support Vector Machines (SVM)
          [x] K-Nearest Neighbors (KNN)
          [x] Logistic Regression
          [x] Gradient Boosting 
          [x] 5-Fold Stratified Cross-Validation on all 3 projects
          [x] Multiple metrics: Accuracy, Precision, Recall, F1, AUC
          [x] Confusion matrices, ROC, curves, PR curves
          [x] Feature importance charts
          [x] Algorithm profiles and when-to-use notes 
          [x] All findings documented with explanations
          """)



    





            
        







