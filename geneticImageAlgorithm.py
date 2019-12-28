# Genetic Algorthim for image duplication
# Steph Herbers
# AI Final project

import numpy as np
import cv2
import random
import functools
import itertools
import operator
import sys
import matplotlib.pyplot as plt
import math


MUTATION_PERCENT = 0.5

''' Returns an array containing 8 numpy arrays each of the same size as the target image and filled with randomly generated pixels'''
def createInitialPopulation(imageShape, numberOfIndividuals):
    population = []
    for i in range(numberOfIndividuals):
        population.append(np.random.random(functools.reduce(operator.mul, imageShape))*256)
    return population

'''calcultes fitness value given the target image and parent in population'''
def calculateFitness(target, parent):
    fitness = 0
    for i in range(len(target)):
        fitness += abs(target.item(i) - parent.item(i))
    fitness = 10000000000 - fitness
    return fitness

'''returns the index of the numpy array of the parent in the population with the highest fitness'''
def mostFitParentIndex(target, population):
    indexOfMostFit = 0
    mostFitValue = 0
    for parent in range(len(population)):
        value = calculateFitness(target, population[parent])
        if value > mostFitValue:
            mostFitValue = value
            indexOfMostFit = parent
    return indexOfMostFit

'''selects the fittest parent and adds to a new population array'''
def selectSurvivingPopulation(target, population):
    survivingPopulation = []
    while len(survivingPopulation) < len(population):
        currentFittestParentIndex = mostFitParentIndex(target, population)
        survivingPopulation.append(population[currentFittestParentIndex])
        population.pop(currentFittestParentIndex)
    return survivingPopulation

'''returns an array of the surviving parents and new offspring computed with crossover and mutation'''
def createNextGeneration(target, survivingPopulation, generationNum):
    nextGeneration = []
    while len(nextGeneration) < len(survivingPopulation):
        firstParentIndex = 0
        secondParentIndex = 0
        while firstParentIndex == secondParentIndex:
            firstParentIndex = random.randint(0,len(survivingPopulation)-1)
            secondParentIndex = random.randint(0,len(survivingPopulation)-1)
        offspring = crossover(survivingPopulation[firstParentIndex],survivingPopulation[secondParentIndex])
        mutatedOffspring = mutation(target, offspring)
        nextGeneration.append(mutatedOffspring)
    nextGeneration = nextGeneration + survivingPopulation
    return nextGeneration

'''Returns offspring with each pixel manipulated by MUTATION_PERCENT'''
def mutation(target, offspring):
    mutatedOffspring = []
    for i in range(len(target)):
        difference = target.item(i) - offspring.item(i)
        changeAmount = random.choice((-1,1)) * (difference * MUTATION_PERCENT)
        if (abs(difference)) < .000001:
            mutatedOffspring.append(offspring.item(i))
        else:
            mutatedOffspring.append((abs(offspring.item(i) + changeAmount))%255)
    offspring = np.asarray(mutatedOffspring)

    return offspring


'''returns a new singular numpy array represents an offspring of two surviving parents'''
def crossover(firstParent, secondParent):
    parentOne = firstParent.copy()
    parentTwo = secondParent.copy()

    combinedOffspring = []
    for i in range(len(firstParent)):
        if i%2 == 0:
            combinedOffspring.append(parentOne.item(i))
        else:
            combinedOffspring.append(parentTwo.item(i))
    offspring = np.asarray(combinedOffspring)
    return offspring


def main():
    #targetImage can be passed through the command line
    targetImage = cv2.imread(sys.argv[1])
    targetImage = cv2.cvtColor(targetImage, cv2.COLOR_BGR2RGB)

    numOfGenerations = int(sys.argv[2])

    reducedTargetImage = targetImage.copy()
    reducedTargetImage = reducedTargetImage.reshape(targetImage.size)


    population = createInitialPopulation(targetImage.shape, 8)
    for i in range(numOfGenerations):
        newPop = selectSurvivingPopulation(reducedTargetImage, population)
        population = createNextGeneration(reducedTargetImage, newPop, i)
        if i % 5 ==0:
            print("Generation ", i)

    finalImage = population[mostFitParentIndex(reducedTargetImage, population)]

    for i in range(finalImage.size):
        finalImage[i] = 255 - finalImage[i]

    outputImageName = "{}_{}gen.png".format(sys.argv[1][:-4], numOfGenerations)
    imageToDisplay = np.reshape(a=finalImage, newshape=targetImage.shape)
    plt.imsave(outputImageName, (imageToDisplay * 255).astype(np.uint8))


if __name__ == "__main__":
    main()
