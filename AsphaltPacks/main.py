#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 00:05:30 2026

@author: tigrangasparian
"""
"""
unique_bundles has gaps. There needs to be a way to prevent them
"""

import math
import numpy as np
import matplotlib.pyplot as plt

def get_3_car_hunt_pack(Prob_featured: int):
    """Calculates the exact PMF of a single 3-pack bundle won in a car hunt race."""
    single_normal = np.zeros(16)
    single_normal[0] = 1-Prob_featured
    single_normal[1] = Prob_featured
    
    "Standard Packs 1st to 3rd"
    three_packs = single_normal
    for _ in range(2):
        three_packs = np.convolve(three_packs, single_normal)
        
    "Final convolved 3-pack PMF"
    return three_packs

def get_10_pack_distribution(Prob_featured: int):
    """Calculates the exact PMF of a single 10-pack bundle via convolution."""
    single_normal = np.zeros(16)
    single_normal[0] = 1-Prob_featured
    single_normal[3] = Prob_featured
    single_normal[15] = 0
    
    "Standard Packs 1st to 9th"
    nine_packs = single_normal
    for _ in range(8):
        nine_packs = np.convolve(nine_packs, single_normal)
        
    "Every 10th Pack"
    guaranteed = np.zeros(16)
    guaranteed[0], guaranteed[4], guaranteed[15] = 0, 1, 0
    
    "Final convolved 10-pack PMF"
    return np.convolve(nine_packs, guaranteed)

def get_10_multi_pack_distribution(N_cars: int,
                                   Prob_featured: int, 
                                   ):
    """
    Calculates the exact PMF of a single 10-pack bundle via convolution.
    
    N_cars is the amount of featured cars
    Prob_featured is the probability of getting any of the featured cars
    Ex.:
        N_cars=2
        Prob_featured=0.15
    """
    single_normal = np.zeros(16)
    single_normal[0] = 1-Prob_featured/N_cars
    single_normal[4] = Prob_featured/N_cars
    single_normal[15] = 0
    
    "Standard Packs 1st to 9th"
    nine_packs = single_normal
    for _ in range(8):
        nine_packs = np.convolve(nine_packs, single_normal)
        
    "Every 10th Pack"
    guaranteed = np.zeros(16)
    guaranteed[0], guaranteed[4], guaranteed[15] = 1-1/N_cars, 1/N_cars, 0

    return np.convolve(nine_packs, guaranteed)

def run_simulation(pmf: np.ndarray, 
                   goal_blueprints: int, 
                   simulations: int
                   ) -> np.ndarray:
    "Monte Carlo of player opening buldles until they get goal_blueprints"
    
    all_rewards = np.arange(len(pmf))
    obtained_blueprints = np.zeros(simulations, dtype=int)
    bundles_opened = np.zeros(simulations, dtype=int)  
    active = np.ones(simulations, dtype=bool)  

    while np.any(active):
        num_active = np.sum(active)
        rewards = np.random.choice(
            all_rewards, 
            p=pmf, 
            size=num_active)
        
        obtained_blueprints[active] += rewards
        bundles_opened[active] += 1  
        active[active] = obtained_blueprints[active] < goal_blueprints

    return bundles_opened, simulations

def cumulative_probability_plot(bundles_opened: np.ndarray, 
                                budget: int,
                                bundle_cost: int, 
                                goal_blueprints: int):
    
    unique_bundles, counts = np.unique(bundles_opened, return_counts=True)
    min_b, max_b = bundles_opened.min(), bundles_opened.max()
    unique_bundles = np.arange(min_b, max_b + 1)
    counts = np.array([np.sum(bundles_opened == b) for b in unique_bundles])
    Probability=np.cumsum(counts/len(bundles_opened))
    
    "Removes outliers"
    valid_mask = counts / len(bundles_opened) >= 1/1_000
    unique_bundles = unique_bundles[valid_mask]
    Probability = Probability[valid_mask]
    
    plt.figure(figsize=(10, 5))
    plt.yticks(np.arange(0,1.1,0.1))
    plt.grid(axis='y', linestyle='--', alpha=1, linewidth=0.7,color='k',zorder=1)

    
    plt.bar(unique_bundles, Probability, color='purple', alpha=1,zorder=2)
    X=math.floor(budget/bundle_cost)-np.min(unique_bundles)
    tokens_spent = math.floor(budget/bundle_cost)*bundle_cost
    
    if 0<=X<len(unique_bundles):
        plt.bar(unique_bundles[X], Probability[X], color='orange', alpha=1,zorder=2)
        plt.title(f"Probability of {goal_blueprints} bp in {math.floor(budget/bundle_cost)} bundles ({tokens_spent/1000}K tokens) is {Probability[X]*100:.1f}%", 
                  fontsize=16, fontweight='semibold',fontfamily="Arial")
    elif X>=len(unique_bundles):
        plt.title(f"Probability of {goal_blueprints} bp in {math.floor(budget/bundle_cost)} bundles ({tokens_spent/1000}K tokens) is {100}%", 
                  fontsize=16, fontweight='semibold',fontfamily="Arial")
    else:
        plt.title(f"Probability of {goal_blueprints} bp in {math.floor(budget/bundle_cost)} bundles ({tokens_spent/1000}K tokens) is {0}%", 
                     fontsize=16, fontweight='semibold',fontfamily="Arial")
    
    
    plt.ylabel("Cumulative Probability",fontsize=16, 
               fontweight='semibold',fontfamily="Arial")
    plt.xlabel("Number of 10-Pack Bundles Purchased",
               fontsize=16, fontweight='semibold',fontfamily="Arial")
    plt.show()

if __name__ == "__main__":

    "Your Needs"
    goal_blueprints = 109
    """
    Multi Pack Specs
    
    N_cars is the amount of featured cars
    Prob_featured is the probability of getting any of the featured cars
    """
    N_cars=6
    Prob_featured=0.20
    
    """
    Choose type of pack
    
    get_3_car_hunt_pack() is for opening car hunt packs 3 per race
    get_10_pack_distribution() is for opening single car packs
    get_10_multi_pack_distribution(): is for opening multi packs
    """
    #ten_pack_pmf = get_3_car_hunt_pack(Prob_featured)
    #ten_pack_pmf = get_10_pack_distribution(Prob_featured)
    ten_pack_pmf = get_10_multi_pack_distribution(N_cars,Prob_featured)
    
    "Monte Carlo Parameter"
    simulations = 1000_000

    bundles_opened, simulations = run_simulation(ten_pack_pmf,
                                                 goal_blueprints, 
                                                 simulations)
    #%%
if __name__ == "__main__":
    "Your Needs"
    budget = 45000
    bundle_cost = 600

    cumulative_probability_plot(bundles_opened, budget,
                                bundle_cost, goal_blueprints)
