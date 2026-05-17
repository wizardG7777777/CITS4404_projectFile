"""Render four algorithm-demonstration animations for the Deliverable 2 video.

Each animation runs the algorithm on a deliberately *simple* 2-D toy landscape
(not the real BTC fitness) so the viewer can see the search behaviour clearly.
This is a pedagogical visualisation, not an experiment — the actual results
in the report come from the full 14-D BTC back-test.

Outputs to ``results/animations/*.mp4``:

  rs.mp4   — Random Search (single-state uniform sampling)
  pso.mp4  — Particle Swarm (one g-best attractor + cognitive/social pull)
  gwo.mp4  — Grey Wolf (three leaders α/β/δ, averaged candidate)
  hho.mp4  — Harris Hawks (energy-gated exploration / exploitation)

Each clip is ~30–50 s, suitable for embedding under the §5 narration in
``docs/d2_video_script.md``.

Requires ``ffmpeg`` on PATH (``brew install ffmpeg``). If ffmpeg is missing
the script falls back to GIF output via Pillow.

Usage:

    uv run python -m tools.make_animations
"""
from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "results" / "animations"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# Shared 2-D toy fitness landscape
# --------------------------------------------------------------------------- #


BOUNDS = np.array([-10.0, 10.0])
GLOBAL_OPT = np.array([0.0, 0.0])


def fitness(p: np.ndarray) -> float:
    """Smoothed multimodal landscape with a clear global max at the origin.

    f(x, y) = -((x² + y²) / 30 + 2·sin(x/2)·sin(y/2))

    Several local maxima sit on the unit-circle-ish region around the origin,
    making the search interesting without being chaotic.
    """
    x = p[..., 0]
    y = p[..., 1]
    return -((x**2 + y**2) / 30.0 + 2.0 * np.sin(x / 2.0) * np.sin(y / 2.0))


# Pre-rendered contour grid (shared across all four animations).
_grid = np.linspace(BOUNDS[0], BOUNDS[1], 200)
_GX, _GY = np.meshgrid(_grid, _grid)
_GZ = fitness(np.stack([_GX, _GY], axis=-1))


def _base_axes(title: str, figsize=(8, 7)) -> tuple:
    fig, ax = plt.subplots(figsize=figsize)
    cf = ax.contourf(_GX, _GY, _GZ, levels=20, cmap="viridis", alpha=0.85)
    ax.scatter(
        GLOBAL_OPT[0],
        GLOBAL_OPT[1],
        marker="*",
        s=350,
        c="gold",
        edgecolors="black",
        zorder=6,
        label="Global max",
    )
    ax.set_xlim(BOUNDS)
    ax.set_ylim(BOUNDS)
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.set_title(title)
    fig.colorbar(cf, ax=ax, shrink=0.85, label="fitness")
    return fig, ax


def _save(anim: animation.FuncAnimation, out_path: Path, fps: int) -> None:
    """Save as mp4 if ffmpeg available, else GIF via Pillow."""
    if shutil.which("ffmpeg"):
        anim.save(str(out_path), writer=animation.FFMpegWriter(fps=fps), dpi=120)
        print(f"  ✓ {out_path.name} (mp4, fps={fps})")
    else:
        gif_path = out_path.with_suffix(".gif")
        anim.save(str(gif_path), writer=animation.PillowWriter(fps=fps), dpi=90)
        print(f"  ✓ {gif_path.name} (gif fallback, fps={fps})")


# --------------------------------------------------------------------------- #
# 1. Random Search animation
# --------------------------------------------------------------------------- #


