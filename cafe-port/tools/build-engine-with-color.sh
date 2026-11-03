#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="${CAFE_ENGINE_SOURCE:-/Users/lf/Cafe engine}"
export DEVKITPRO="${DEVKITPRO:-/opt/devkitpro}"
export DEVKITPPC="${DEVKITPPC:-${DEVKITPRO}/devkitPPC}"
export PATH="${DEVKITPPC}/bin:${DEVKITPRO}/tools/bin:${PATH}"
stage_dir="$(mktemp -d "${TMPDIR:-/tmp}/anegg-cafe-engine.XXXXXX")"
trap 'rm -rf "${stage_dir}"' EXIT

if [[ ! -f "${source_dir}/src/renderer/SoftwareRenderer.cpp" ]]; then
  echo "Cafe Engine source missing: ${source_dir}" >&2
  exit 1
fi

rsync -a --exclude build --exclude build-wiiu --exclude dist \
  --exclude cafe-preview.ppm "${source_dir}/" "${stage_dir}/"
cmake -S "${stage_dir}" -B "${stage_dir}/build" \
  -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=ON
cmake --build "${stage_dir}/build" --parallel 4
ctest --test-dir "${stage_dir}/build" --output-on-failure

/opt/devkitpro/portlibs/wiiu/bin/powerpc-eabi-cmake \
  -S "${stage_dir}" -B "${stage_dir}/build-wiiu" \
  -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF
cmake --build "${stage_dir}/build-wiiu" --parallel 4

cp "${stage_dir}/build/cafe" "${project_dir}/runtime/cafe-macos"
cp "${stage_dir}/build-wiiu/cafe.rpx" "${project_dir}/runtime/cafe.rpx"
echo "Updated Cafe Engine runtimes for An EgG."
