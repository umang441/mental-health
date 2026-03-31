import { network } from "hardhat";

async function main() {
  const CONTRACT_ADDRESS = '0x9fe46736679d2d9a65f0992f2272de9f3c7fa6e0';

  console.log("--- Blockchain Health Check ---");

  try {
    const { viem } = await network.connect();
    const [deployer] = await viem.getWalletClients();

    const contract = await viem.getContractAt(
      "MentalHealthRecords",
      CONTRACT_ADDRESS
    );

    console.log(`Target Contract: ${CONTRACT_ADDRESS}`);
    console.log(`Connected Account: ${deployer.account.address}`);

    const owner = await contract.read.owner();
    console.log(`Contract Owner: ${owner}`);

    // Check count for the deployer
    const count = await contract.read.getRecordCount([deployer.account.address]);
    console.log(`✅ Data Registry: Healthy`);
    console.log(`📊 Records found for YOUR account: ${count.toString()}`);

    if (deployer.account.address.toLowerCase() === owner.toLowerCase()) {
      const allUsers = await contract.read.getAllUsers();
      console.log(`📊 Global Unique Users: ${allUsers.length}`);
    }

    if (count > 0n) {
      console.log("\n🚀 STATUS: Blockchain is PROPERLY INTEGRATED and storing data.");
    } else {
      console.log("\n⚠️ STATUS: Blockchain is connected, but no records have been saved yet. Please use the frontend to store a result.");
    }

  } catch (error) {
    console.error("❌ ERROR: Could not connect to the contract.");
    console.error(error.message);
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