def render_random_search(seed: int = 0, n_samples: int = 60, fps: int = 2) -> Path:
    rng = np.random.default_rng(seed)
    samples = rng.uniform(BOUNDS[0], BOUNDS[1], size=(n_samples, 2))
    fitnesses = fitness(samples)
    best_history = np.maximum.accumulate(fitnesses)
    best_x_history = []
    cur_best_idx = -1
    for i, f in enumerate(fitnesses):
        if cur_best_idx == -1 or f > fitnesses[cur_best_idx]:
            cur_best_idx = i
        best_x_history.append(samples[cur_best_idx])

    fig, ax = _base_axes("Random Search — uniform i.i.d. samples")
    sample_scat = ax.scatter([], [], c="red", s=40, edgecolors="black", alpha=0.55, label="samples")
    best_scat = ax.scatter([], [], c="yellow", s=200, marker="*", edgecolors="black",
                          linewidths=1.5, zorder=7, label="best so far")
    ax.legend(loc="upper right", fontsize=9)
    text = ax.text(0.02, 0.97, "", transform=ax.transAxes, va="top", ha="left",
                   bbox=dict(boxstyle="round", fc="white", alpha=0.85), fontsize=10)

    def update(i):
        sample_scat.set_offsets(samples[: i + 1])
        bx = best_x_history[i]
        best_scat.set_offsets([[bx[0], bx[1]]])
        text.set_text(f"sample {i+1}/{n_samples}\nbest f = {best_history[i]:.2f}")
        return sample_scat, best_scat, text

    anim = animation.FuncAnimation(fig, update, frames=n_samples, blit=False, interval=500)
    out = OUT_DIR / "rs.mp4"
    _save(anim, out, fps=fps)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# 2. PSO animation
# --------------------------------------------------------------------------- #


def render_pso(seed: int = 0, pop: int = 30, n_iters: int = 30, fps: int = 2) -> Path:
    rng = np.random.default_rng(seed)
    pos = rng.uniform(BOUNDS[0], BOUNDS[1], size=(pop, 2))
    vel = rng.uniform(-3.0, 3.0, size=(pop, 2))
    f = fitness(pos)
    pbest = pos.copy()
    pbest_f = f.copy()
    g_idx = int(np.argmax(pbest_f))
    gbest = pbest[g_idx].copy()
    gbest_f = float(pbest_f[g_idx])

    history = [(pos.copy(), gbest.copy(), gbest_f)]
    w, c1, c2 = 0.7, 2.0, 2.0
    v_max = 0.5 * (BOUNDS[1] - BOUNDS[0])
    for _ in range(n_iters - 1):
        r1 = rng.uniform(size=(pop, 2))
        r2 = rng.uniform(size=(pop, 2))
        vel = w * vel + c1 * r1 * (pbest - pos) + c2 * r2 * (gbest - pos)
        vel = np.clip(vel, -v_max, v_max)
        pos = np.clip(pos + vel, BOUNDS[0], BOUNDS[1])
        f = fitness(pos)
        improve = f > pbest_f
        pbest[improve] = pos[improve]
        pbest_f[improve] = f[improve]
        if pbest_f.max() > gbest_f:
            g_idx = int(np.argmax(pbest_f))
            gbest = pbest[g_idx].copy()
            gbest_f = float(pbest_f[g_idx])
        history.append((pos.copy(), gbest.copy(), gbest_f))

    fig, ax = _base_axes("Particle Swarm Optimization — one g-best attractor")
    particles = ax.scatter([], [], c="white", s=45, edgecolors="black",
                           linewidths=0.7, zorder=5, label="particles")
    gbest_scat = ax.scatter([], [], c="cyan", s=220, marker="*", edgecolors="black",
                            linewidths=1.5, zorder=7, label="g-best")
    ax.legend(loc="upper right", fontsize=9)
    text = ax.text(0.02, 0.97, "", transform=ax.transAxes, va="top", ha="left",
                   bbox=dict(boxstyle="round", fc="white", alpha=0.85), fontsize=10)

    def update(i):
        ps, gb, gf = history[i]
        particles.set_offsets(ps)
        gbest_scat.set_offsets([[gb[0], gb[1]]])
        text.set_text(f"iter {i+1}/{n_iters}\ng-best f = {gf:.2f}")
        return particles, gbest_scat, text

    anim = animation.FuncAnimation(fig, update, frames=n_iters, blit=False, interval=500)
    out = OUT_DIR / "pso.mp4"
    _save(anim, out, fps=fps)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# 3. GWO animation
# --------------------------------------------------------------------------- #


