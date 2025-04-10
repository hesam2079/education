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

    // تست ایجاد انتخابات
    function testCreateElection() public {
        string;
        candidates[0] = "کاندیدا 1";
        candidates[1] = "کاندیدا 2";
        candidates[2] = "کاندیدا 3";

        uint startTime = 1672531200;
        uint endTime = 1672617600;

        // انتظار داریم که ایونت ElectionCreated با آرگومان‌های مشخص صادر شود
        vm.expectEmit(true, true, true, true);
        emit ElectionCreated(1, "انتخابات ریاست جمهوری", startTime, endTime, candidates);

        // فراخوانی تابع ایجاد رای گیری
        votingSystem.createElection("انتخابات ریاست جمهوری", startTime, endTime, candidates);
        
        // حالا بررسی اینکه اطلاعات انتخابات درست ذخیره شده است
        (string memory name, uint start, uint end, string[] memory storedCandidates) = votingSystem.elections(1);

        Assert.equal(name, "انتخابات ریاست جمهوری", "Election name should be correct");
        Assert.equal(start, startTime, "Start time should be correct");
        Assert.equal(end, endTime, "End time should be correct");

        // بررسی کاندیداها
        Assert.equal(storedCandidates[0], "کاندیدا 1", "First candidate should be correct");
        Assert.equal(storedCandidates[1], "کاندیدا 2", "Second candidate should be correct");
        Assert.equal(storedCandidates[2], "کاندیدا 3", "Third candidate should be correct");
    }
}
