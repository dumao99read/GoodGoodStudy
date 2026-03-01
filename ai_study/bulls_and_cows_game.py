#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猜数字游戏（Bulls and Cows / 1A2B 游戏）
作者: 你的助手
日期: 2026-02-28

游戏规则：
1. 从0-9中选取X个不重复的数字作为目标数字
2. 玩家有Y次竞猜机会
3. 每次猜测后，系统返回结果：
   - A: 数字和位置都正确
   - B: 数字正确但位置错误
   - A的优先级比B高（已经记作A的数字不会再统计B）
4. 当所有数字和位置都正确时（XA0B），玩家胜利
"""

import random
import time
from typing import List, Tuple, Optional


class BullsAndCowsGame:
    """猜数字游戏（Bulls and Cows）类"""
    
    def __init__(self):
        self.digits = list(range(10))  # 0-9的数字
        self.default_digit_count = 4   # 默认数字个数
        self.default_max_attempts = 10 # 默认最大尝试次数
        self.digit_count = self.default_digit_count
        self.max_attempts = self.default_max_attempts
        self.secret_number = None      # 秘密数字列表
        self.attempts = 0              # 当前尝试次数
        self.guess_history = []        # 猜测历史
        self.result_history = []       # 结果历史
        self.games_played = 0          # 游戏次数
        self.wins = 0                  # 胜利次数
        self.best_score = float('inf') # 最佳成绩（最少尝试次数）
        
    def generate_secret_number(self) -> List[int]:
        """生成不重复的秘密数字列表"""
        available_digits = self.digits.copy()
        random.shuffle(available_digits)
        return available_digits[:self.digit_count]
    
    def validate_guess(self, guess_str: str) -> Optional[List[int]]:
        """验证玩家输入的猜测"""
        guess_str = guess_str.strip()
        
        # 检查退出命令
        if guess_str.lower() == 'q':
            return None
        
        # 检查长度
        if len(guess_str) != self.digit_count:
            print(f"❌ 请输入 {self.digit_count} 位数字！")
            return False
        
        # 检查是否为数字
        if not guess_str.isdigit():
            print("❌ 请输入数字！")
            return False
        
        # 转换为数字列表
        guess_digits = [int(d) for d in guess_str]
        
        # 检查是否有重复数字
        if len(set(guess_digits)) != self.digit_count:
            print("❌ 数字不能重复！")
            return False
        
        # 检查数字范围
        for digit in guess_digits:
            if digit not in self.digits:
                print(f"❌ 请输入 0-9 之间的数字！")
                return False
        
        return guess_digits
    
    def calculate_result(self, guess: List[int]) -> Tuple[int, int]:
        """计算猜测结果（A和B的数量）"""
        a_count = 0  # 数字和位置都正确
        b_count = 0  # 数字正确但位置错误
        
        # 先计算A（数字和位置都正确）
        for i in range(self.digit_count):
            if guess[i] == self.secret_number[i]:
                a_count += 1
        
        # 计算B（数字正确但位置错误）
        # 需要排除已经算作A的数字
        secret_remaining = []
        guess_remaining = []
        
        for i in range(self.digit_count):
            if guess[i] != self.secret_number[i]:
                secret_remaining.append(self.secret_number[i])
                guess_remaining.append(guess[i])
        
        # 统计guess_remaining中有多少数字在secret_remaining中
        for digit in guess_remaining:
            if digit in secret_remaining:
                b_count += 1
                secret_remaining.remove(digit)  # 移除已匹配的数字
        
        return a_count, b_count
    
    def format_result(self, a_count: int, b_count: int) -> str:
        """格式化结果显示"""
        result_parts = []
        if a_count > 0:
            result_parts.append(f"{a_count}A")
        if b_count > 0:
            result_parts.append(f"{b_count}B")
        
        if not result_parts:
            return "0A0B"
        
        return "".join(result_parts)
    
    def get_hint_based_on_result(self, a_count: int, b_count: int) -> str:
        """根据结果给出提示"""
        total_digits = self.digit_count
        
        if a_count == total_digits:
            return "🎉 完美！完全正确！"
        
        correct_count = a_count + b_count
        
        # 特殊情况处理
        if a_count == total_digits - 1 and b_count == 0:
            return "🔥 就差一个数字的位置了！"
        elif a_count == total_digits - 1:
            return "👍 非常接近了！"
        elif correct_count == total_digits:
            return "🔀 所有数字都对了，但位置需要调整！"
        
        # 根据正确数字的比例给出提示
        correct_ratio = correct_count / total_digits
        
        if correct_ratio >= 0.75:
            return "👌 大部分数字都对了！"
        elif correct_ratio >= 0.5:
            return "🤔 大约一半的数字对了。"
        elif correct_ratio >= 0.25:
            return "😅 只有少数数字对了。"
        elif correct_count > 0:
            return "😟 只有1-2个数字对了。"
        else:
            return "💀 完全没有猜中，换个思路试试！"
    
    def show_guess_history(self):
        """显示猜测历史"""
        if not self.guess_history:
            print("暂无猜测历史。")
            return
        
        print(f"\n{'📜'*15} 猜测历史 {'📜'*15}")
        print(f"{'序号':<6} {'猜测':<10} {'结果':<8} {'提示':<20}")
        print("-" * 50)
        
        for i, (guess, result) in enumerate(zip(self.guess_history, self.result_history), 1):
            guess_str = "".join(str(d) for d in guess)
            a_count, b_count = result
            result_str = self.format_result(a_count, b_count)
            hint = self.get_hint_based_on_result(a_count, b_count)
            print(f"{i:<6} {guess_str:<10} {result_str:<8} {hint:<20}")
        
        print(f"{'📜'*40}")
    
    def play_round(self) -> bool:
        """玩一轮游戏"""
        print(f"\n{'='*60}")
        print("🎮 猜数字游戏（Bulls and Cows）开始！")
        print(f"我已经想好了一个 {self.digit_count} 位不重复的数字（0-9）。")
        print(f"你有 {self.max_attempts} 次机会猜中它。")
        print("="*60)
        
        # 生成秘密数字
        self.secret_number = self.generate_secret_number()
        self.attempts = 0
        self.guess_history = []
        self.result_history = []
        
        print(f"\n💡 提示：输入 {self.digit_count} 位不重复的数字（0-9），输入 'q' 退出游戏。")
        
        while self.attempts < self.max_attempts:
            remaining = self.max_attempts - self.attempts
            print(f"\n📊 第 {self.attempts + 1} 次尝试，剩余 {remaining} 次")
            
            # 获取玩家输入
            guess_input = input("请输入你的猜测: ").strip()
            
            # 验证输入
            validated_guess = self.validate_guess(guess_input)
            
            if validated_guess is None:  # 用户退出
                secret_str = "".join(str(d) for d in self.secret_number)
                print(f"游戏结束。秘密数字是: {secret_str}")
                return False
            elif validated_guess is False:  # 输入无效
                continue
            
            # 计算结果
            self.attempts += 1
            a_count, b_count = self.calculate_result(validated_guess)
            result_str = self.format_result(a_count, b_count)
            hint = self.get_hint_based_on_result(a_count, b_count)
            
            # 保存历史
            self.guess_history.append(validated_guess)
            self.result_history.append((a_count, b_count))
            
            # 显示结果
            guess_str = "".join(str(d) for d in validated_guess)
            print(f"\n🎯 你的猜测: {guess_str}")
            print(f"📊 结果: {result_str}")
            print(f"💡 {hint}")
            
            # 检查是否胜利
            if a_count == self.digit_count:
                print(f"\n{'🎉'*25}")
                print(f"恭喜！你在第 {self.attempts} 次尝试时猜中了数字！")
                print(f"秘密数字是: {''.join(str(d) for d in self.secret_number)}")
                print(f"{'🎉'*25}")
                
                # 更新统计
                self.games_played += 1
                self.wins += 1
                if self.attempts < self.best_score:
                    self.best_score = self.attempts
                    print(f"🏆 新纪录！这是你的最佳成绩！")
                
                # 显示猜测历史
                self.show_guess_history()
                return True
        
        # 如果用完所有尝试次数
        secret_str = "".join(str(d) for d in self.secret_number)
        print(f"\n{'💀'*25}")
        print(f"游戏结束！你没有在 {self.max_attempts} 次尝试内猜中数字。")
        print(f"秘密数字是: {secret_str}")
        print(f"{'💀'*25}")
        
        self.games_played += 1
        
        # 显示猜测历史
        self.show_guess_history()
        return False
    
    def show_statistics(self):
        """显示游戏统计信息"""
        print(f"\n{'📊'*15} 游戏统计 {'📊'*15}")
        print(f"游戏次数: {self.games_played}")
        print(f"胜利次数: {self.wins}")
        if self.games_played > 0:
            win_rate = (self.wins / self.games_played) * 100
            print(f"胜率: {win_rate:.1f}%")
        else:
            print(f"胜率: 0%")
        
        if self.best_score != float('inf'):
            print(f"最佳成绩: {self.best_score} 次尝试")
        else:
            print("最佳成绩: 暂无")
        
        print(f"当前设置: {self.digit_count} 位数字，{self.max_attempts} 次尝试")
        print(f"{'📊'*40}")
    
    def show_instructions(self):
        """显示游戏说明"""
        print(f"\n{'📖'*15} 游戏说明 {'📖'*15}")
        print("游戏规则:")
        print("1. 我会从 0-9 中随机选择 X 个不重复的数字作为目标数字")
        print(f"2. 你有 Y 次机会猜中这个数字（当前: {self.digit_count}位, {self.max_attempts}次）")
        print("3. 每次猜测后，我会返回 A 和 B 的结果：")
        print("   - A: 数字和位置都正确")
        print("   - B: 数字正确但位置错误")
        print("   - A的优先级比B高（已经记作A的数字不会再统计B）")
        print("4. 示例:")
        print("   秘密数字: 1234")
        print("   猜测: 1356 → 1A1B（1正确且位置对，3正确但位置错）")
        print("   猜测: 4321 → 0A4B（所有数字都对，但位置全错）")
        print("   猜测: 1234 → 4A0B（完全正确，胜利！）")
        print("5. 输入 'q' 可以随时退出当前游戏")
        print(f"{'📖'*40}")
    
    def change_settings(self):
        """修改游戏设置"""
        print(f"\n{'⚙️'*15} 游戏设置 {'⚙️'*15}")
        
        try:
            # 修改数字个数
            print(f"当前数字个数: {self.digit_count} (1-10)")
            new_digit_count = input("请输入新的数字个数 (1-10，回车保持当前): ").strip()
            if new_digit_count:
                new_digit_count = int(new_digit_count)
                if 1 <= new_digit_count <= 10:
                    self.digit_count = new_digit_count
                    print(f"✅ 数字个数已更新为: {self.digit_count}")
                else:
                    print("❌ 数字个数必须在 1-10 之间！")
            
            # 修改尝试次数
            print(f"\n当前最大尝试次数: {self.max_attempts} (1-50)")
            new_max_attempts = input("请输入新的最大尝试次数 (1-50，回车保持当前): ").strip()
            if new_max_attempts:
                new_max_attempts = int(new_max_attempts)
                if 1 <= new_max_attempts <= 50:
                    self.max_attempts = new_max_attempts
                    print(f"✅ 最大尝试次数已更新为: {self.max_attempts}")
                else:
                    print("❌ 尝试次数必须在 1-50 之间！")
            
            print("\n✅ 设置已保存！")
            
        except ValueError:
            print("❌ 请输入有效的数字！")
    
    def show_difficulty_presets(self):
        """显示难度预设"""
        print(f"\n{'🎯'*15} 难度预设 {'🎯'*15}")
        print("1. 简单模式 - 3位数字，12次尝试")
        print("2. 标准模式 - 4位数字，10次尝试（默认）")
        print("3. 困难模式 - 5位数字，8次尝试")
        print("4. 专家模式 - 6位数字，6次尝试")
        print("5. 大师模式 - 7位数字，5次尝试")
        print(f"{'🎯'*40}")
        
        choice = input("请选择难度 (1-5，回车取消): ").strip()
        
        if choice == '1':
            self.digit_count = 3
            self.max_attempts = 12
            print("✅ 已设置为简单模式")
        elif choice == '2':
            self.digit_count = 4
            self.max_attempts = 10
            print("✅ 已设置为标准模式")
        elif choice == '3':
            self.digit_count = 5
            self.max_attempts = 8
            print("✅ 已设置为困难模式")
        elif choice == '4':
            self.digit_count = 6
            self.max_attempts = 6
            print("✅ 已设置为专家模式")
        elif choice == '5':
            self.digit_count = 7
            self.max_attempts = 5
            print("✅ 已设置为大师模式")
        elif choice:
            print("❌ 无效的选择！")
    
    def show_analysis_tools(self):
        """显示分析工具"""
        if not self.guess_history:
            print("暂无猜测数据可供分析。")
            return
        
        print(f"\n{'🔍'*15} 分析工具 {'🔍'*15}")
        
        # 显示可能的数字
        print("可能的数字分析:")
        
        # 收集所有已猜测的数字
        guessed_digits = set()
        for guess in self.guess_history:
            guessed_digits.update(guess)
        
        print(f"已尝试的数字: {sorted(guessed_digits)}")
        print(f"未尝试的数字: {sorted(set(self.digits) - guessed_digits)}")
        
        # 显示位置分析
        print("\n位置分析（基于最后一次猜测）:")
        last_guess = self.guess_history[-1]
        last_result = self.result_history[-1]
        
        a_count, b_count = last_result
        if a_count > 0:
            print(f"有 {a_count} 个数字在正确位置上")
        if b_count > 0:
            print(f"有 {b_count} 个数字正确但位置错误")
        
        print(f"{'🔍'*40}")
    
    def main_menu(self):
        """显示主菜单"""
        while True:
            print(f"\n{'🌟'*25}")
            print("       猜数字游戏（Bulls and Cows）")
            print(f"{'🌟'*25}")
            print("1. 🎮 开始新游戏")
            print("2. 📊 查看统计")
            print("3. 📖 游戏说明")
            print("4. ⚙️  自定义设置")
            print("5. 🎯 难度预设")
            print("6. 🔍 分析工具（需有游戏记录）")
            print("7. 📜 查看历史（需有游戏记录）")
            print("8. 🚪 退出游戏")
            print(f"{'🌟'*25}")
            
            choice = input("请选择 (1-8): ").strip()
            
            if choice == '1':
                self.play_round()
            elif choice == '2':
                self.show_statistics()
            elif choice == '3':
                self.show_instructions()
            elif choice == '4':
                self.change_settings()
            elif choice == '5':
                self.show_difficulty_presets()
            elif choice == '6':
                self.show_analysis_tools()
            elif choice == '7':
                self.show_guess_history()
            elif choice == '8':
                print("\n感谢游玩！再见！👋")
                break
            else:
                print("❌ 请输入 1-8 之间的数字！")


def main():
    """主函数"""
    print("欢迎来到猜数字游戏（Bulls and Cows）！")
    print("这是一个经典的数字逻辑游戏，比简单猜数字更有挑战性。")
    
    # 创建游戏实例
    game = BullsAndCowsGame()
    
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