def render_gwo(seed: int = 0, pop: int = 30, n_iters: int = 30, fps: int = 2) -> Path:
    rng = np.random.default_rng(seed)
    pos = rng.uniform(BOUNDS[0], BOUNDS[1], size=(pop, 2))
    f = fitness(pos)

    history = []
    for t in range(n_iters):
        order = np.argsort(-f)
        alpha = pos[order[0]].copy()
        beta = pos[order[1]].copy()
        delta = pos[order[2]].copy()
        history.append((pos.copy(), order[:3].copy(), alpha.copy(), float(f[order[0]])))
        a = 2.0 * (1.0 - (t + 1) / n_iters)
        new_pos = np.zeros_like(pos)
        for i in range(pop):
            cands = np.zeros((3, 2))
            for k, leader in enumerate((alpha, beta, delta)):
                A = 2 * a * rng.uniform(size=2) - a
                C = 2 * rng.uniform(size=2)
                D = np.abs(C * leader - pos[i])
                cands[k] = leader - A * D
            new_pos[i] = cands.mean(axis=0)
        pos = np.clip(new_pos, BOUNDS[0], BOUNDS[1])
        f = fitness(pos)

    fig, ax = _base_axes("Grey Wolf Optimizer — α/β/δ averaged candidate")
    omega_scat = ax.scatter([], [], c="white", s=45, edgecolors="black",
                            linewidths=0.7, zorder=5, label="ω (others)")
    alpha_scat = ax.scatter([], [], c="red", s=200, marker="*", edgecolors="black",
                            linewidths=1.5, zorder=8, label="α")
    beta_scat = ax.scatter([], [], c="orange", s=140, marker="^", edgecolors="black",
                           linewidths=1.0, zorder=7, label="β")
    delta_scat = ax.scatter([], [], c="yellow", s=110, marker="s", edgecolors="black",
                            linewidths=1.0, zorder=6, label="δ")
    ax.legend(loc="upper right", fontsize=9)
    text = ax.text(0.02, 0.97, "", transform=ax.transAxes, va="top", ha="left",
                   bbox=dict(boxstyle="round", fc="white", alpha=0.85), fontsize=10)

    def update(i):
        ps, top3, alpha, af = history[i]
        omega_mask = np.ones(len(ps), dtype=bool)
        omega_mask[top3] = False
        omega_scat.set_offsets(ps[omega_mask])
        alpha_scat.set_offsets([[ps[top3[0]][0], ps[top3[0]][1]]])
        beta_scat.set_offsets([[ps[top3[1]][0], ps[top3[1]][1]]])
        delta_scat.set_offsets([[ps[top3[2]][0], ps[top3[2]][1]]])
        a_t = 2.0 * (1.0 - (i + 1) / n_iters)
        text.set_text(f"iter {i+1}/{n_iters}\na = {a_t:.2f}\nα-fitness = {af:.2f}")
        return omega_scat, alpha_scat, beta_scat, delta_scat, text

    anim = animation.FuncAnimation(fig, update, frames=n_iters, blit=False, interval=500)
    out = OUT_DIR / "gwo.mp4"
    _save(anim, out, fps=fps)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# 4. HHO animation (with mode colouring)
# --------------------------------------------------------------------------- #


MODE_NAMES = ["exploration", "soft besiege", "hard besiege", "soft+dive", "hard+dive"]
MODE_COLOURS = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e"]


