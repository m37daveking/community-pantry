// Maps common item names to emojis for auto-assignment.
// Matching is case-insensitive and checks if the item name contains the keyword.

const EMOJI_MAP: [string[], string][] = [
  // Fruit
  [["apple"], "🍎"],
  [["pear"], "🍐"],
  [["orange"], "🍊"],
  [["lemon", "lime"], "🍋"],
  [["grape"], "🍇"],
  [["strawberr"], "🍓"],
  [["blueberr"], "🫐"],
  [["banana"], "🍌"],
  [["peach", "nectarine"], "🍑"],
  [["cherry", "cherries"], "🍒"],
  [["melon", "rockmelon", "cantaloupe", "honeydew"], "🍈"],
  [["kiwi"], "🥝"],
  [["pineapple"], "🍍"],
  [["mango"], "🥭"],
  [["olive"], "🫒"],

  // Vegetables
  [["cucumber", "zucchini", "courgette"], "🥒"],
  [["carrot"], "🥕"],
  [["tomato"], "🍅"],
  [["lettuce", "spinach", "silverbeet", "chard", "greens", "kale"], "🥬"],
  [["capsicum", "pepper", "bell pepper"], "🫑"],
  [["corn", "sweetcorn"], "🌽"],
  [["broccoli"], "🥦"],
  [["eggplant", "aubergine"], "🍆"],
  [["garlic"], "🧄"],
  [["onion"], "🧅"],
  [["potato", "spud"], "🥔"],
  [["sweet potato", "kumara"], "🍠"],
  [["bean"], "🫘"],
  [["peanut"], "🥜"],
  [["chilli", "chili", "jalapeno", "habanero"], "🌶️"],

  // Herbs & other
  [["herb", "basil", "mint", "parsley", "coriander", "cilantro", "rosemary", "thyme", "oregano", "dill", "sage"], "🌿"],
  [["egg"], "🥚"],
  [["honey"], "🍯"],
  [["sunflower", "flower"], "🌻"],
  [["pea"], "🫛"],
  [["butter"], "🧈"],
  [["bread", "loaf", "sourdough"], "🍞"],
  [["milk"], "🥛"],
  [["jam", "preserve", "pickle", "chutney", "sauce", "jar"], "🫙"],
  [["chestnut", "walnut", "almond", "nut"], "🌰"],
  [["coconut"], "🥥"],
  [["mushroom"], "🍄"],
];

const DEFAULT_EMOJI = "🥬";

export function getEmoji(itemName: string): string {
  const lower = itemName.toLowerCase();
  for (const [keywords, emoji] of EMOJI_MAP) {
    if (keywords.some((kw) => lower.includes(kw))) {
      return emoji;
    }
  }
  return DEFAULT_EMOJI;
}
