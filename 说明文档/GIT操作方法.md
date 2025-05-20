# **完整 Fork 维护与定制开发流程总结**

## **1. 初始设置（仅需一次）**
```bash
# 克隆你的 Fork
git clone https://github.com/deepinnet/vllm.git
cd dify

# 添加原仓库为 upstream
git remote add upstream https://github.com/vllm-project/vllm.git

# 检查远程仓库
git remote -v
# 应显示：
# origin    https://github.com/vllm-project/vllm.git (fetch & push)
# upstream  https://github.com/vllm-project/vllm.git (fetch & push)
```

## **2. 推荐分支策略**
| 分支 | 用途 |
|------|------|
| `main` | 仅用于同步上游代码，保持干净 |
| `custom-dev` | 你的**长期开发分支**，所有定制在此进行 |
| `feature/xxx` (可选) | 短期功能分支，完成后合并回 `custom-dev` |

```bash
# 创建你的开发分支
git checkout -b custom-dev
```

---

## **3. 日常开发流程**
### **① 在 `custom-dev` 分支开发**
```bash
git checkout custom-dev

# 进行修改并提交
git add .
git commit -m "feat: 我的定制功能"
git push origin custom-dev
```

### **② 定期同步上游更新，或者官方发布重大版本升级，重要Bug修复等情况下**
```bash
# 1. 切换到 main 分支
git checkout main

# 2. 拉取上游最新代码（不自动合并）
git fetch upstream

# 3. 合并上游更新到你的 main 分支
git merge upstream/main

# 4. 推送更新到你的 Fork（可选）
git push origin main

# 5. 切换回开发分支
git checkout custom-dev

# 6. 合并上游更新到你的开发分支
git merge main
# 或使用 rebase（更整洁，但需处理冲突）
# git rebase main

# 7. 解决冲突（如果有）并推送
git push origin custom-dev
```

---

## **4. 冲突处理技巧**
- **查看冲突文件**：
  ```bash
  git status
  ```
- **手动编辑冲突文件**（搜索 `<<<<<<<`, `=======`, `>>>>>>>`）
- **标记冲突已解决**：
  ```bash
  git add <冲突文件>
  ```
- **继续合并/变基**：
  ```bash
  git commit  # 如果是 merge
  git rebase --continue  # 如果是 rebase
  ```

---

## **5. 高级维护技巧**
### **① 仅合并特定提交（cherry-pick）**
```bash
git cherry-pick <commit-hash>
```

### **② 清理提交历史（交互式 rebase）**
```bash
git rebase -i main
```

### **③ 强制同步 main 分支（丢弃本地修改）**
```bash
git checkout main
git reset --hard upstream/main
git push origin main --force
```

---

## **6. 最佳实践**
✅ **定期同步上游**（建议每周一次）  
✅ **模块化修改**，避免直接改核心文件  
✅ **提交信息清晰**，方便追踪  
✅ **维护 `CHANGES.md` 记录定制内容**  
❌ **避免直接在 `main` 分支开发**  

---

这样，你可以：
- **持续获取上游更新**（新功能/安全修复）  
- **安全保留定制代码**  
- **减少合并冲突风险**


将你的 `custom-dev` 分支修改同步回 `main` 分支的时机和方式需要谨慎处理，以下是专业建议：

---

### 🕰 **何时同步回 main 分支？**
1. **准备发布生产环境时**  
   - 当定制功能开发完成并通过测试后
   - 示例流程：
     ```bash
     # 1. 确保 main 已更新到最新上游代码
     git checkout main
     git fetch upstream
     git merge upstream/main

     # 2. 合并定制功能到 main
     git merge --no-ff custom-dev  # 显式生成合并提交
     git push origin main

     # 3. 打标签并部署
     git tag -a v1.0-custom -m "包含定制功能的生产版本"
     git push origin --tags
     ```

---

**黄金准则**：  
> 保持 `main` 分支随时可发布，合并 `custom-dev` 前必须：  
> 1. 测试通过  
> 2. 文档更新  
> 3. 创建回滚点（如 tag）