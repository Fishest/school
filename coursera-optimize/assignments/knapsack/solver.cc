/**
 * compile with:
 * g++ -std=c++11 O3 solver.cc -o solver
 */
#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>

/**
 * A simple poco that is used to hold the settings for
 * each item.
 *
 * @param weight The weight of this item
 * @param value The value of this item
 */
struct Item {
    int weight;
    int value;
};

/**
 * @summary This implements a quick dp algorithm for the supplied items
 * @param capacity The capacity that we would like to fill
 * @param items The items to fill the knapsack with
 */
void dynamic_quick_solution(const int capacity, const std::vector<Item>& items) {
    const int count = items.size() + 1;
    std::vector<int> lookup(capacity, 0);
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
 * @summary Read the supplied header from the given file
 * @param filename The file to read the items from
 * @return A tuple of (capacity, item_count)
 */
std::tuple<int, int> read_header(const std::string& filename) {
    int capacity = -1, item_count = -1;

    std::ifstream stream(filename);
    stream >> item_count >> capacity;

    return std::make_tuple(capacity, item_count);
}

/**
 * @summary Read the supplied items from the given file
 * @param filename The file to read the items from
 * @return A vector of the items read from disk
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
 * @summary Print a listing of the supplied items
 * @param items The items to print out
 */
void print_items(const std::vector<Item> items) {
    for (auto item : items) {
        std::cout << "weight " << item.weight << " value " << item.value << std::endl;
    }
    std::cout << "total items: " << items.size() << std::endl;
}

/**
 * @summary Print a listing of the supplied items
 * @param items The items to print out
 */
int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "usage: ./" << argv[0] << " <filename>" << std::endl;
        return -1;
    }

    auto config = read_header(argv[1]);
    auto items  = read_items(argv[1]);
    //print_items(items);
    dynamic_quick_solution(std::get<0>(config), items);
}
