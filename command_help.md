
# pip命令
- `pip freeze > requirements.txt`:自动生成/更新 requirements 文件
- `pip install -r requirements.txt`:自动安装依赖库（根据 requirements 文件）
- `pip install xlwings==0.32.2`:安装指定版本的第三方库

# git命令
- `git add .`:将工作区的新增/修改添加到缓存区
- `git commit -m "提交说明"`:将缓存区记录的新增/修改提交到本地仓库（需填写提交说明）
- `git push`:将本地仓库最新代码推送到远程仓库（个人仓建议先 pull 最新代码避免冲突）
- `git log`:查看 git 提交日志
- `git fsck --lost-found`:检查丢失的提交记录（用于恢复误删的提交）
- `git show commitid`:查看具体提交记录内容（commitid 替换为实际 ID）
- `git apply commitid`:应用恢复的提交记录（需手动处理可能的冲突）
- `git stash`:将工作区的新增/修改添加到暂存区（可多次添加）
- `git stash save "注释内容"`:添加带注释的暂存记录（方便后续识别）
- `git stash list`:查看暂存区的历史记录列表
- `git stash clear`:清空暂存区的所有内容（包括 git add . 的记录）
- `git stash pop [0]`:[0] 为可选序号，默认取最后一次。从暂存区取出最近一次记录（取出后历史记录消失）
- `git stash apply [0]`:[0] 为具体序号（如 1、2、3）从暂存区应用某次记录（应用后历史记录保留）
- `git stash show [-p] [0]`:查看暂存区记录详情（-p 显示代码差异）

# pyuic命令
- `pyuic5 guessNumberWindow.ui -o guessNumberWindow.py`:不自动添加 Main 代码（需手动补充界面启动逻辑）
- `pyuic5 guessNumberWindow.ui -o guessNumberWindow.py -x`:自动添加 Main 代码（可直接运行测试界面）
- `pyuic5 outputSalesWin.ui -o outputSalesWin.py -x`:自动添加 Main 代码（可直接运行测试界面）