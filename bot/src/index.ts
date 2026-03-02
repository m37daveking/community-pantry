import pkg from "whatsapp-web.js";
const { Client, LocalAuth } = pkg;
import qrcode from "qrcode-terminal";
import { isPantryCommand, handleCommand } from "./commands.js";

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  },
});

client.on("qr", (qr) => {
  console.log("\n📱 Scan this QR code with WhatsApp:\n");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("✅ Community Pantry bot is running!");
});

client.on("authenticated", () => {
  console.log("🔐 Authenticated with WhatsApp");
});

client.on("auth_failure", (msg) => {
  console.error("❌ Auth failure:", msg);
});

client.on("disconnected", (reason) => {
  console.log("🔌 Disconnected:", reason);
  // Attempt to reconnect
  client.initialize();
});

client.on("message", async (msg) => {
  // Only respond to pantry commands
  if (!isPantryCommand(msg.body)) return;

  try {
    await handleCommand(msg);
  } catch (err) {
    console.error("Error handling command:", err);
    try {
      await msg.reply(
        "❌ Something went wrong. Try again or use *!pantry* for help."
      );
    } catch {
      // Can't reply, just log
    }
  }
});

console.log("🧺 Starting Community Pantry WhatsApp bot...");
client.initialize();
