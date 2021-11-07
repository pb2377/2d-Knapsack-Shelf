class ItemWithBoundingBox:
    def __init__(self, name, width, height, x_min=0., y_min=0.):
        self.name = name
        self.width = width
        self.height = height
        self.area = height * width
        self.y_min = y_min
        self.bounding_box = (x_min, y_min, x_min + width, y_min + height)

    def place_at_xcoord(self, x_min):
        x_max = x_min + self.width
        self.bounding_box = (x_min, self.y_min, x_max, self.y_min + self.height)

    def copy(self):
        return ItemWithBoundingBox(self.name, self.width, self.height, self.bounding_box[0], self.bounding_box[1])


class MainShelf:
    def __init__(self, max_width, max_items, min_items=0):
        self.max_width = max_width
        self.optimal_layout = []
        self.optimal_criterion = 0.
        self.max_items = max_items
        self.min_items = min_items
        self.product_types = []
        self.floating_shelves = []

    def add_product(self, name, width, height):
        assert name not in [p.name for p in self.product_types]
        self.product_types.append(ItemWithBoundingBox(name, width, height))

    def add_floating_shelf(self, name, width, height, x_min, y_min):
        assert name not in [sh.name for sh in self.floating_shelves]
        self.floating_shelves.append(ItemWithBoundingBox(name, width, height, x_min, y_min))

    def clear_shelves(self):
        self.__init__(self.max_width, self.max_items, self.min_items)

    def report_optimal_layout(self):
        print('Optimal Layout =', [product_.name for product_ in self.optimal_layout])
        print('Product Bottoms Corner Locations along Shelf_width (x1, x2) =', self._dimensions_on_shelf())
        print('Total Area =', sum(product_.area for product_ in self.optimal_layout))

    def _dimensions_on_shelf(self):
        dimensions_on_shelf = []
        for product_ in self.optimal_layout:
            x_min, y_min, x_max, y_max = product_.bounding_box
            dimensions_on_shelf.append((x_min, x_max))
        return dimensions_on_shelf
