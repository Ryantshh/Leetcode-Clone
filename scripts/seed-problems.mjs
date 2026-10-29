// Seeds the problems collection from scripts/problems.json, built by build_problems.py.
// Usage: node --env-file=.env.local scripts/seed-problems.mjs [--admin you@example.com]
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import mongoose from "mongoose";

const problemsPath = fileURLToPath(new URL("./problems.json", import.meta.url));
const problems = JSON.parse(readFileSync(problemsPath, "utf-8"));

const adminFlagIndex = process.argv.indexOf("--admin");
const adminEmail = adminFlagIndex === -1 ? null : process.argv[adminFlagIndex + 1];

const { MONGODB_URI, DB_NAME } = process.env;
if (!MONGODB_URI) throw new Error("MONGODB_URI is not set");

await mongoose.connect(MONGODB_URI, { dbName: DB_NAME });
const db = mongoose.connection.db;

// The add-problem route numbers titles "N. Title"; match it so links and sorting stay consistent.
let nextIndex = (await db.collection("problems").countDocuments()) + 1;
const now = new Date();
let inserted = 0;

for (const problem of problems) {
  const escapedTitle = problem.title.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const isAlreadySeeded = await db
    .collection("problems")
    .findOne({ title: { $regex: `^\\d+\\. ${escapedTitle}$` } });
  if (isAlreadySeeded) continue;

  await db.collection("problems").insertOne({
    ...problem,
    title: `${nextIndex}. ${problem.title}`,
    like: 0,
    dislike: 0,
    similarQuestions: [],
    solutions: [],
    createdAt: now,
    updatedAt: now,
  });
  nextIndex++;
  inserted++;
}

if (adminEmail) {
  const result = await db
    .collection("users")
    .updateOne({ email: adminEmail }, { $set: { userType: "admin" } });
  if (result.matchedCount === 0) throw new Error(`No user with email ${adminEmail}`);
}

console.log(`seeded ${inserted} problem(s), skipped ${problems.length - inserted}`);
await mongoose.disconnect();
