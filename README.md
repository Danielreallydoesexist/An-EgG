# An EgG

An EgG is a Wii U game built with [Cafe Engine](https://github.com/Danielreallydoesexist/Cafe-Engine). Drag and throw eggs across an infinite desk, complete quests, explore procedural biomes, and fight UNDEF.

The game source and Wii U packaging script are in [`cafe-port/`](cafe-port/). The original art, sounds, and Handlee font are in [`assets/`](assets/); Scratch source assets are retained in [`original/`](original/).

## Run on macOS

```sh
cd cafe-port
./runtime/cafe-macos main.uml
```

## Build for Wii U

Cafe Engine must be available at `/Users/lf/Cafe engine`, or set `CAFE_ENGINE_SOURCE` to its location. The Wii U build needs devkitPro with Wii U tools. Build the runtime and package An EgG with:

```sh
cd cafe-port
./tools/build-engine-with-color.sh
./package.sh
```

The WUHB is written to `build/An-EgG-Cafe-Engine.wuhb` at the repository root. Copy it to `sd:/wiiu/apps/` for Aroma. See [`cafe-port/README.md`](cafe-port/README.md) for controls and gameplay details.

Save files live on the Wii U SD card under `sd:/wiiu/apps/cafe-engine/saves/` and are not part of this repository.

## License

The An EgG source code and project documentation are licensed under the [MIT License](LICENSE). Bundled art, audio, fonts, and the Cafe Engine runtime are separate from this grant and retain their own terms. The Handlee font is licensed under the [SIL Open Font License 1.1](assets/fonts/OFL.txt).
