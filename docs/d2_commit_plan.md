# D2 Git Commit Plan

`.gitignore` 已更新（添加 `~$*` 和 `*_BACKUP_*.{pptx,docx,xlsx}`）。剩下需要你在本地终端执行——沙箱无法操作 `.git/` 目录。

## 1. 清掉残留的 git 锁（必做）

```bash
cd ~/Documents/CITS4404/Project
rm -f .git/index.lock
```

（沙箱里跑过 `git status`, 留了个空的 `index.lock`, 不清掉的话 git add 会报错）

## 2. 检查待提交列表

```bash
git status --short
```

应该看到这 7 项（**不**应该看到 `~$...pptx` 或 `..._BACKUP_*.pptx`, 它们已被 ignore）:

```
 M .gitignore
 M docs/d2_video_script.md
?? CITS4404_Team20_Presentation.pptx
?? docs/d2_video_alignment_review.md
?? docs/d2_video_script_v2.md
?? results/animations/
?? tools/make_animations.py
```

## 3. 一次性暂存全部

```bash
git add -A
git status --short    # 确认全部变为 M/A, 无遗漏
```

## 4. 提交

```bash
git commit -m "docs(D2): add final presentation, PPT-aligned video script, and animations

- Add CITS4404_Team20_Presentation.pptx (21 slides; Slide 21 carries
  the AI/TTS assistance disclosure; Slide 5 PSO/HHO table de-duplicated)
- Add docs/d2_video_script_v2.md aligned to the 21-slide deck with
  4 animation B-roll cues; total narration ~2,559 words (~19-21 min
  depending on TTS pace, well under the 25-min cap)
- Add docs/d2_video_alignment_review.md documenting the PPT-vs-script
  alignment analysis and the rationale for v2 revisions
- Add results/animations/{rs,pso,gwo,hho}.mp4 (4 algorithm walkthrough
  animations, ~680 KB total) and tools/make_animations.py generator
- Update docs/d2_video_script.md (v1) with animation B-roll structure
- Update .gitignore: exclude Office lockfiles (~\$*) and timestamped
  local backups (*_BACKUP_*.{pptx,docx,xlsx})"
```

## 5. 推送（如有远端）

```bash
git push
```

---

## 总体积估算

提交体积约 **1.4 MB**: PPT 640 KB + 动画 676 KB + 文档/脚本 ~80 KB。对 git 完全可接受。

## 不会进入提交的临时文件（保留在本地）

- `~$CITS4404_Team20_Presentation.pptx` — Office 锁文件（PowerPoint 关闭后会自动消失）
- `CITS4404_Team20_Presentation_BACKUP_20260517_145700.pptx` — 我做的安全备份, 你确认新 PPT 没问题之后可以本地删掉

两者都已被新 `.gitignore` 规则覆盖, `git add` 不会带上它们。
