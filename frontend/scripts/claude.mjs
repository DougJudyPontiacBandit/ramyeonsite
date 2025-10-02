// scripts/claude.mjs
import Anthropic from "@anthropic-ai/sdk";

async function main() {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    console.error("❌ Missing ANTHROPIC_API_KEY environment variable.");
    console.error("   Set it, then re-open your terminal.");
    process.exit(1);
  }

  const client = new Anthropic({ apiKey });

  // Take everything after the script name as the prompt
  const prompt = process.argv.slice(2).join(" ").trim() || "Say hello!";

  try {
    const msg = await client.messages.create({
      // You can change models later; this is a safe default
      model: "claude-3-haiku-20240307",
      max_tokens: 500,
      messages: [{ role: "user", content: prompt }],
    });

    // Claude returns an array of content blocks; print text blocks
    const text =
      (msg.content || [])
        .filter((p) => p.type === "text")
        .map((p) => p.text)
        .join("\n") || "[No text content returned]";
    console.log(text);
  } catch (err) {
    // Show a readable error
    const msg =
      err?.response?.data?.error?.message ||
      err?.message ||
      JSON.stringify(err, null, 2);
    console.error("❌ Claude error:", msg);
    process.exit(1);
  }
}

main();
