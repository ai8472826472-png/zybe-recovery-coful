# Zybe Recovery product makefile (based on 404xg31/coful_G31)
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, vendor/twrp/config/common.mk)
$(call inherit-product, device/motorola/coful/device.mk)

PRODUCT_DEVICE := coful
PRODUCT_NAME := twrp_coful
PRODUCT_BRAND := motorola
PRODUCT_MODEL := moto g31
PRODUCT_MANUFACTURER := motorola
PRODUCT_RELEASE_NAME := coful

PRODUCT_GMS_CLIENTID_BASE := android-motorola

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRIVATE_BUILD_DESC="coful_g-user 12 S3RWBS32.125-29-2-4-3 3c754f release-keys"

BUILD_FINGERPRINT := motorola/coful_g/coful:12/S3RWBS32.125-29-2-4-3/3c754f:user/release-keys
