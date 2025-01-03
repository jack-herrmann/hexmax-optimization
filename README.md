# Maximizing Hexadecimal Values with Limited Segment Swaps

This project was developed as part of the semifinals of the German Informatics Competition 2021, where it received an exceptional score of 20/20 + 2 additional points.

## Overview

The task is to maximize a hexadecimal number represented on a seven-segment display by swapping a limited number of segments. The goal is to determine the largest possible valid number that can be achieved under these constraints.

## Problem Description

- **Objective**: Maximize the value of a hexadecimal number by rearranging a limited number of segments on a seven-segment display.
- **Constraints**: 
  - Each digit must be valid on a seven-segment display.
  - A fixed number of swaps is allowed across all digits.
  - The original number cannot decrease.

## Solution Approach

### Search Tree and Pruning
1. **Search Tree Construction**:
   - For each digit, a tree of possible transformations is generated, storing:
     - The number of swaps required.
     - The resulting valid hexadecimal digits.

2. **Depth-First Search (DFS)**:
   - A DFS algorithm iterates through the search tree, exploring potential transformations for each digit.
   - Memoization avoids redundant calculations for previously visited states.

3. **Pruning Invalid Paths**:
   - Subtrees leading to invalid configurations (e.g., insufficient swaps remaining) are pruned to enhance efficiency.

### Optimization Techniques
- **Memoization**: Stores results of sub-problems to reduce redundant computations.
- **Deque for Efficient Callstack Management**: Allows faster addition/removal of nodes during DFS traversal.

## Extensions and Variants
The program can be extended to handle additional constraints, such as:
- Unlimited swaps but limited segments.
- Finding the smallest valid number instead of the largest.
- Supporting an infinite number of digits or segments.

## Usage
The implementation includes functions for:
- Generating transformation trees.
- Executing DFS with pruning and memoization.
- Visualizing segment swaps for small datasets.

(For a more detailed documentation and analysis, view the included pdf file)
