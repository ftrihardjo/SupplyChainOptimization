#include <iostream>
#include <stdexcept>
#include <vector>
#include <cmath>

// Objective function: Placeholder function for optimization
double objectiveFunction(double x, double cost) {
    return x * cost; // Placeholder function
}

// Function to find the minimum of the objective function
double optimizeSupplyChain(double demand, double cost, double capacity) {
    double step = 0.01;
    double bestX = 0;
    double bestValue = objectiveFunction(0, cost);
    
    for (double x = 0; x <= demand; x += step) {
        if (x > capacity) break;
        double currentValue = objectiveFunction(x, cost);
        if (currentValue < bestValue) {
            bestValue = currentValue;
            bestX = x;
        }
    }
    
    return bestX;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <demand> <cost> <capacity>" << std::endl;
        return 1;
    }

    try {
        double demand = std::stod(argv[1]);
        double cost = std::stod(argv[2]);
        double capacity = std::stod(argv[3]);

        double optimalSolution = optimizeSupplyChain(demand, cost, capacity);
        std::cout << "Optimal Solution: " << optimalSolution << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cerr << "Invalid argument: " << e.what() << std::endl;
        return 1;
    } catch (const std::out_of_range& e) {
        std::cerr << "Argument out of range: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
