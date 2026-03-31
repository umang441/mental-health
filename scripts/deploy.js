import { network } from "hardhat";

async function main() {
  // Connect to the local Hardhat network or the one specified via --network
  const { viem } = await network.connect();
  
  console.log("🚀 Deploying MentalHealthRecords...");
  
  // Deploy the contract using Viem
  const contract = await viem.deployContract("MentalHealthRecords");
  
  console.log(`✅ MentalHealthRecords deployed to: ${contract.address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});