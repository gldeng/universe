#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from generate_theory_json import extract_dimension

def test_dimension_extraction():
    test_cases = [
        ("# 测试理论 v1.0\n(维度：D1)", "D1"),
        ("# 测试理论 v1.0\n(维度:D2)", "D2"),
        ("# 测试理论 v1.0\n维度：D3", "D3"),
        ("# 测试理论 v1.0\n维度:D4", "D4"),
        ("# 测试理论 v1.0\n(D5)", "D5"),
        ("# 测试理论 v1.0\nD6维度", "D6"),
        ("# 测试理论 v1.0\n维度：7", "D7"),
        ("# 测试理论 v1.0\n维度:8", "D8"),
        ("# 测试理论 v1.0\n(维度： D ∞)", "D∞"),
        ("# 测试理论 v1.0\n维度：D 9", "D9"),
        ("# 测试理论 v1.0\n(维度:D  10  )", "D10"),
        ("# 测试理论 v1.0\n没有维度信息", "无维度"),
        ("# 测试理论 v1.0\n维度：D+∞", "D+∞"),
    ]

    print("开始测试维度提取功能...")
    print("-" * 50)
    
    for i, (test_input, expected) in enumerate(test_cases, 1):
        result = extract_dimension(test_input)
        status = "✓" if result == expected else "✗"
        print(f"测试 {i:2d}: {status} ", end="")
        print(f"输入: {test_input.strip():<30} ", end="")
        print(f"期望: {expected:<6} ", end="")
        print(f"实际: {result:<6}")
        
        if result != expected:
            print(f"    错误：期望得到 {expected}，但得到了 {result}")
    
    print("-" * 50)

if __name__ == "__main__":
    test_dimension_extraction() 