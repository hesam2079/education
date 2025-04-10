// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingSystemWithZKP{
    address public admin;
    uint public electionId;

        // structure should has name
        // start and end time
        // is the election active or not
        // string for condidates
        struct Election {
            string name;
            uint startTime;
            uint endTime;
            bool isActive;
            uint number_of_condidates;
            string[] condidates;
            bool resultDeclerate;
            mapping(string => uint) votes;
            mapping(bytes32 => bool) proofHashes;
    }

    // also we need a mapping for handeling electionId
    mapping(uint => Election) public elections;

    // create events to publish election created and vote submission
    event ElectionCreated(string name, uint startTime, uint endTime, string[] candidates);
    event VoteSubmitted(uint electionId, address voter, string candidate, bytes32 proofHash);
    event ElectionResults(uint electionId, string winner, uint winningVoteCount);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier electionExists(uint _electionId) {
        require(bytes(elections[_electionId].name).length > 0, "Election does not exist");
        _;
    }

    modifier electionOngoing(uint _electionId) {
        require(block.timestamp >= elections[_electionId].startTime && block.timestamp <= elections[_electionId].endTime, "Election is not ongoing");
        _;
    }

    constructor() {
        admin = msg.sender; // a person whe create new election is admin
    }

    // function should be public because every body in the network can create election
    function createElection( string memory _name, uint _startTime, uint _endTime, string[] memory _condidates) public onlyAdmin{
        electionId++;
        Election storage newElection = elections[electionId];
        newElection.name = _name;
        newElection.startTime = _startTime;
        newElection.endTime = _endTime;
        newElection.isActive = true;
        newElection.condidates = _condidates;
        newElection.resultDeclerate = false;
        newElection.number_of_condidates = _condidates.length;


        emit ElectionCreated(electionId, _name, _startTime, _endTime, _condidates);
    }

    event ElectionCreated(uint electionId, string name, uint startTime, uint _endTime, string[] condidates);

    // we should to create next function to submit votes
    // check the election is exists and Ongoing
    function submitvote(uint _electionId, string memory _condidate, bytes32 _proofHash) public electionExists(_electionId) electionOngoing(_electionId){
        Election storage election = elections[_electionId];

        // check the proof hash not be used before
        require(!election.proofHashes[_proofHash], "this proof hash is already been used.");

        // check the condidate exists or not
        bool condidateExists = false;
        for (uint i = 0; i < election.number_of_condidates; i++){
            if (keccak256(abi.encodePacked(election.condidates[i])) == keccak256(abi.encodePacked(_condidate))) {
                condidateExists = true;
                break;
            }
        }
        
        require(condidateExists, "invalid condidate");

        election.proofHashes[_proofHash] = true;

        election.votes[_condidate]++;
    }

    // next function is to declare results
    function declareResluts(uint _electionId) public onlyAdmin {
        Election storage election = elections[_electionId];

        // check the requirements of election ended
        require(block.timestamp > election.endTime, "Election has not ended yet");
        require(msg.sender == admin, "only admin can declare the results");
        
        uint winningVoteCount = 0;
        string memory winner = "";

        for (uint i = 0; i < election.number_of_condidates; i++) {
            string memory candidate = election.condidates[i];
            uint voteCount = election.votes[candidate];
        
            if (voteCount > winningVoteCount) {
                winningVoteCount = voteCount;
                winner = candidate;
            }
    }
        election.isActive = false;
        election.resultDeclerate = true;

        emit ElectionResults(_electionId, winner, winningVoteCount);

    }

    function getVots(uint _electionId, string memory _condidate) public view electionExists(_electionId) returns (uint){
        return elections[_electionId].votes[_condidate];
    }

    function getCondidates(uint _electionId) public view electionExists(_electionId) returns (string[] memory) {
        return elections[_electionId].condidates;
    }

    function isProofUsed(uint _electionId, bytes32 _proofHash) public view electionExists(_electionId) returns (bool) {
        Election storage election = elections[_electionId];
        return election.proofHashes[_proofHash];
    }

}