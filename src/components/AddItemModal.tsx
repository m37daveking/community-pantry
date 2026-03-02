"use client";

import { supabase } from "@/lib/supabase";
import { useState, useEffect } from "react";

const QUICK_PICKS = ["🥒", "🍋", "🌿", "🍅", "🥬", "🫑", "🥕", "🍎", "🌽", "🥚"];

const FULL_EMOJIS: { label: string; emojis: string[] }[] = [
  { label: "Fruit", emojis: ["🍎", "🍐", "🍊", "🍋", "🍇", "🍓", "🫐", "🍌", "🍑", "🍒", "🍈", "🥝", "🍍", "🥭", "🫒"] },
  { label: "Veg", emojis: ["🥒", "🥕", "🍅", "🥬", "🫑", "🌽", "🥦", "🍆", "🧄", "🧅", "🥔", "🍠", "🫘", "🥜", "🌶️"] },
  { label: "Herbs & other", emojis: ["🌿", "🥚", "🍯", "🌻", "🫛", "🧈", "🍞", "🥛", "🫙", "🌰", "🥥", "🍄"] },
];

export default function AddItemModal({
  open,
  onClose,
  onAdded,
}: {
  open: boolean;
  onClose: () => void;
  onAdded: () => void;
}) {
  const [name, setName] = useState("");
  const [emoji, setEmoji] = useState("🥬");
  const [quantity, setQuantity] = useState("");
  const [fromName, setFromName] = useState("");
  const [pickupNote, setPickupNote] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [showAllEmojis, setShowAllEmojis] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("pantry-name");
    if (saved) setFromName(saved);
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim() || !quantity.trim() || !fromName.trim()) return;

    setSubmitting(true);
    localStorage.setItem("pantry-name", fromName.trim());

    await supabase.from("items").insert({
      name: name.trim(),
      emoji,
      quantity: quantity.trim(),
      from_name: fromName.trim(),
      pickup_note: pickupNote.trim() || null,
    });

    setName("");
    setQuantity("");
    setPickupNote("");
    setEmoji("🥬");
    setShowAllEmojis(false);
    setSubmitting(false);
    onAdded();
    onClose();
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/30 animate-fade-in"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative w-full sm:max-w-md max-h-[85vh] overflow-y-auto bg-cream rounded-t-2xl sm:rounded-2xl p-6 animate-slide-up shadow-xl">
        <div className="flex items-center justify-between mb-5">
          <h2 className="font-serif text-xl font-semibold text-green">
            Share something
          </h2>
          <button
            onClick={onClose}
            className="text-text-muted hover:text-text transition-colors text-2xl leading-none cursor-pointer"
          >
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Emoji picker */}
          <div>
            <label className="block text-xs font-medium text-text-muted mb-1.5">
              Pick an icon
            </label>

            {!showAllEmojis ? (
              <div className="flex gap-1.5 flex-wrap">
                {QUICK_PICKS.map((e) => (
                  <button
                    key={e}
                    type="button"
                    onClick={() => setEmoji(e)}
                    className={`text-2xl p-1.5 rounded-lg transition-all cursor-pointer ${
                      emoji === e
                        ? "bg-green-pale ring-2 ring-green scale-110"
                        : "hover:bg-cream-dark"
                    }`}
                  >
                    {e}
                  </button>
                ))}
                <button
                  type="button"
                  onClick={() => setShowAllEmojis(true)}
                  className="text-xs font-medium text-text-muted hover:text-green
                    px-2.5 py-1.5 rounded-lg hover:bg-cream-dark transition-colors cursor-pointer
                    flex items-center"
                >
                  more...
                </button>
              </div>
            ) : (
              <div className="space-y-2.5">
                {FULL_EMOJIS.map((group) => (
                  <div key={group.label}>
                    <p className="text-[10px] uppercase tracking-wider text-text-muted/60 font-medium mb-1">
                      {group.label}
                    </p>
                    <div className="flex gap-1 flex-wrap">
                      {group.emojis.map((e) => (
                        <button
                          key={e}
                          type="button"
                          onClick={() => {
                            setEmoji(e);
                            setShowAllEmojis(false);
                          }}
                          className={`text-xl p-1 rounded-lg transition-all cursor-pointer ${
                            emoji === e
                              ? "bg-green-pale ring-2 ring-green scale-110"
                              : "hover:bg-cream-dark"
                          }`}
                        >
                          {e}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => setShowAllEmojis(false)}
                  className="text-xs text-text-muted hover:text-green transition-colors cursor-pointer"
                >
                  show less
                </button>
              </div>
            )}
          </div>

          {/* Item name */}
          <div>
            <label htmlFor="item-name" className="block text-xs font-medium text-text-muted mb-1.5">
              What is it?
            </label>
            <input
              id="item-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Cucumbers, Limes, Basil..."
              required
              className="w-full px-3 py-2.5 bg-white border border-cream-dark rounded-lg
                text-text placeholder:text-text-muted/50
                focus:outline-none focus:ring-2 focus:ring-green/30 focus:border-green
                font-serif text-lg"
            />
          </div>

          {/* Quantity */}
          <div>
            <label htmlFor="quantity" className="block text-xs font-medium text-text-muted mb-1.5">
              How much?
            </label>
            <input
              id="quantity"
              type="text"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              placeholder="6, a big bag, heaps..."
              required
              className="w-full px-3 py-2.5 bg-white border border-cream-dark rounded-lg
                text-text placeholder:text-text-muted/50
                focus:outline-none focus:ring-2 focus:ring-green/30 focus:border-green"
            />
          </div>

          {/* Name */}
          <div>
            <label htmlFor="from-name" className="block text-xs font-medium text-text-muted mb-1.5">
              Your name
            </label>
            <input
              id="from-name"
              type="text"
              value={fromName}
              onChange={(e) => setFromName(e.target.value)}
              placeholder="Colin"
              required
              className="w-full px-3 py-2.5 bg-white border border-cream-dark rounded-lg
                text-text placeholder:text-text-muted/50
                focus:outline-none focus:ring-2 focus:ring-green/30 focus:border-green"
            />
          </div>

          {/* Pickup note */}
          <div>
            <label htmlFor="pickup-note" className="block text-xs font-medium text-text-muted mb-1.5">
              Pickup note <span className="text-text-muted/50">(optional)</span>
            </label>
            <input
              id="pickup-note"
              type="text"
              value={pickupNote}
              onChange={(e) => setPickupNote(e.target.value)}
              placeholder="Leave at front gate, ring doorbell..."
              className="w-full px-3 py-2.5 bg-white border border-cream-dark rounded-lg
                text-text placeholder:text-text-muted/50
                focus:outline-none focus:ring-2 focus:ring-green/30 focus:border-green"
            />
          </div>

          <button
            type="submit"
            disabled={submitting || !name.trim() || !quantity.trim() || !fromName.trim()}
            className="w-full py-3 bg-terracotta hover:bg-terracotta-light text-white
              font-medium rounded-lg transition-colors
              disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer text-sm"
          >
            {submitting ? "Adding..." : "Add to the pantry"}
          </button>
        </form>
      </div>
    </div>
  );
}
