"use client";

import { Item, supabase } from "@/lib/supabase";
import { timeAgo } from "@/lib/time";
import { useState } from "react";

const rotations = [
  "card-rotate-1",
  "card-rotate-2",
  "card-rotate-3",
  "card-rotate-4",
  "card-rotate-5",
  "card-rotate-6",
];

export default function ItemCard({ item, index, onRefresh }: { item: Item; index: number; onRefresh: () => void }) {
  const [marking, setMarking] = useState(false);
  const rotation = rotations[index % rotations.length];

  async function markAsTaken() {
    setMarking(true);
    await supabase
      .from("items")
      .update({ is_taken: true, taken_at: new Date().toISOString() })
      .eq("id", item.id);
    setMarking(false);
    onRefresh();
  }

  async function markAsAvailable() {
    setMarking(true);
    await supabase
      .from("items")
      .update({ is_taken: false, taken_at: null })
      .eq("id", item.id);
    setMarking(false);
    onRefresh();
  }

  return (
    <div
      className={`
        ${rotation} ${item.is_taken ? "item-taken" : ""}
        bg-white rounded-xl p-5 shadow-md hover:shadow-lg
        border border-cream-dark
        transition-all duration-300 ease-in-out
      `}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-2xl flex-shrink-0">{item.emoji}</span>
            <h3 className="item-name font-serif text-xl font-semibold text-green truncate">
              {item.name}
            </h3>
          </div>

          <p className="text-brown font-medium text-sm mb-2">
            {item.quantity}
          </p>

          <div className="flex items-center gap-1.5 text-text-muted text-xs">
            <span>from</span>
            <span className="font-medium text-brown">{item.from_name}</span>
            <span className="mx-1">&middot;</span>
            <span>{timeAgo(item.created_at)}</span>
          </div>

          {item.pickup_note && (
            <p className="mt-2 text-xs text-brown-light italic bg-cream rounded-lg px-3 py-1.5">
              {item.pickup_note}
            </p>
          )}
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-cream-dark">
        {item.is_taken ? (
          <button
            onClick={markAsAvailable}
            disabled={marking}
            className="w-full text-xs font-medium text-terracotta hover:text-terracotta-light
              transition-colors disabled:opacity-50 py-1 cursor-pointer"
          >
            {marking ? "Updating..." : "Oops, still available"}
          </button>
        ) : (
          <button
            onClick={markAsTaken}
            disabled={marking}
            className="w-full text-sm font-medium text-white bg-green hover:bg-green-light
              rounded-lg py-2 transition-colors disabled:opacity-50 cursor-pointer"
          >
            {marking ? "Updating..." : "I'll take this!"}
          </button>
        )}
      </div>
    </div>
  );
}
