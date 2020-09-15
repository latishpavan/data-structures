import operator
from enum import IntEnum


class Orientation(IntEnum):
    POSITIVE = 1
    NEGATIVE = 0


class SplitDirection(IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y

    def __add__(self, other):
        return self.x + other.x, self.y + other.y

    def __le__(self, other):
        return self.x < other.x or self.y < other.y

    def __getitem__(self, item):
        return self.x if item == 0 else self.y

    def __repr__(self):
        return f'({self.x}, {self.y})'


class BoundingBox:
    def __init__(self, top_left: Point, bottom_right: Point, include_boundary: bool = False):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.include_boundary = include_boundary

    def is_inside(self, point: Point) -> bool:
        lb_func = operator.le if self.include_boundary else operator.lt
        up_func = operator.ge if self.include_boundary else operator.gt

        return lb_func(self.top_left.x, point.x) and up_func(self.bottom_right.x, point.x) \
            and lb_func(self.bottom_right.y, point.y) and up_func(self.top_left.y, point.y)

    def intersects_split_line(self, split_point: Point, split_dir: SplitDirection) -> bool:
        if split_dir == SplitDirection.VERTICAL:
            return self.bottom_right.y < split_point.y < self.top_left.y

        return self.top_left.x < split_point.x < self.bottom_right.x

    def orientation(self, point: Point, split_dir: SplitDirection) -> Orientation:
        if split_dir == SplitDirection.HORIZONTAL:
            return Orientation(self.bottom_right.x <= point.x)

        return Orientation(self.top_left.y <= point.y)


class TwoDimensionalTreeNode:
    def __init__(self, value: Point, left=None, right=None):
        self.value: Point = value
        self.left = left
        self.right = right

    def set_right_child(self, right):
        self.right = right

    def set_left_child(self, left):
        self.left = left


class TwoDimensionalTree(object):
    def __init__(self, root: TwoDimensionalTreeNode = None):
        self.k = 2
        self.root = root

    def _insert_helper(self, curr_node: TwoDimensionalTreeNode, new_node: TwoDimensionalTreeNode, level: int):
        curr_split = level % self.k

        if curr_node.value[curr_split] > new_node.value[curr_split]:
            if curr_node.left is None:
                curr_node.left = new_node
            else:
                self._insert_helper(curr_node.left, new_node, level + 1)
        else:
            if curr_node.right is None:
                curr_node.right = new_node
            else:
                self._insert_helper(curr_node.right, new_node, level + 1)

    def insert(self, point: Point):
        node = TwoDimensionalTreeNode(point)

        if self.root is None:
            self.root = node
        else:
            self._insert_helper(self.root, node, 0)

    def _range_search_helper(self, node: TwoDimensionalTreeNode, query_box: BoundingBox, level: int, res: list):
        if node is None:
            return

        # if inside append the point and search left and right subtrees
        if query_box.is_inside(node.value):
            res.append(node.value)
            self._range_search_helper(node.left, query_box, level + 1, res)
            self._range_search_helper(node.right, query_box, level + 1, res)

        # else check if split line intersects the bounding box
        else:
            split_direction = SplitDirection(level % self.k)

            if query_box.intersects_split_line(node.value, split_direction):
                self._range_search_helper(node.left, query_box, level + 1, res)
                self._range_search_helper(node.right, query_box, level + 1, res)
            else:
                if query_box.orientation(node.value, split_direction) == Orientation.POSITIVE:
                    self._range_search_helper(node.left, query_box, level + 1, res)
                else:
                    self._range_search_helper(node.right, query_box, level + 1, res)

    def range_search(self, query: BoundingBox) -> list:
        res = []
        self._range_search_helper(self.root, query, 0, res)
        return res


def main():
    points = [
        Point(10, 20),
        Point(25, 40),
        Point(1, 2),
        Point(85, 100),
        Point(0.9, 0.6)
    ]

    kd_tree = TwoDimensionalTree()
    for point in points:
        kd_tree.insert(point)

    bounding_box = BoundingBox(top_left=Point(0, 10), bottom_right=Point(10, 0))
    print(kd_tree.range_search(bounding_box))


if __name__ == '__main__':
    main()
