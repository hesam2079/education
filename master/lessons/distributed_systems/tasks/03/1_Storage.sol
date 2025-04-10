// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract Storage {

    uint private favoriteNumber;

    function store(uint256 _num) public {
        favoriteNumber = _num;
    }

    /**
     * @dev Return value 
     * @return value of 'number'
     */
    function retrieve() public view returns (uint256){
        return favoriteNumber;
    }

    // define structure person with name and favoriteNumber
    struct Person {
        string name;
        uint favoriteNumber;

    }

    // private array - list of persons = people
    Person[] private people;

    // mapping 
    mapping(string => uint) private nameToFavoriteNumber;

    // function to add person in list of peoples
    function addPerson (string memory _name, uint _favoriteNumber) public {
        people.push(Person(_name, _favoriteNumber));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    // function to get person by index in list of people
    function getPersonByIndex(uint _index) public view returns (uint, string memory) {
        return (people[_index].favoriteNumber , people[_index].name);
    }

    // function to get person using mapping
    function getFavoriteNumberByMapping(string memory _name) public view returns (uint) {
        return(nameToFavoriteNumber[_name]);
    }
}