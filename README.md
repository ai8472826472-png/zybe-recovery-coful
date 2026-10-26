# Zybe Recovery for Moto G31 (coful)

Unofficial custom recovery build for the **Motorola Moto G31, Indian/LatAm model (codename `coful`, XT2173-1 / XT2173-2)**, MediaTek Helio G85 (MT6768).

**UNTESTED** until someone boots it on a real phone. Use at your own risk.

- Base: OrangeFox Recovery (fox_12.1), with a TWRP 12.1 fallback built in the same run
- Branding: "Zybe Recovery", dark theme with a blue accent
- Device tree: [404xg31/coful_G31](https://github.com/404xg31/coful_G31) @ `b65cd226487f` (TWRP tree made with twrpdtgen from India firmware S3RWBS32.125-29-2-4-3)
- Touch modules (focaltech / goodix, vermagic 4.19.191-g8d7f445cecef): [Swastik369/twrp_device_motorola_coful](https://github.com/Swastik369/twrp_device_motorola_coful) @ `f1dc027d6045`
- Kernel: stock prebuilt 4.19.191 (from the tree). The kernel only supports **gzip** ramdisks (CONFIG_RD_GZIP only), and the image must fit the **32 MiB** boot partition.

The phone is A/B and has **no recovery partition**: recovery lives inside the boot image. So this is a `boot.img` that boots straight into recovery.

Safe test: `fastboot boot <image>` (temporary, nothing is written). Flashing it to `boot` replaces normal Android boot until the stock boot.img is flashed back.

Builds run in GitHub Actions (`.github/workflows/build.yml`); images are attached to Releases.
