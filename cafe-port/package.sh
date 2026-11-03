#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(cd "${project_dir}/.." && pwd)"
engine_rpx="${CAFE_RPX:-${project_dir}/runtime/cafe.rpx}"
wuhbtool="${WUHBTOOL:-/opt/devkitpro/tools/bin/wuhbtool}"
build_dir="${root_dir}/build"
scratch_dir="$(mktemp -d "${TMPDIR:-/tmp}/anegg-build.XXXXXX")"
trap 'rm -rf "${scratch_dir}"' EXIT
content_dir="${scratch_dir}/content"
output="${build_dir}/An-EgG-Cafe-Engine.wuhb"
staged_output="${scratch_dir}/An-EgG-Cafe-Engine.wuhb"

if [[ ! -f "${engine_rpx}" ]]; then
  echo "Cafe Engine RPX missing: ${engine_rpx}" >&2
  exit 1
fi
if [[ ! -x "${wuhbtool}" ]]; then
  echo "wuhbtool missing: ${wuhbtool}" >&2
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is needed to fit the TV and GamePad splash art." >&2
  exit 1
fi

art=(egg boss-core boss-ring boss-glow boss-aura hard-orb
  interior-fragment interior-beam void-particle shockwave-visible shockwave-hitbox
  avoidance-warning avoidance-hazard)
sounds=(final-boss.ogg hard-phase.wav hard-waves.wav
  shockwave-whoosh.wav hand-whoosh.wav hyperactivity.wav
  meme-shocked.wav meme-video.wav meme-oh-my-god.wav meme-faaah.wav
  meme-cat-laugh.wav meme-phone.wav)
sources=("${root_dir}/assets/fonts/Handlee-Regular.ttf")
art_sources=()
for name in "${art[@]}"; do
  source="${root_dir}/assets/images/${name}.png"
  if [[ -s "${project_dir}/assets/${name}.png" ]] &&
     { [[ ! -s "${source}" ]] || [[ "$(stat -f '%Sf' "${source}")" == *dataless* ]]; }; then
    source="${project_dir}/assets/${name}.png"
  fi
  art_sources+=("${source}")
done
sources+=("${art_sources[@]}")
for name in "${sounds[@]}"; do sources+=("${project_dir}/audio/${name}"); done
for source in "${sources[@]}"; do
  if [[ ! -s "${source}" ]] || [[ "$(stat -f '%Sf' "${source}")" == *dataless* ]]; then
    echo "Original art/audio is still cloud-only: ${source}" >&2
    echo "Download the original project's assets folder, then rerun this script." >&2
    exit 1
  fi
done

python3 "${project_dir}/tools/make_gradients.py"
cp "${project_dir}/main.cafe" "${project_dir}/main-bundle.cafe"
mkdir -p "${content_dir}/assets" "${content_dir}/audio" "${build_dir}"
cp "${project_dir}/main.uml" "${project_dir}/main-bundle.cafe" \
   "${project_dir}/main.cstyle" "${content_dir}/"
cp "${project_dir}/assets/"*.svg "${project_dir}/assets/"*.png "${content_dir}/assets/"
cp "${root_dir}/assets/fonts/Handlee-Regular.ttf" "${content_dir}/assets/"
for i in "${!art_sources[@]}"; do
  name="${art[$i]}"
  source="${art_sources[$i]}"
  case "${name}" in
    boss-glow|boss-aura)
      # These originals are 1424–2307 px wide but draw at under 182 px.
      # Keep the source untouched and ship a smaller GPU texture to Wii U.
      sips -Z 384 "${source}" --out "${content_dir}/assets/${name}.png" >/dev/null
      ;;
    boss-core|hard-orb)
      sips -Z 256 "${source}" --out "${content_dir}/assets/${name}.png" >/dev/null
      ;;
    *) cp "${source}" "${content_dir}/assets/" ;;
  esac
done
for name in "${sounds[@]}"; do
  cp "${project_dir}/audio/${name}" "${content_dir}/audio/"
done

sips -z 128 128 "${project_dir}/icon.png" --out "${scratch_dir}/icon-128.png" >/dev/null
ffmpeg -y -loglevel error -i "${project_dir}/tv.png" \
  -vf 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720' \
  -frames:v 1 -update 1 "${scratch_dir}/tv-1280.png"
ffmpeg -y -loglevel error -i "${project_dir}/tv.png" \
  -vf 'scale=854:480:force_original_aspect_ratio=increase,crop=854:480' \
  -frames:v 1 -update 1 "${scratch_dir}/drc-854.png"

"${wuhbtool}" "${engine_rpx}" "${staged_output}" \
  "--content=${content_dir}" \
  "--name=An EgG" "--short-name=An EgG" "--author=lf" \
  "--icon=${scratch_dir}/icon-128.png" \
  "--tv-image=${scratch_dir}/tv-1280.png" \
  "--drc-image=${scratch_dir}/drc-854.png"

mv -f "${staged_output}" "${output}"
echo "Built ${output}"
