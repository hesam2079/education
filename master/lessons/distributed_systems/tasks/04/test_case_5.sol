// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "remix_tests.sol"; // برای تست‌های Remix
import "../VotingSystem.sol"; // آدرس قرارداد شما

contract TestVotingSystem {
    VotingSystem votingSystem;
    address admin;

    // قبل از هر تست، قرارداد را استقرار می‌دهیم
    function beforeAll() public {
        votingSystem = new VotingSystem();
        admin = address(this); // اینجا ادمین همان خود ما هستیم
    }

    // تست پرس و جو از تعداد آرا برای هر کاندیدا
    function testQueryVotesForCandidates() public {
        // ایجاد انتخابات
        string;
        candidates[0] = "کاندیدا 1";
        candidates[1] = "کاندیدا 2";

        uint startTime = 1672531200; // 2023-01-01 00:00:00
        uint endTime = 1672617600;   // 2023-01-02 00:00:00
        
        // ایجاد رای گیری
        votingSystem.createElection("انتخابات ریاست جمهوری", startTime, endTime, candidates);

        // ارسال رای‌ها برای کاندیداها
        bytes32 proofHash1 = keccak256(abi.encodePacked("proofHash1"));
        bytes32 proofHash2 = keccak256(abi.encodePacked("proofHash2"));

        votingSystem.submitVote(1, "کاندیدا 1", proofHash1);
        votingSystem.submitVote(1, "کاندیدا 1", proofHash2);

        bytes32 proofHash3 = keccak256(abi.encodePacked("proofHash3"));
        votingSystem.submitVote(1, "کاندیدا 2", proofHash3);

        // چک کردن تعداد آرا برای هر کاندیدا
        uint votesForCandidate1 = votingSystem.getVotes(1, "کاندیدا 1");
        uint votesForCandidate2 = votingSystem.getVotes(1, "کاندیدا 2");

        // بررسی اینکه تعداد آرا درست باشد
        Assert.equal(votesForCandidate1, 2, "کاندیدا 1 باید 2 رای داشته باشد");
        Assert.equal(votesForCandidate2, 1, "کاندیدا 2 باید 1 رای داشته باشد");
    }
}
