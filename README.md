# PipeMania Solver

## Overview

This project implements a solver for the **PIPEMANIA** puzzle using search algorithms in Python 3.8.2. The goal is to find the unique solution where all pipes are connected without leaks.

## Problem Description

PIPEMANIA is a puzzle game where a grid contains different types of pipe pieces. The objective is to rotate these pieces to create a continuous pipeline for the flow. Given an initial configuration of the grid, the program must determine the correct orientation for each pipe to form a valid solution.

## Input Format

The input is read from the **standard input** and follows this format:

<pipe-piece-l1c1> <pipe-piece-l1c2> ... <pipe-piece-l1cN> 
<pipe-piece-l2c1> <pipe-piece-l2c2> ... <pipe-piece-l2cN> 
... 
<pipe-piece-lNc1> <pipe-piece-lNc2> ... <pipe-piece-lNcN>


Each pipe piece is represented as a **two-letter string**:
- **First letter**: Type of piece  
  - `F` - Fecho (End piece)  
  - `B` - Bifurcação (Branching piece)  
  - `V` - Volta (Corner piece)  
  - `L` - Ligação (Straight pipe)  
- **Second letter**: Orientation  
  - `C` - Up  
  - `B` - Down  
  - `E` - Left  
  - `D` - Right  
  - `H` - Horizontal (for `L` pieces)  
  - `V` - Vertical (for `L` pieces)  


## Output Format

The output must describe the correct orientation of the pipes in the same format as the input.

## Search Algorithms 

- Função breadth_first_tree_search;
- Função depth_first_tree_search;
- Função greedy_search;
- Função astar_search.


