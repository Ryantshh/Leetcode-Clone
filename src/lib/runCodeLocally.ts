import { spawn } from "node:child_process";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Drop-in replacement for runJudge0Batch that compiles and runs code on this
// machine. Returns the Judge0 submission shape the routes and UI already read:
// status.description, stdout, compile_output, time, memory.
// Runs submitted code unsandboxed as the current user - local single-user only.

type TestCase = { input: string; output: string };

type JudgeStatus = { id: number; description: string };

export type LocalRunResult = {
    status: JudgeStatus;
    stdout: string | null;
    stderr: string | null;
    compile_output: string | null;
    time: string;
    memory: number;
};

type LanguageSpec = {
    fileName: string;
    compileArgs?: [string, string[]];
    runArgs: [string, string[]];
};

const COMPILE_TIMEOUT_MS = 20000;
const RUN_TIMEOUT_MS = 6000;

// Judge0 status ids, kept so existing checks against the descriptions still pass.
const ACCEPTED: JudgeStatus = { id: 3, description: "Accepted" };
const WRONG_ANSWER: JudgeStatus = { id: 4, description: "Wrong Answer" };
const TIME_LIMIT_EXCEEDED: JudgeStatus = { id: 5, description: "Time Limit Exceeded" };
const COMPILATION_ERROR: JudgeStatus = { id: 6, description: "Compilation Error" };
const RUNTIME_ERROR: JudgeStatus = { id: 11, description: "Runtime Error (NZEC)" };

const binaryName = process.platform === "win32" ? "main.exe" : "main";
const pythonCommand = process.platform === "win32" ? "python" : "python3";

// Keyed by the Judge0 language ids the editor sends (see ProblemPageCodeEditor).
const LANGUAGES: Record<number, LanguageSpec> = {
    50: {
        fileName: "main.c",
        compileArgs: ["gcc", ["main.c", "-o", binaryName, "-lm"]],
        runArgs: [`./${binaryName}`, []],
    },
    54: {
        fileName: "main.cpp",
        compileArgs: ["g++", ["main.cpp", "-o", binaryName, "-std=c++17"]],
        runArgs: [`./${binaryName}`, []],
    },
    62: {
        fileName: "Main.java",
        compileArgs: ["javac", ["Main.java"]],
        runArgs: ["java", ["Main"]],
    },
    71: { fileName: "main.py", runArgs: [pythonCommand, ["main.py"]] },
    93: { fileName: "main.js", runArgs: ["node", ["main.js"]] },
};

type ProcessOutcome = {
    stdout: string;
    stderr: string;
    exitCode: number | null;
    isTimedOut: boolean;
    durationMs: number;
    missingCommand: string | null;
};

const runProcess = (
    command: string,
    args: string[],
    workingDir: string,
    timeoutMs: number,
    stdinText?: string
): Promise<ProcessOutcome> =>
    new Promise((resolve) => {
        const startedAt = Date.now();
        // A relative ./main.exe is resolved against process.cwd(), not the child cwd.
        const resolvedCommand = command.startsWith("./") ? join(workingDir, command.slice(2)) : command;
        const child = spawn(resolvedCommand, args, { cwd: workingDir });

        let stdout = "";
        let stderr = "";
        let isTimedOut = false;
        let missingCommand: string | null = null;

        const timer = setTimeout(() => {
            isTimedOut = true;
            child.kill("SIGKILL");
        }, timeoutMs);

        child.stdout.on("data", (chunk) => {
            stdout += chunk.toString();
        });
        child.stderr.on("data", (chunk) => {
            stderr += chunk.toString();
        });

        child.on("error", (error: NodeJS.ErrnoException) => {
            if (error.code === "ENOENT") missingCommand = command;
            else stderr += error.message;
        });

        child.on("close", (exitCode) => {
            clearTimeout(timer);
            resolve({ stdout, stderr, exitCode, isTimedOut, durationMs: Date.now() - startedAt, missingCommand });
        });

        child.stdin.on("error", () => {
            // A program that exits without reading stdin closes the pipe first.
        });
        if (stdinText !== undefined) child.stdin.write(stdinText.endsWith("\n") ? stdinText : `${stdinText}\n`);
        child.stdin.end();
    });

const normalizeOutput = (text: string): string =>
    text
        .replace(/\r\n/g, "\n")
        .split("\n")
        .map((line) => line.replace(/\s+$/, ""))
        .join("\n")
        .replace(/\n+$/, "");

const buildResult = (outcome: ProcessOutcome, expectedOutput: string): LocalRunResult => {
    // ponytail: memory is reported as 0; Windows has no cheap per-process peak
    // and nothing here depends on it. Wire up a measured value if it ever matters.
    const base = {
        stdout: outcome.stdout || null,
        stderr: outcome.stderr || null,
        compile_output: null,
        time: (outcome.durationMs / 1000).toFixed(3),
        memory: 0,
    };

    if (outcome.isTimedOut) return { ...base, status: TIME_LIMIT_EXCEEDED };
    if (outcome.exitCode !== 0) return { ...base, status: RUNTIME_ERROR };

    const isMatch = normalizeOutput(outcome.stdout) === normalizeOutput(expectedOutput);
    return { ...base, status: isMatch ? ACCEPTED : WRONG_ANSWER };
};

export const runCodeLocally = async (
    sourceCode: string,
    languageId: string | number,
    testCases: TestCase[]
): Promise<{ success: true; result: LocalRunResult[] } | { success: false; result: string }> => {
    const language = LANGUAGES[Number(languageId)];
    if (!language) {
        return { success: false, result: `Unsupported language id ${languageId}` };
    }

    const workingDir = await mkdtemp(join(tmpdir(), "leetcode-run-"));

    try {
        await writeFile(join(workingDir, language.fileName), sourceCode, "utf-8");

        if (language.compileArgs) {
            const [command, args] = language.compileArgs;
            const compilation = await runProcess(command, args, workingDir, COMPILE_TIMEOUT_MS);

            if (compilation.missingCommand) {
                return { success: false, result: `${command} is not installed or not on PATH` };
            }
            if (compilation.isTimedOut || compilation.exitCode !== 0) {
                const message = compilation.stderr || compilation.stdout || "compilation failed";
                return {
                    success: true,
                    result: testCases.map(() => ({
                        status: COMPILATION_ERROR,
                        stdout: null,
                        stderr: null,
                        compile_output: message,
                        time: "0.000",
                        memory: 0,
                    })),
                };
            }
        }

        const results: LocalRunResult[] = [];
        for (const testCase of testCases) {
            const [command, args] = language.runArgs;
            const outcome = await runProcess(command, args, workingDir, RUN_TIMEOUT_MS, testCase.input);

            if (outcome.missingCommand) {
                return { success: false, result: `${command} is not installed or not on PATH` };
            }
            results.push(buildResult(outcome, testCase.output));
        }

        return { success: true, result: results };
    } catch (error) {
        return { success: false, result: error instanceof Error ? error.message : "Local run failed" };
    } finally {
        await rm(workingDir, { recursive: true, force: true });
    }
};
