# An EgG — Cafe Engine port

This is the CafeScript version of An EgG. Open `main.uml` with the Cafe Engine desktop runner to
try the title screen, save files, infinite desk, quests, and the UNDEF fight.
Both TV and GamePad use the same aspect-fitted 640 × 480 layout.

## Controls

- Left stick: move the cursor in the desk and fight; choose items in menus.
- Right stick or WASD: scroll the desk.
- A: grab or release an egg, and select a menu item.
- Fast swipe/release: launch an egg with friction.
- B or +: pause. X: quest book.
- Y: open the bag. With the Egg Grabber, drag an egg onto the backpack icon
  in the lower right to store it.
- GamePad touch or desktop mouse: drag eggs and scroll empty desk space.

The desk HUD and pause menu open the shop and bag. Breaking an egg earns $5,
frying one earns $10, and clearing UNDEF's final phase earns $100. The
Egg Grabber stores up to 24 eggs; the Portable Pan fries a stored raw egg in
2.4 seconds. The bag and shop show each item's art, with a selected-tile hint
that explains its action. If the desk is full when placing a bagged raw or
fried egg, one random desk egg breaks to make room after a clear spot is found.
A purchased giraffe stands at the lower left and eats eggs
dragged to it for $5. The electric giraffe stands at the lower right;
feeding it an egg makes blue sparks and completes ELEGGTROCUTED.
The electric giraffe costs $1000.
Butchering a normal giraffe puts six meat cuts in the bag; butchering an
electric giraffe gives six electric meat cuts. Press
a store on the map to open the item picker. Its Eggs, Food, and Gear tabs show
owned items as tiles; use ZL/ZR to change tabs, the stick/D-pad to pick an item,
and A to list it. A page control appears when a tab has more than six kinds of
items. Giraffes cannot be listed.
Each listed meat cut earns $2 every ten seconds. Other listed items earn $1
every ten seconds.
During the UNDEF arena and phase IV, select a meat slot, then carry it onto
UNDEF with the cursor. Normal meat glitches away without damage. Electric
meat overcharges UNDEF, plays the hyperactivity sound, and rolls the fast
secret credits. His shaking grows stronger until the sound ends. The silly
credits scroll twice as fast as before. The secret does not count as
defeating him. The next UNDEF
encounter is cyan through phases I–IV and plays the supplied meme sounds.
Leaving that encounter clears the tint, so entering again starts purple.
Clearing phase IV with
eggs rolls the regular credits and still grants the $100 reward.
The shop, egg rewards, and store sales use one money balance. Older save slots
merge their coin and dollar amounts when loaded. Shop purchases, stored eggs,
pending frying, and store income are kept in each save slot.

The forbidden button starts all three UNDEF phases. Difficulty comes from
completed quests: fewer than 10 is extra hard, 10 is hard, 25 is medium, and
50 is easy. Phase II starts after phase I ends; phase III starts when phase II
reaches half health. Clearing phase III leaves a black hole on the desk; press
it to start the phase IV chase. In Portal Biomes, eggs travel between linked
portals with their momentum, and may emerge upside down.

Three cave variants appear farther out on the desk: a default cave, a frying
pan cave, and a portal cave. Default and frying caves mix 80% gray with 20%
of their color; the default cave uses blue. Portal caves retain a 60% gray,
40% portal-color mix. The gray is slightly darkened. Black stone has rounded,
curving edges that block eggs and form connected tunnels;
only the default cave has blind branches. The cave walls and objects are
generated from the same coordinates each time, so saved desks remain stable.
Exposed outer corners are rounded. Seeded passages can curve diagonally or
snake from side to side while staying connected at chunk seams.
Cafe Engine makes the stone texture from each chunk's curve values at runtime
and keeps only a small set of nearby textures cached.

## Run and build

With the included assets available locally:

```bash
./runtime/cafe-macos main.uml
./package.sh
```

`package.sh` copies the original art and Handlee font, plus the Cafe port's
`audio/` files, into a temporary staging folder. It fits the splash and icon,
then creates the sole build output,
`build/An-EgG-Cafe-Engine.wuhb`. Put that WUHB in `sd:/wiiu/apps/` under
Aroma. The script refuses to make a package while an original asset is
cloud-only or missing. Both `runtime/cafe-macos` and `runtime/cafe.rpx` include
the particle emitter `camera` setting: `true` moves existing particles with
the emitter, while `false` leaves them where they were emitted.

On Wii U, Cafe Engine save slots live under
`sd:/wiiu/apps/cafe-engine/saves/`. To bring an old LÖVE save across,
copy `an-egg-slot-1.txt` (and other slot numbers you use) into that folder
before playing this port. The port reads the old line format and scales the
saved egg and camera positions to the 640 × 480 canvas. Keep a backup of the
old save files. Existing mod files and mod assignment files are ignored, so
old desk saves remain usable. The removed editor source is kept in `archive/`
for recovery; it is not included in the WUHB.

To rebuild the matching Wii U and desktop Cafe Engine runtimes from the Cafe
Engine source, run `tools/build-engine-with-color.sh` before `package.sh`.
Set `CAFE_ENGINE_SOURCE` if the source folder is somewhere other than
`/Users/lf/Cafe engine`. The script builds a temporary source copy, runs the
desktop tests, and updates `runtime/`.
