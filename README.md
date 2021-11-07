#  2d-Knapsack Shelf Optimisation

## Assumptions and Constraints
1. Maximum of two of each item.
1. "As full as possible" interpreted as maximum area of products on the display.
1. All products assumed to have equal height (set to be =1) for Question 1.
1. Overflowing interpreted as no products edges can extend beyond the width of the shelf 
(total width of products <= shelf width).
1. No spacing is needed between products.
1. Products cannot be placed on top of floating shelves.
1. Cannot rotate products.


## Optimisation Algorithm
In general, this code brute forces the problem to find an optimal solution (there can be multiple).

1. Generate permutations of valid quantities of each product. The N products can each take M values, 
therefore a loop of complexity O(M^N).
  
1. Iterates though these permutations:
    1. Check valid product layout with `total width of products <= shelf width`
    1. Check `total area of products > area of optimal best layout` 
    1. With floating shelves, a further nested loop to find valid spatial arrangements of products:
        
            e.g. ['A', 'A', 'B', 'C, 'C', 'D'] and ['A', B', 'C', 'C', 'D', 'A'] are different spatial permutations with the same number of each in product
       
       The complexity of this nested loop of permutations will be O(P!) where P is total number of products.

    1. Compute Intersection area between coordinates of products and floating shelves.
    1. If `intersection area > 0` for any pair, there is a product collision with floating shelf -- 
        that layout is invalid.
   
1. Store optimal valid layout (could store multiple solutions if desired.)


## Environment
- python=3.6.6
- No third party libraries

## Discussion
1. In general this is a type of packing/knapsack problem. This code performs a brute force search of all product setups within
the above constraints and assumptions. This is okay for simple problems, but it will get very slow with 
large numbers of products due to the Big-O complexity.

1. Spatial arrangement of products is not actually a problem for Q1, as there are no floating shelves to collide with.

1. The minimum of each item can be set (default `min_items=0`).

1. Although it is brute force the solution is not necessarily optimal because adding variable spacing
 between products is not considered. Running the same dimensions without floating shelves gives an upper bound (is this case, it is an optimal solution).

1. Some ideas for more scalable method:
    1. Greedy packing algorithm, rather than brute force.
    
    1. A genetic algorithm based method.
 
    1. Add more constraints to reduce the complexity of nested loops.

        e.g restrict possible spatial arrangements to those where 
    like-products are adjacent:

                e.g. ['A', 'A', 'B', 'C, 'C', 'D'] is valid but ['A', B', 'C', 'C', 'D', 'A'] is not

        and this can be reduce to

            from ['A', 'A', 'B', 'C, 'C', 'D'] to ['AA', B', 'CC', 'D']

        Which  reduces the number of spatial permutations (P!) significantly as P <= N (number of unique products) rather 
        than the total products on the shelf (P <= NM).
 
 
## Files
- `main.py`: Main script to run the code with product/shelf dimensions for Q1 and Q2.
- `shelf.py`: MainShelf and ItemWithBoundingBox classes to hold the basic attributes of ShelfA and bounding box dimensions of
 Product/Floating Shelves, respectively.
- `optimiser.py`: BruteForcePacking inherits MainShelf and adds the brute force optimisation of shelf layout.


