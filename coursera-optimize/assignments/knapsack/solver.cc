#include <iostream>
#include <vector>
#include <algorithm>

struct Item {
    int weight;
    int value;
};

void dynamic_solution(int capacity, const std::vector<Item>& items) {
    const int count = items.size() + 1;
    int lookup[10][5] = { 0 };
    // int lookup[capacity][count] = { 0 };

    for (int index = 1; index < count; ++index) {
        for (int weight = 0; weight <= capacity; ++weight) {
            lookup[weight][index] = lookup[weight][index - 1];
            Item item = items.at(index - 1);
            if (item.weight <= weight) {
                int possible = item.value + lookup[weight - item.weight][index - 1];
                lookup[weight][index] = std::max(lookup[weight][index], possible);
            }
        }
    }

    int weight = capacity;
    int value  = lookup[weight][count - 1];
    int selected[5] = { 0 };
    std::cout << value << std::endl;

    for (int index = count - 1; index > 0; --index) {
        if (lookup[weight][index] != lookup[weight][index - 1]) {
            std::cout << 1 << " ";
            selected[index - 1] = 1;
            weight -= items.at(index - 1).weight;
        } else {
            std::cout << 0 << " ";
        }
    }
    std::cout << std::endl;

}

int main(int argc, char** argv) {
    int capacity = 9;
    std::vector<Item> items {{4, 5}, {5, 6}, {2, 3}};
    dynamic_solution(capacity, items);
}
