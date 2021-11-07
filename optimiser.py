import itertools

from shelf import MainShelf, ItemWithBoundingBox


class BruteForceShelfPacking(MainShelf):
    def __init__(self, max_width, max_items, min_items=0):
        super().__init__(max_width, max_items, min_items)

    def solve(self):
        self._optimise()
        self.report_optimal_layout()
        return self.optimal_layout

    def _optimise(self):
        # make iterables as list of valid quantities of each product
        # i.e  [[0, 1, ..., max_items], [0, 1, ..., max_items], for each product type]
        iterables = [[i for i in range(0, self.max_items + 1)] for _ in self.product_types]

        # The problematic nested loops of the brute force approach, first loop O(M^N)
        for product_count in itertools.product(*iterables):
            # place product_count[i] of each self.product_type[i] on the shelf
            current_product_list = self._place_n_products(product_count)
            self._validate_and_optimise_layout(current_product_list)

    def _place_n_products(self, product_count):
        # e.g. product_count of [2, 1, 2, 1] becomes product_list of ['A', 'A', 'B', 'C', 'C', 'D'] etc
        current_product_list = []
        for product_, n_products in zip(*(self.product_types, product_count)):
            current_product_list.extend([product_] * n_products)

        # add the remaining shelf space as a single movable spacing between products
        spacer_width = max(0, self.max_width - sum(i.width for i in current_product_list))
        if spacer_width:
            current_product_list.append(ItemWithBoundingBox('space', spacer_width, 0.))
        return current_product_list

    def _validate_and_optimise_layout(self, product_list):
        total_width = sum(i.width for i in product_list)
        total_area = sum(i.area for i in product_list)
        criterion = total_area

        is_layout_valid = [
            total_width <= self.max_width,
            criterion > self.optimal_criterion,
        ]

        if all(is_layout_valid):
            valid_permutation = self._find_valid_permutation(product_list)
            if valid_permutation is not None:
                self._update_layout(valid_permutation, criterion)

    def _find_valid_permutation(self, product_list):
        # iterate permutations with this current list of products on the shelf
        # O(P!) where P <= N*M
        for permuted_product_list in itertools.permutations(product_list):
            products_with_bounding_boxes = self._generate_bounding_boxes(permuted_product_list)
            n_collisions = self._number_of_collisions(products_with_bounding_boxes)
            if n_collisions == 0:
                return products_with_bounding_boxes
        return None

    @staticmethod
    def _generate_bounding_boxes(product_list):
        x_coord = 0.
        bounding_box_list = []
        for product_ in product_list:
            product_.place_at_xcoord(x_coord)
            bounding_box_list.append(product_.copy())
            x_coord += product_.width
        return bounding_box_list

    def _number_of_collisions(self, product_list):
        n_collisions = 0
        for product_, floating_shelf in itertools.product(product_list, self.floating_shelves):
            n_collisions += self._collision_found(product_.bounding_box, floating_shelf.bounding_box)
        return n_collisions

    @staticmethod
    def _collision_found(box_a, box_b):
        # Get coordinates of the intersection rectangle
        xa = max(box_a[0], box_b[0])
        ya = max(box_a[1], box_b[1])
        xb = min(box_a[2], box_b[2])
        yb = min(box_a[3], box_b[3])

        # compute the area of intersection area of boxes
        # collision if intersection area > 0.0
        intersection_area = max(0, xb - xa) * max(0, yb - ya)
        return int(intersection_area > 0)

    def _update_layout(self, product_layout, optimal_criterion):
        self.optimal_layout = product_layout
        self.optimal_criterion = optimal_criterion
