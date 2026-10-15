# Steam Workshop publishing checklist

The repository is ready to package, but the mod has **not** been uploaded to Steam Workshop.

1. Complete the live gameplay and multiplayer checks in [TESTING.md](TESTING.md), including a dedicated server with two clients. Update the README and Workshop descriptions with the tested build once those checks pass.
2. Put the repository's mod files in the DST `mods` folder and enable the mod. Exclude the `.git` directory and development-only `tools` and `docs` folders from the Workshop package if using a manual uploader.
3. Use `preview.png` as the Workshop preview image.
4. Paste [English description](STEAM_WORKSHOP_EN.md) and [Korean description](STEAM_WORKSHOP_KO.md) into the Workshop listing, then review the combined text and links.
5. Publish only after the in-game checks pass.
