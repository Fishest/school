/**
 * compile with:
 * g++ -std=c++11 solver.cc -o solver
 */
#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>

/**
 * A simple poco that is used to hold the settings for
 * each item.
 */
struct Item {
    int weight;
    int value;
};

#define WEIGHT 100000
//#define WEIGHT 1000000
static int lookup[WEIGHT] = { 0 };

/**
 *
 */
void dynamic_quick_solution(int capacity, const std::vector<Item>& items) {
    const int count = items.size() + 1;
    // vector<vector<int>> -> when the value changes, add that capacity to
    // the keep list

    for (int index = 1; index < count; ++index) {
        for (int weight = capacity; weight >= 0; --weight) {
            Item item = items[index - 1];
            if (item.weight <= weight) {
                int possible = item.value + lookup[weight - item.weight];
                lookup[weight] = std::max(lookup[weight], possible);
            }
        }
    }

    int weight = capacity;
    int value  = lookup[weight];

    std::cout << "starting the item lookup: " << value << std::endl;
}

/**
 *
 */
std::vector<Item> read_items(const std::string& filename) {
    int weight, value, capacity = -1, item_count = -1;
    std::vector<Item> items;

    std::ifstream stream(filename);
    stream >> item_count >> capacity;

    while (stream >> value >> weight) {
        items.push_back({ value, weight });
    }

    return std::move(items);
}

/**
 *
 */
void print_items(const std::vector<Item> items) {
    for (auto item : items) {
        std::cout << "weight " << item.weight << " value " << item.value << std::endl;
    }
    std::cout << "total items: " << items.size() << std::endl;
}

int main(int argc, char** argv) {
    int capacity = WEIGHT;
    std::vector<Item> items = read_items("data/ks_40_0");
    //std::vector<Item> items = read_items("data/ks_10000_0");
    //print_items(items);
    dynamic_quick_solution(capacity, items);
}
