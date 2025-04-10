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

    // تست ارسال رای برای کاندیداهای مختلف
    function testSubmitVotes() public {
        // ایجاد انتخابات
        string;
        candidates[0] = "کاندیدا 1";
        candidates[1] = "کاندیدا 2";

        uint startTime = 1672531200;
        uint endTime = 1672617600;
        
        // ایجاد رای گیری
        votingSystem.createElection("انتخابات ریاست جمهوری", startTime, endTime, candidates);

        // ایجاد هش‌های اثبات منحصر به فرد
        bytes32 proofHash1 = keccak256(abi.encodePacked("proof1"));
        bytes32 proofHash2 = keccak256(abi.encodePacked("proof2"));

        // ارسال رای برای کاندیداها
        votingSystem.submitVote(1, "کاندیدا 1", proofHash1);
        votingSystem.submitVote(1, "کاندیدا 2", proofHash2);

        // چک کردن آرا
        uint votesForCandidate1 = votingSystem.getVotes(1, "کاندیدا 1");
        uint votesForCandidate2 = votingSystem.getVotes(1, "کاندیدا 2");

        Assert.equal(votesForCandidate1, 1, "The vote count for candidate 1 should be 1");
        Assert.equal(votesForCandidate2, 1, "The vote count for candidate 2 should be 1");

        // ارسال رای با هش تکراری (باید ارور بده)
        try votingSystem.submitVote(1, "کاندیدا 1", proofHash1) {
            Assert.ok(false, "Should not be able to vote with the same proofHash again");
        } catch (bytes memory) {
            // صحیح است که ارور داده می‌شود
        }
    }
}
