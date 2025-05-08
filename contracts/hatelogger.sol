
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HateLogger {
    event HateLogged(string hash, uint8 target, uint256 confidence, string timestamp);

    struct LogEntry {
        string hash;
        uint8 target;
        uint256 confidence;
        string timestamp;
    }

    LogEntry[] public logs;

    function logHate(
        string memory hash,
        uint8 target,
        uint256 confidence,
        string memory timestamp
    ) public {
        logs.push(LogEntry(hash, target, confidence, timestamp));
        emit HateLogged(hash, target, confidence, timestamp);
    }

    function getLogs() public view returns (LogEntry[] memory) {
        return logs;
    }
}
