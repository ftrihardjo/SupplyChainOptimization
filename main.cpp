#include <iostream>
#include <fstream>
#include <string>
#include <ctime>

enum LogLevel { INFO, WARNING, ERROR };

std::string getCurrentTime() {
    std::time_t now = std::time(nullptr);
    char buf[100];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
    return buf;
}

void logMessage(LogLevel level, const std::string& message) {
    std::ofstream logFile("log.txt", std::ios::app);
    if (!logFile) {
        std::cerr << "Unable to open log file.\n";
        return;
    }

    std::string levelStr;
    switch (level) {
        case INFO: levelStr = "INFO"; break;
        case WARNING: levelStr = "WARNING"; break;
        case ERROR: levelStr = "ERROR"; break;
    }

    logFile << "[" << getCurrentTime() << "] [" << levelStr << "] " << message << std::endl;
    logFile.close();

    std::cout << "Logged: [" << levelStr << "] " << message << std::endl;
}

int main() {
    while (true) {
        int level;
        std::string message;

        std::cout << "Enter log level (0=INFO, 1=WARNING, 2=ERROR, -1=EXIT): ";
        std::cin >> level;
        if (level == -1) break;

        std::cin.ignore(); // Ignore newline character left in the buffer
        std::cout << "Enter message: ";
        std::getline(std::cin, message);

        logMessage(static_cast<LogLevel>(level), message);
    }

    return 0;
}
