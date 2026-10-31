# Profile maintenance

The English profile is `README.md`; the Chinese version is `README.zh-CN.md`. Both render from this public repository's `main` branch.

## Open-source components

- [GitHub Profile 3D Contrib](https://github.com/yoshi389111/github-profile-3d-contrib), MIT: generates the contribution skyline and public activity breakdown. Pinned to `7d95e7d4cdc028dd1e1cbd957d65f35efb12ae39`.
- [Platane/snk](https://github.com/Platane/snk): generates the optional animated contribution trace. Pinned to `d8f6715049803e982ee5ff501b6b9b7d5deeb09b`.
- [actions/checkout](https://github.com/actions/checkout): checks out this repository. Pinned to `11d5960a326750d5838078e36cf38b85af677262`.
- Sora is distributed under the SIL Open Font License; see `assets/OFL-Sora.txt`.

The hero and architecture artwork are original SVGs built around the Coloop mark. All load-bearing images are stored in this repository. No live widget endpoint or personal token is needed.

## Updates

`.github/workflows/profile.yml` refreshes public contribution visuals daily at approximately **03:17 Asia/Shanghai** (19:17 UTC). GitHub may delay scheduled runs. It also supports **Actions → Refresh profile visuals → Run workflow**.

The workflow uses GitHub's built-in `GITHUB_TOKEN`; only this repository receives write permission so the bot can commit generated images. It does not fetch private project source. Public contribution aggregation follows GitHub's visibility settings. Scheduled workflows may stop after prolonged repository inactivity; run the workflow manually or re-enable it in Actions if needed.

Edit `profile-settings.json` to adjust the skyline palette. Regenerate the static hero and architecture SVGs with:

```sh
python -m pip install 'fonttools>=4.50,<5'
python scripts/build-profile-assets.py
```

The SVG animation respects `prefers-reduced-motion`. Identity and project descriptions remain native Markdown, with theme-aware `<picture>` images and descriptive alt text.
