"use client";

import { useEffect, useState, useCallback } from "react";
import { supabase, Item } from "@/lib/supabase";
import { isOlderThan24Hours } from "@/lib/time";
import ItemCard from "@/components/ItemCard";
import AddItemModal from "@/components/AddItemModal";

export default function Home() {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);

  const fetchItems = useCallback(async () => {
    const { data } = await supabase
      .from("items")
      .select("*")
      .order("created_at", { ascending: false });
    if (data) setItems(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchItems();

    const channel = supabase
      .channel("items-realtime")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "items" },
        () => {
          fetchItems();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [fetchItems]);

  // Split items: available first, then taken (collapsed if >24h old)
  const available = items.filter((i) => !i.is_taken);
  const recentlyTaken = items.filter(
    (i) => i.is_taken && !isOlderThan24Hours(i.taken_at)
  );
  const oldTaken = items.filter(
    (i) => i.is_taken && isOlderThan24Hours(i.taken_at)
  );

  return (
    <div className="min-h-screen pb-24">
      {/* Header */}
      <header className="pt-8 pb-6 px-5 text-center">
        <h1 className="font-serif text-3xl sm:text-4xl font-bold text-green mb-1">
          Community Pantry
        </h1>
        <p className="text-text-muted text-sm">
          Surplus from the neighbourhood, free to a good home
        </p>
      </header>

      {/* Content */}
      <main className="max-w-lg mx-auto px-4">
        {loading ? (
          <div className="text-center py-16">
            <p className="text-text-muted text-sm">Loading the pantry...</p>
          </div>
        ) : items.length === 0 ? (
          /* Empty state */
          <div className="text-center py-16 px-6">
            <div className="text-5xl mb-4">🧺</div>
            <h2 className="font-serif text-xl text-green mb-2">
              The pantry&apos;s bare
            </h2>
            <p className="text-text-muted text-sm mb-6">
              Got something to share? Tomatoes going wild? Too many eggs?
              <br />
              Be the first to add something.
            </p>
            <button
              onClick={() => setModalOpen(true)}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-terracotta
                hover:bg-terracotta-light text-white font-medium rounded-lg
                transition-colors text-sm cursor-pointer"
            >
              Share something
            </button>
          </div>
        ) : (
          <>
            {/* Available items */}
            {available.length > 0 && (
              <div className="grid gap-4">
                {available.map((item, i) => (
                  <ItemCard key={item.id} item={item} index={i} onRefresh={fetchItems} />
                ))}
              </div>
            )}

            {/* Recently taken */}
            {recentlyTaken.length > 0 && (
              <div className="mt-8">
                <p className="text-xs text-text-muted uppercase tracking-wider font-medium mb-3 px-1">
                  Recently claimed
                </p>
                <div className="grid gap-3">
                  {recentlyTaken.map((item, i) => (
                    <ItemCard
                      key={item.id}
                      item={item}
                      index={i + available.length}
                      onRefresh={fetchItems}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Old taken items (collapsed) */}
            {oldTaken.length > 0 && (
              <div className="mt-8">
                <p className="text-xs text-text-muted uppercase tracking-wider font-medium mb-3 px-1">
                  Previously shared
                </p>
                <div className="grid gap-2 opacity-40">
                  {oldTaken.map((item) => (
                    <div
                      key={item.id}
                      className="bg-white/60 rounded-lg px-4 py-2.5 text-sm flex items-center gap-2"
                    >
                      <span>{item.emoji}</span>
                      <span className="line-through text-text-muted font-serif">
                        {item.name}
                      </span>
                      <span className="text-text-muted/60 text-xs ml-auto">
                        from {item.from_name}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Floating add button */}
      {!loading && (
        <button
          onClick={() => setModalOpen(true)}
          className="fixed bottom-6 right-6 w-14 h-14 bg-terracotta hover:bg-terracotta-light
            text-white rounded-full shadow-lg hover:shadow-xl
            transition-all text-2xl flex items-center justify-center cursor-pointer
            active:scale-95"
          aria-label="Share something"
        >
          +
        </button>
      )}

      <AddItemModal open={modalOpen} onClose={() => setModalOpen(false)} onAdded={fetchItems} />
    </div>
  );
}
