#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猜数字小游戏
作者: 你的助手
日期: 2026-02-28
"""

import random
import time


class GuessNumberGame:
    """猜数字游戏类"""
    
    def __init__(self):
        self.min_number = 1
        self.max_number = 100
        self.max_attempts = 10
        self.secret_number = None
        self.attempts = 0
        self.best_score = float('inf')  # 存储最佳成绩（最少尝试次数）
        self.games_played = 0
        
    def generate_secret_number(self):
        """生成秘密数字"""
        self.secret_number = random.randint(self.min_number, self.max_number)
        self.attempts = 0
        
    def get_hint(self, guess):
        """根据猜测给出提示"""
        if guess < self.secret_number:
            return "太小了！再试一次。"
        elif guess > self.secret_number:
            return "太大了！再试一次。"
        else:
            return "恭喜！猜对了！"
    
    def get_warm_hint(self, guess):
        """根据接近程度给出更详细的提示"""
        difference = abs(guess - self.secret_number)
        
        if difference == 0:
            return "🎉 完美！完全正确！"
        elif difference <= 5:
            return "🔥 非常接近了！就差一点点！"
        elif difference <= 10:
            return "👍 很接近了！继续加油！"
        elif difference <= 20:
            return "👌 有点接近了，再调整一下。"
        elif difference <= 30:
            return "🤔 距离目标还有一段距离。"
        else:
            return "😅 离目标还比较远，大胆猜测！"
    
    def play_round(self):
        """玩一轮游戏"""
        print(f"\n{'='*50}")
        print("🎮 猜数字游戏开始！")
        print(f"我已经想好了一个 {self.min_number} 到 {self.max_number} 之间的数字。")
        print(f"你有 {self.max_attempts} 次机会猜中它。")
        print("="*50)
        
        self.generate_secret_number()
        
        while self.attempts < self.max_attempts:
            remaining = self.max_attempts - self.attempts
            print(f"\n📊 剩余尝试次数: {remaining}")
            
            try:
                guess = input("请输入你的猜测（输入 'q' 退出）: ").strip()
                
                # 检查是否退出
                if guess.lower() == 'q':
                    print("游戏结束。秘密数字是:", self.secret_number)
                    return False
                
                guess = int(guess)
                
                # 检查范围
                if guess < self.min_number or guess > self.max_number:
                    print(f"❌ 请输入 {self.min_number} 到 {self.max_number} 之间的数字！")
                    continue
                
                self.attempts += 1
                
                # 检查是否猜中
                if guess == self.secret_number:
                    print(f"\n{'🎉'*20}")
                    print(f"恭喜！你在第 {self.attempts} 次尝试时猜中了数字 {self.secret_number}！")
                    print(f"{'🎉'*20}")
                    
                    # 更新最佳成绩
                    if self.attempts < self.best_score:
                        self.best_score = self.attempts
                        print(f"🏆 新纪录！这是你的最佳成绩！")
                    
                    self.games_played += 1
                    return True
                
                # 给出提示
                hint = self.get_hint(guess)
                warm_hint = self.get_warm_hint(guess)
                print(f"{hint} {warm_hint}")
                
            except ValueError:
                print("❌ 请输入有效的数字！")
        
        # 如果用完所有尝试次数
        print(f"\n{'💀'*20}")
        print(f"游戏结束！你没有在 {self.max_attempts} 次尝试内猜中数字。")
        print(f"秘密数字是: {self.secret_number}")
        print(f"{'💀'*20}")
        
        self.games_played += 1
        return False
    
    def show_statistics(self):
        """显示游戏统计信息"""
        print(f"\n{'📊'*10} 游戏统计 {'📊'*10}")
        print(f"游戏次数: {self.games_played}")
        if self.best_score != float('inf'):
            print(f"最佳成绩: {self.best_score} 次尝试")
        else:
            print("最佳成绩: 暂无")
        print(f"数字范围: {self.min_number} - {self.max_number}")
        print(f"每次游戏最大尝试次数: {self.max_attempts}")
        print(f"{'📊'*25}")
    
    def show_instructions(self):
        """显示游戏说明"""
        print(f"\n{'📖'*10} 游戏说明 {'📖'*10}")
        print("1. 我会随机生成一个 1-100 之间的数字")
        print(f"2. 你有 {self.max_attempts} 次机会猜中它")
        print("3. 每次猜测后，我会告诉你猜大了还是猜小了")
        print("4. 根据你猜测的接近程度，我会给出不同的提示")
        print("5. 输入 'q' 可以随时退出游戏")
        print("6. 目标是尽可能用最少的次数猜中数字")
        print(f"{'📖'*25}")
    
    def change_settings(self):
        """修改游戏设置"""
        print(f"\n{'⚙️'*10} 游戏设置 {'⚙️'*10}")
        try:
            new_min = int(input(f"当前最小数字 ({self.min_number})，请输入新的最小值: "))
            new_max = int(input(f"当前最大数字 ({self.max_number})，请输入新的最大值: "))
            new_attempts = int(input(f"当前最大尝试次数 ({self.max_attempts})，请输入新的次数: "))
            
            if new_min >= new_max:
                print("❌ 最小值必须小于最大值！")
                return
            
            if new_attempts <= 0:
                print("❌ 尝试次数必须大于0！")
                return
            
            self.min_number = new_min
            self.max_number = new_max
            self.max_attempts = new_attempts
            print("✅ 设置已更新！")
            
        except ValueError:
            print("❌ 请输入有效的数字！")
    
    def main_menu(self):
        """显示主菜单"""
        while True:
            print(f"\n{'🌟'*20}")
            print("         猜数字游戏主菜单")
            print(f"{'🌟'*20}")
            print("1. 🎮 开始新游戏")
            print("2. 📊 查看统计")
            print("3. 📖 游戏说明")
            print("4. ⚙️  修改设置")
            print("5. 🚪 退出游戏")
            print(f"{'🌟'*20}")
            
            choice = input("请选择 (1-5): ").strip()
            
            if choice == '1':
                self.play_round()
            elif choice == '2':
                self.show_statistics()
            elif choice == '3':
                self.show_instructions()
            elif choice == '4':
                self.change_settings()
            elif choice == '5':
                print("\n感谢游玩！再见！👋")
                break
            else:
                print("❌ 请输入 1-5 之间的数字！")


def main():
    """主函数"""
    print("欢迎来到猜数字游戏！")
    print("这是一个简单但有趣的数字猜测游戏。")
    
    # 创建游戏实例
    game = GuessNumberGame()
    
    # 显示主菜单
    game.main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n游戏被中断。再见！")
    except Exception as e:
        print(f"\n发生错误: {e}")
        print("请检查程序并重试。")