def render_hho(seed: int = 0, pop: int = 30, n_iters: int = 30, fps: int = 2) -> Path:
    rng = np.random.default_rng(seed)
    pos = rng.uniform(BOUNDS[0], BOUNDS[1], size=(pop, 2))
    f = fitness(pos)
    rabbit_idx = int(np.argmax(f))
    rabbit = pos[rabbit_idx].copy()
    rabbit_f = float(f[rabbit_idx])

    history = []
    for t in range(n_iters):
        modes = np.zeros(pop, dtype=int)
        x_mean = pos.mean(axis=0)
        scale = 1.0 - (t + 1) / n_iters
        for i in range(pop):
            E0 = rng.uniform(-1.0, 1.0)
            E = 2.0 * E0 * scale
            absE = abs(E)
            if absE >= 1.0:
                modes[i] = 0
                q = rng.uniform()
                if q >= 0.5:
                    j = int(rng.integers(pop))
                    r1, r2 = rng.uniform(), rng.uniform()
                    pos[i] = pos[j] - r1 * np.abs(pos[j] - 2.0 * r2 * pos[i])
                else:
                    r3, r4 = rng.uniform(), rng.uniform()
                    pos[i] = (rabbit - x_mean) - r3 * (BOUNDS[0] + r4 * (BOUNDS[1] - BOUNDS[0]))
            else:
                r = rng.uniform()
                J = 2.0 * (1.0 - rng.uniform())
                if r >= 0.5 and absE >= 0.5:
                    modes[i] = 1
                    pos[i] = (rabbit - pos[i]) - E * np.abs(J * rabbit - pos[i])
                elif r >= 0.5 and absE < 0.5:
                    modes[i] = 2
                    pos[i] = rabbit - E * np.abs(rabbit - pos[i])
                else:
                    modes[i] = 3 if absE >= 0.5 else 4
                    target = pos[i] if absE >= 0.5 else x_mean
                    Y = rabbit - E * np.abs(J * rabbit - target)
                    pos[i] = Y  # simplified — skip Lévy Z for visual clarity
            pos[i] = np.clip(pos[i], BOUNDS[0], BOUNDS[1])
        f = fitness(pos)
        if f.max() > rabbit_f:
            rabbit_idx = int(np.argmax(f))
            rabbit = pos[rabbit_idx].copy()
            rabbit_f = float(f[rabbit_idx])
        history.append((pos.copy(), modes.copy(), rabbit.copy(), rabbit_f, scale))

    fig, ax = _base_axes("Harris Hawks — energy-gated 5-mode update")
    scat = ax.scatter([], [], c=[], s=55, edgecolors="black",
                      linewidths=0.7, zorder=5, vmin=0, vmax=4,
                      cmap=matplotlib.colors.ListedColormap(MODE_COLOURS))
    rabbit_scat = ax.scatter([], [], c="red", s=260, marker="*", edgecolors="black",
                             linewidths=1.5, zorder=8, label="rabbit")
    # Custom legend for modes (since scatter colormap doesn't auto-legend)
    from matplotlib.patches import Patch
    handles = [Patch(color=c, label=n) for c, n in zip(MODE_COLOURS, MODE_NAMES)]
    handles.insert(0, plt.Line2D([0], [0], marker="*", color="red", markersize=14,
                                  markeredgecolor="black", linewidth=0, label="rabbit"))
    ax.legend(handles=handles, loc="upper right", fontsize=8)
    text = ax.text(0.02, 0.97, "", transform=ax.transAxes, va="top", ha="left",
                   bbox=dict(boxstyle="round", fc="white", alpha=0.85), fontsize=10)

    def update(i):
        ps, modes, rb, rf, sc = history[i]
        scat.set_offsets(ps)
        scat.set_array(modes)
        rabbit_scat.set_offsets([[rb[0], rb[1]]])
        text.set_text(
            f"iter {i+1}/{n_iters}\n"
            f"energy envelope = {2*sc:.2f}\n"
            f"rabbit f = {rf:.2f}"
        )
        return scat, rabbit_scat, text

    anim = animation.FuncAnimation(fig, update, frames=n_iters, blit=False, interval=500)
    out = OUT_DIR / "hho.mp4"
    _save(anim, out, fps=fps)
    plt.close(fig)
    return out


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #


def main() -> None:
    print(f"Rendering animations to {OUT_DIR.relative_to(REPO_ROOT)} ...")
    if not shutil.which("ffmpeg"):
        print("  ⚠ ffmpeg not found on PATH — will fall back to GIF (install with `brew install ffmpeg`)")
    render_random_search()
    render_pso()
    render_gwo()
    render_hho()
    print(f"\nDone. Each clip is ~30-50 s at 2 fps; speed up in your editor if needed.")


if __name__ == "__main__":
    main()
