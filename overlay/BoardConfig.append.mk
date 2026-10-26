
# ---------------- Zybe Recovery additions ----------------
# The kernel only has CONFIG_RD_GZIP: never use lz4/xz for the ramdisk.
BOARD_RAMDISK_USE_LZ4 := false
# Let the build finish; tools/fit_boot.py repacks and enforces the real 32 MiB limit.
BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864
BOARD_RECOVERYIMAGE_PARTITION_SIZE := 67108864

# Touchscreen drivers are modules on this phone (not built into the kernel).
# The .ko files are copied into recovery/root/vendor/lib/modules/1.1 by the workflow.
TW_LOAD_VENDOR_MODULES := "focaltech_mtk_v2_mmi.ko goodix_mtk_gtx8_mmi.ko goodix_mtk_gtx8_ts_tools_mmi.ko"

TW_DEVICE_VERSION := Zybe
TW_EXTRA_LANGUAGES := false
TW_EXCLUDE_TWRPAPP := true
TW_EXCLUDE_PYTHON := true
TW_EXCLUDE_NANO := true
TW_EXCLUDE_TZDATA := true
TW_EXCLUDE_LPDUMP := true
TW_EXCLUDE_APEX := true
TW_FRAMERATE := 60
TARGET_USES_MKE2FS := true
