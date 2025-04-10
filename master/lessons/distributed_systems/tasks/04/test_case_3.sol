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

    // تست رد هش‌های اثبات تکراری
    function testDuplicateProofHashRejection() public {
        // ایجاد انتخابات
        string;
        candidates[0] = "کاندیدا 1";
        candidates[1] = "کاندیدا 2";

        uint startTime = 1672531200;
        uint endTime = 1672617600;
        
        // ایجاد رای گیری
        votingSystem.createElection("انتخابات ریاست جمهوری", startTime, endTime, candidates);

        // ایجاد یک هش اثبات منحصر به فرد
        bytes32 proofHash = keccak256(abi.encodePacked("uniqueProofHash"));

        // ارسال رای برای کاندیدا 1
        votingSystem.submitVote(1, "کاندیدا 1", proofHash);

        // چک کردن آرا برای کاندیدا 1
        uint votesForCandidate1 = votingSystem.getVotes(1, "کاندیدا 1");
        Assert.equal(votesForCandidate1, 1, "The vote count for candidate 1 should be 1");

        // تلاش برای ارسال رای با همان proofHash (باید رد بشه)
        try votingSystem.submitVote(1, "کاندیدا 2", proofHash) {
            Assert.ok(false, "Should not be able to vote with the same proofHash again");
        } catch (bytes memory) {
            // ارور صحیح است که دریافت شود
        }

        // چک کردن آرا برای کاندیدا 2 باید همچنان 0 باشد
        uint votesForCandidate2 = votingSystem.getVotes(1, "کاندیدا 2");
        Assert.equal(votesForCandidate2, 0, "The vote count for candidate 2 should still be 0");
    }
}
