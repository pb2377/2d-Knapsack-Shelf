import sys

from optimiser import BruteForceShelfPacking

print(sys.version)


def main():
    min_items = 0
    max_items = 2

    # Example 1
    print('\n{0} Q1 {0}'.format('-' * 20))

    # Shelf Dimensions
    shelf_a_width = 7

    shelf_packer = BruteForceShelfPacking(max_width=shelf_a_width, max_items=max_items, min_items=min_items)

    # Product Dimensions
    product_names = ['A', 'B', 'C', 'D']
    product_widths = [1., 1.5, 2., 0.7]
    product_heights = [1., 1., 1., 1.]

    # list of products that can be placed on the shelf
    for name, width, height in zip(*(product_names, product_widths, product_heights)):
        shelf_packer.add_product(name, width, height)

    shelf_packer.solve()

    # Example 2: Adds a floating shelf to avoid collision with.
    print('\n{0} Q2 {0}'.format('-' * 20))
    # reset the shelf, clear of products and floating shelves
    shelf_packer.clear_shelves()

    product_heights = [2., 2., 2., 1.]

    # list of products that can be placed on the shelf, regenerate these.
    for name, width, height in zip(*(product_names, product_widths, product_heights)):
        shelf_packer.add_product(name, width, height)

    # Floating shelf
    shelf_x = product_widths[0] * 1.5  # = 1.5 * A_width
    shelf_y = product_heights[0] * 3. / 4  # = 3/4 * A_height
    shelf_width = product_widths[0]  # = A_width
    shelf_height = 1.  # value to give it thickenss above shelf_b_y
    shelf_packer.add_floating_shelf('floating_shelf', shelf_width, shelf_height, shelf_x, shelf_y)

    shelf_packer.solve()


if __name__ == '__main__':
    main()
