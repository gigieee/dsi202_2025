# adopt/utils.py

import libscrc
import qrcode
import io

from typing import Optional, Union
from PIL import Image
from django.http import JsonResponse
import base64

# --- EMVCo Constants ---
TAG_PAYLOAD_FORMAT_INDICATOR = "00"
TAG_POINT_OF_INITIATION_METHOD = "01"
TAG_MERCHANT_ACCOUNT_INFORMATION = "29"
SUB_TAG_AID_PROMPTPAY = "00"
SUB_TAG_MOBILE_NUMBER_PROMPTPAY = "01"
SUB_TAG_NATIONAL_ID_PROMPTPAY = "02"
TAG_TRANSACTION_CURRENCY = "53"
TAG_TRANSACTION_AMOUNT = "54"
TAG_COUNTRY_CODE = "58"
TAG_CRC = "63"

VALUE_PAYLOAD_FORMAT_INDICATOR = "01"
VALUE_POINT_OF_INITIATION_ONETIME = "12"
VALUE_PROMPTPAY_AID = "A000000677010111"
VALUE_COUNTRY_CODE_TH = "TH"
VALUE_CURRENCY_THB = "764"
LEN_CRC_VALUE_HEX = "04"

class InvalidInputError(Exception):
    pass

def _format_tlv(tag: str, value: str) -> str:
    length_str = f"{len(value):02d}"
    return f"{tag}{length_str}{value}"

def calculate_crc(code_string: str) -> str:
    encoded_string = str.encode(code_string, 'ascii')
    crc_val = libscrc.ccitt_false(encoded_string)
    crc_hex_str = hex(crc_val)[2:].upper()
    return crc_hex_str.rjust(4, '0')

def generate_promptpay_qr_payload(
    mobile: Optional[str] = None,
    nid: Optional[str] = None,
    amount: Optional[Union[float, int, str]] = None,
) -> str:
    if not mobile and not nid:
        raise InvalidInputError("Either mobile or NID must be provided.")

    payload_elements = [
        _format_tlv(TAG_PAYLOAD_FORMAT_INDICATOR, VALUE_PAYLOAD_FORMAT_INDICATOR),
        _format_tlv(TAG_POINT_OF_INITIATION_METHOD, VALUE_POINT_OF_INITIATION_ONETIME)
    ]

    merchant_account = [_format_tlv(SUB_TAG_AID_PROMPTPAY, VALUE_PROMPTPAY_AID)]

    if mobile:
        if len(mobile) != 10 or not mobile.isdigit():
            raise InvalidInputError("Invalid mobile number.")
        formatted = f"00{VALUE_COUNTRY_CODE_TH}{mobile[1:]}"
        merchant_account.append(_format_tlv(SUB_TAG_MOBILE_NUMBER_PROMPTPAY, formatted))
    elif nid:
        nid = nid.replace('-', '')
        if len(nid) != 13 or not nid.isdigit():
            raise InvalidInputError("Invalid NID.")
        merchant_account.append(_format_tlv(SUB_TAG_NATIONAL_ID_PROMPTPAY, nid))

    payload_elements.append(
        _format_tlv(TAG_MERCHANT_ACCOUNT_INFORMATION, "".join(merchant_account))
    )
    payload_elements.append(_format_tlv(TAG_TRANSACTION_CURRENCY, VALUE_CURRENCY_THB))

    if amount:
        amount_float = float(amount)
        if amount_float < 0:
            raise InvalidInputError("Amount cannot be negative.")
        payload_elements.append(_format_tlv(TAG_TRANSACTION_AMOUNT, f"{amount_float:.2f}"))

    payload_elements.append(_format_tlv(TAG_COUNTRY_CODE, VALUE_COUNTRY_CODE_TH))

    payload_body = "".join(payload_elements)
    string_to_crc = payload_body + TAG_CRC + LEN_CRC_VALUE_HEX
    crc = calculate_crc(string_to_crc)
    return string_to_crc + crc

def generate_promptpay_qr_image_base64(mobile: str, amount: Union[int, float]) -> str:
    payload = generate_promptpay_qr_payload(mobile=mobile, amount=amount)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    return base64.b64encode(img_bytes).decode("utf-8")
