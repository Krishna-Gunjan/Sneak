#include <iostream>
#include <vector>
#include <random>
#include <ctime>
#include <queue>
#include <set>
#include <unordered_set>
#include <tuple>
#include <pybind11/pybind11.h> // Pybind11 to connect with Python

namespace py = pybind11;

class MapGenerator {
public:
    MapGenerator(int width = 68, int height = 15, int seekers = 15, int collectibles = 5)
        : width(width), height(height), seekers(seekers), collectibles(collectibles) {
        map.resize(height, std::vector<char>(width, '#'));
    }

    void generateMap() {
        std::cout << "Generating map..." << std::endl;
        while (true) {
            map.assign(height, std::vector<char>(width, '#'));

            // Randomly place empty spaces
            for (int y = 1; y < height - 1; y++) {
                for (int x = 1; x < width - 1; x++) {
                    if (randomChance(0.6)) {
                        map[y][x] = ' ';
                    }
                }
            }

            // Place start and end positions
            std::pair<int, int> start = {1, 1};
            std::pair<int, int> end = {width - 2, height - 2};
            map[start.second][start.first] = 'S';
            map[end.second][end.first] = 'E';

            // Place seekers with a time limit
            start_time = std::time(nullptr);
            int placed_seekers = 0;
            while (placed_seekers < seekers && (std::time(nullptr) - start_time) < 5) {
                if (placeSeekers()) {
                    placed_seekers++;
                }
            }

            // Place collectibles
            for (int i = 0; i < collectibles; i++) {
                placeCollectibles();
            }

            // Ensure the map is clearable
            if (isMapClearable(start, end, getAssetPositions())) {
                break;
            }
        }
    }

    void printMap() const {
        for (const auto& row : map) {
            for (const auto& cell : row) {
                std::cout << cell;
            }
            std::cout << std::endl;
        }
    }

private:
    int width, height, seekers, collectibles;
    std::time_t start_time;
    std::vector<std::vector<char>> map;

    bool randomChance(double probability) {
        return (static_cast<double>(std::rand()) / RAND_MAX) < probability;
    }

    bool placeSeekers() {
        std::time_t current_time = std::time(nullptr);
        if (current_time - start_time > 5) {
            std::cout << "Time limit exceeded for placing seekers." << std::endl;
            return false;
        }

        while (true) {
            int x = rand() % (width - 2) + 1;
            int y = rand() % (height - 2) + 1;
            if (map[y][x] == ' ' && isBetweenClosedWalls(x, y) && seekersInVicinity(x, y)) {
                map[y][x] = '$';
                std::cout << "Seeker placed at (" << x << ", " << y << ")." << std::endl;
                return true;
            }
        }
        return false;
    }

    void placeCollectibles() {
        while (true) {
            int x = rand() % (width - 2) + 1;
            int y = rand() % (height - 2) + 1;
            if (map[y][x] == ' ') {
                map[y][x] = 'C';
                std::cout << "Collectible placed at (" << x << ", " << y << ")." << std::endl;
                return;
            }
        }
    }

    bool isBetweenClosedWalls(int x, int y) {
        int k = 1, l = 1;

        while (map[y][x - k] != '#') {
            if (map[y][x - k] == '$') return false;
            k++;
        }

        while (map[y][x + l] != '#') {
            if (map[y][x + l] == '$') return false;
            l++;
        }

        return (k > 4 || l > 4);
    }

    bool seekersInVicinity(int x, int y) {
        for (int i = std::max(0, x - 2); i <= std::min(width - 1, x + 2); i++) {
            for (int j = std::max(0, y - 2); j <= std::min(height - 1, y + 2); j++) {
                if (map[j][i] == '$' && (i != x || j != y)) {
                    return false;
                }
            }
        }
        return true;
    }

    std::vector<std::pair<int, int>> getAssetPositions() const {
        std::vector<std::pair<int, int>> assets;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (map[y][x] == '$' || map[y][x] == 'C') {
                    assets.push_back({x, y});
                }
            }
        }
        return assets;
    }

    bool isMapClearable(std::pair<int, int> start, std::pair<int, int> end, std::vector<std::pair<int, int>> assets) {
        return bfs(start, std::unordered_set<std::pair<int, int>>(assets.begin(), assets.end(), {end}));
    }

    bool bfs(std::pair<int, int> start, std::unordered_set<std::pair<int, int>> goals) {
        std::queue<std::pair<int, int>> queue;
        std::set<std::pair<int, int>> visited;
        std::set<std::pair<int, int>> found;

        queue.push(start);

        while (!queue.empty()) {
            auto [x, y] = queue.front();
            queue.pop();

            if (goals.find({x, y}) != goals.end()) {
                found.insert({x, y});
            }

            if (found.size() == goals.size()) {
                return true;
            }

            if (visited.find({x, y}) == visited.end()) {
                visited.insert({x, y});
                for (auto [dx, dy] : std::vector<std::pair<int, int>>{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}) {
                    int nx = x + dx, ny = y + dy;
                    if (nx >= 0 && nx < width && ny >= 0 && ny < height && map[ny][nx] != '#' && visited.find({nx, ny}) == visited.end()) {
                        queue.push({nx, ny});
                    }
                }
            }
        }

        return false;
    }
};

// Bindings for Python integration
PYBIND11_MODULE(generator, m) {
    py::class_<MapGenerator>(m, "MapGenerator")
        .def(py::init<int, int, int, int>())
        .def("generateMap", &MapGenerator::generateMap)
        .def("printMap", &MapGenerator::printMap);
}

