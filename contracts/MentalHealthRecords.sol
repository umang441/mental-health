// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MentalHealthRecords
 * @dev This contract stores mental health prediction references (IPFS hashes) for users.
 * It follows the Ownable pattern for admin-level access control.
 */
contract MentalHealthRecords is Ownable {

    /// @dev Structure to store each mental health record reference
    struct Record {
        address user;        // Address of the patient/user
        string ipfsHash;     // Off-chain data reference hash
        uint256 prediction;  // Prediction outcome (0: Normal, 1: Anxiety/Depression)
        uint256 timestamp;   // Time when record was added
    }

    /// @dev Mapping from user address to their collection of records
    mapping(address => Record[]) private userRecords;

    /// @dev Array of all unique users for admin reporting/analytics
    address[] private allUsers;

    /// @dev Mapping to track if a user has already been added to the allUsers array
    mapping(address => bool) private hasAccount;

    /// @dev Event emitted when a new record is added
    event RecordAdded(
        address indexed user,
        string ipfsHash,
        uint256 prediction,
        uint256 timestamp
    );

    /// @dev Event emitted when a record is deleted
    event RecordDeleted(address indexed user, uint256 index, uint256 timestamp);

    /**
     * @dev Constructor that initializes the contract with the deployer as the owner.
     */
    constructor() Ownable(msg.sender) {}

    /**
     * @notice Adds a new mental health record.
     * @param _ipfsHash The IPFS hash pointing to off-chain encrypted data.
     * @param _prediction The prediction outcome (0 or 1).
     * @dev Validates that the IPFS hash is not empty.
     */
    function addRecord(string memory _ipfsHash, uint256 _prediction) public {
        require(bytes(_ipfsHash).length > 0, "IPFS hash cannot be empty");
        
        // Create the new record
        Record memory newRecord = Record({
            user: msg.sender,
            ipfsHash: _ipfsHash,
            prediction: _prediction,
            timestamp: block.timestamp
        });

        // Store the record
        userRecords[msg.sender].push(newRecord);

        // Add user to unique list if they haven't been added before
        if (!hasAccount[msg.sender]) {
            allUsers.push(msg.sender);
            hasAccount[msg.sender] = true;
        }

        // Emit the event
        emit RecordAdded(msg.sender, _ipfsHash, _prediction, block.timestamp);
    }

    /**
     * @notice Returns all records belonging to the caller.
     * @return Array of Records for the msg.sender.
     */
    function getMyRecords() public view returns (Record[] memory) {
        return userRecords[msg.sender];
    }

    /**
     * @notice Returns records of a specific user.
     * @param _user The address of the user to fetch records for.
     * @return Array of Records for the specified user.
     * @dev Restricted to the contract owner (admin).
     */
    function getUserRecords(address _user) public view onlyOwner returns (Record[] memory) {
        return userRecords[_user];
    }

    /**
     * @notice Returns a list of all users who have stored records.
     * @return Array of user addresses.
     * @dev Restricted to the contract owner (admin).
     */
    function getAllUsers() public view onlyOwner returns (address[] memory) {
        return allUsers;
    }

    /**
     * @notice Bonus: Deletes a specific record of a user.
     * @param _index The index of the record to delete.
     * @dev Only the record owner or the contract owner can delete records.
     * Uses the pattern of swapping with last element then popping to minimize gas cost.
     */
    function deleteRecord(address _user, uint256 _index) public {
        require(
            msg.sender == _user || msg.sender == owner(),
            "Not authorized to delete this record"
        );
        require(_index < userRecords[_user].length, "Index out of bounds");

        // Swap with the last element and pop to save gas
        uint256 lastIndex = userRecords[_user].length - 1;
        if (_index != lastIndex) {
            userRecords[_user][_index] = userRecords[_user][lastIndex];
        }
        userRecords[_user].pop();

        emit RecordDeleted(_user, _index, block.timestamp);
    }

    /**
     * @notice Bonus: Returns the total number of records for a user.
     * @param _user The address of the user.
     * @return The count of records.
     */
    function getRecordCount(address _user) public view returns (uint256) {
        return userRecords[_user].length;
    }
}
