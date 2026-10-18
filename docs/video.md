# 30-second video — production plan

No source footage was supplied. No generated UI, fake notification or unfinished video is published. The page has an optional video insertion point documented below; absent assets leave no empty public section.

| Time | Actual source and motion |
| --- | --- |
| 0–4 s | Owner-approved logo; phone reveal and restrained camera move |
| 4–11 s | Real menu recording: dish choice, cart zoom and highlight |
| 11–17 s | Actual checkout; visibly label any isolated test flow |
| 17–23 s | Verified restaurant Telegram receipt; otherwise label simulation |
| 23–30 s | Pull back, logo, localized “View demo” CTA |

Collect approved high-resolution screen captures with synthetic data only, clean logo, licensed music, consent for any identifying footage. Record desktop/phone source at readable sizes. Keep restaurant names and tokens private. Prepare RU/UZ/EN captions and subtitles. Motion design can be authored later in Remotion; FFmpeg is the free encoding path now. Do not add a Node framework to the landing solely for this clip.

`py -3 scripts/video.py <approved-master.mp4> --output-dir <output-directory> --dry-run` prints the two reviewed FFmpeg commands. Without `--dry-run` it creates 16:9 and 9:16 H.264/AAC MP4 files; `-n` prevents overwrite; aspect-fit padding preserves the interface. A vertical native edit is preferable to padding for a final Reels campaign. The encoder requires real footage and FFmpeg. Rendering has not been claimed: footage is absent.

To publish an approved clip locally: place `tour.mp4` and `tour-poster.webp` in `assets/`, set `QADAMUP_VIDEO_READY=1`, and rebuild with `py -3 scripts/funnel.py`. Generator only inserts the section if both files exist. Use controls, no autoplay, preload=none, dimensions 1920×1080; no video fetch before interaction. Review the poster and localized captions before public deployment.
