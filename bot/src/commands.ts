import type { Message } from "whatsapp-web.js";
import { supabase, type Item } from "./supabase.js";
import { getEmoji } from "./emoji-map.js";

const PREFIX = "!pantry";

export function isPantryCommand(body: string): boolean {
  return body.trim().toLowerCase().startsWith(PREFIX);
}

export function parseCommand(body: string): { command: string; args: string } {
  const trimmed = body.trim().slice(PREFIX.length).trim();
  const spaceIndex = trimmed.indexOf(" ");
  if (spaceIndex === -1) {
    return { command: trimmed.toLowerCase() || "help", args: "" };
  }
  return {
    command: trimmed.slice(0, spaceIndex).toLowerCase(),
    args: trimmed.slice(spaceIndex + 1).trim(),
  };
}

export async function handleCommand(msg: Message): Promise<void> {
  const { command, args } = parseCommand(msg.body);

  switch (command) {
    case "help":
      return handleHelp(msg);
    case "list":
      return handleList(msg);
    case "add":
      return handleAdd(msg, args);
    case "claim":
      return handleClaim(msg, args);
    default:
      await msg.reply(
        `🤔 Unknown command. Try:\n\n` +
          `*!pantry list* — see what's available\n` +
          `*!pantry add* — add something\n` +
          `*!pantry claim <number>* — claim an item`
      );
  }
}

async function handleHelp(msg: Message): Promise<void> {
  await msg.reply(
    `🧺 *Community Pantry*\n\n` +
      `*!pantry list*\nSee what's available\n\n` +
      `*!pantry add <item>, <quantity>, <your name>*\nShare something — e.g.\n_!pantry add Tomatoes, heaps, Carol_\n\n` +
      `*!pantry add <item>, <quantity>, <your name>, "<note>"*\nWith a pickup note — e.g.\n_!pantry add Basil, a bunch, Carol, "front porch"_\n\n` +
      `*!pantry claim <number>*\nClaim an item from the list`
  );
}

async function handleList(msg: Message): Promise<void> {
  const { data: items } = await supabase
    .from("items")
    .select("*")
    .eq("is_taken", false)
    .order("created_at", { ascending: false });

  if (!items || items.length === 0) {
    await msg.reply(
      `🧺 The pantry's bare!\n\nGot something to share? Try:\n*!pantry add Tomatoes, heaps, Your Name*`
    );
    return;
  }

  const lines = items.map(
    (item: Item, i: number) =>
      `${i + 1}. ${item.emoji} *${item.name}* — ${item.quantity} _(from ${item.from_name})_` +
      (item.pickup_note ? `\n   📍 ${item.pickup_note}` : "")
  );

  await msg.reply(
    `🧺 *Community Pantry*\n\n` +
      lines.join("\n") +
      `\n\nReply *!pantry claim <number>* to grab something`
  );
}

async function handleAdd(msg: Message, args: string): Promise<void> {
  if (!args) {
    await msg.reply(
      `To add something, use:\n*!pantry add <item>, <quantity>, <your name>*\n\n` +
        `Example:\n_!pantry add Tomatoes, heaps, Carol_\n_!pantry add Basil, a bunch, Carol, "front porch"_`
    );
    return;
  }

  // Parse: name, quantity, from_name[, "pickup note"]
  // Handle quoted pickup note
  let pickupNote: string | null = null;
  let rest = args;

  // Check for quoted pickup note at the end
  const quoteMatch = rest.match(/,\s*[""]([^""]+)[""]\s*$/);
  if (quoteMatch) {
    pickupNote = quoteMatch[1].trim();
    rest = rest.slice(0, quoteMatch.index!).trim();
  }

  const parts = rest.split(",").map((s) => s.trim());

  if (parts.length < 3) {
    await msg.reply(
      `Hmm, I need at least: *item, quantity, your name*\n\n` +
        `Example: _!pantry add Tomatoes, heaps, Carol_`
    );
    return;
  }

  const name = parts[0];
  const quantity = parts[1];
  const fromName = parts[2];

  // If there's a 4th part and no quoted note was found, treat it as the note
  if (!pickupNote && parts.length >= 4) {
    pickupNote = parts.slice(3).join(", ").trim();
  }

  const emoji = getEmoji(name);

  const { error } = await supabase.from("items").insert({
    name,
    emoji,
    quantity,
    from_name: fromName,
    pickup_note: pickupNote || null,
  });

  if (error) {
    await msg.reply(`❌ Something went wrong adding that. Try again?`);
    return;
  }

  let reply = `${emoji} Added! *${name}* (${quantity}) from ${fromName}`;
  if (pickupNote) {
    reply += ` — 📍 ${pickupNote}`;
  }
  await msg.reply(reply);
}

async function handleClaim(msg: Message, args: string): Promise<void> {
  const num = parseInt(args, 10);

  if (!args || isNaN(num) || num < 1) {
    await msg.reply(
      `Which item? Use *!pantry list* first, then *!pantry claim <number>*`
    );
    return;
  }

  // Fetch available items in same order as list
  const { data: items } = await supabase
    .from("items")
    .select("*")
    .eq("is_taken", false)
    .order("created_at", { ascending: false });

  if (!items || items.length === 0) {
    await msg.reply(`🧺 Nothing to claim — the pantry's empty!`);
    return;
  }

  if (num > items.length) {
    await msg.reply(
      `There are only ${items.length} item${items.length === 1 ? "" : "s"} available. Try *!pantry list* to see them.`
    );
    return;
  }

  const item = items[num - 1];

  const { error } = await supabase
    .from("items")
    .update({ is_taken: true, taken_at: new Date().toISOString() })
    .eq("id", item.id);

  if (error) {
    await msg.reply(`❌ Something went wrong claiming that. Try again?`);
    return;
  }

  await msg.reply(`✅ *${item.name}* claimed! Enjoy 🎉`);
}
