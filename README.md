```
Image Replication Genetic Algorithm Steph Herbers
Artificial Intelligence Final Project November 24, 2019
```
# 1 Introduction

This is a genetic algorithm for replicating an input photo. The individuals in the first generation
are photos of the same size as the target image with randomized pixels. It works for all images and
generally shows a vague resemblance to the target image starting at 25 generations.

Example generations on images I have already ran are provided in previousOutcomes.pdf

# 2 Running the Code

A name of a photo is required to run the algorithm and the number of generations. I included 2 images
(one of me collaging and another of a quiche I made) as photos you could easily use to run it. The
name of the photo is the first command line argument and the number of generations is the second.
Some example commands :

$ python3 g e n e t i c I m a g e. py q u i c h e. JPG 65
$ python3 g e n e t i c I m a g e. py c o l l a g e. JPG 85
It will print every fifth generation that it completes. One finished, it will save the image in the
same file with the name as the ImageNameNumberOfGenerationsgen.png. So the above examples
would be quiche65gen.png and collage85gen.png. It will take a few minutes to run the quiche.JPG
(about 7.5 minutes for 100 generation) and a little less time for the collage.JPG. I recommend running
them for at least 40 generations each to see the same of the objects, and then more generations to
really see the approximate colors.

# 3 Algorithm Function Details

- Fitness: The fitness function evaluates each of the pixels in an individual for the absolute
    valued difference between that pixel and the pixel of the target image. That is added to a total
    for all of the pixels. Because we want to try tomaximizefitness, this is subtracted from a very
    largest number and then used to determine the most fit individuals.
- Crossover: Two parents are randomly selected for the surviving set of individuals and then
    create an offspring by alternating a pixel from each parent that it gives the child. So for each
    offspring, the probability that that particular parent was chosen was^14 and, becuase order mat-
    ters, the probability that that particular second parent was chosen was^13. So any particular part
    of parents have a P( 121 ) of being chosen.
- Mutation: Each of the newly created offspring are then mutated such that for every pixel
    the difference between the target image pixel and the actual pixel is calculated. Then, either a
    -1 or 1 is randomly chosen. The new pixel value is equal to orginalPixelValue + (difference *
    MUTATIONPERCENT). The MUTATIONPERCENT can be changed at the top of the code–
    right now it is set to 0.5. This ensures that the pixel value will change by 50% of the difference
    from the target value. However, it is random whether the pixel is 50% better or worse than
    before. I also have the pixel values such that if it is above 255, it will take the mod of that
    value. This is also why extreme colors with either (or all) of the values are 0 or 255 are hard
    to achieve. I did this so even though a ”misstep” for the extreme values is not actually that
    detrimental. The mutation will occur on every pixel until the difference between the target pixel
    and the actual pixel is<0.000001.
