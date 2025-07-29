/*
 * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The OpenAirInterface Software Alliance licenses this file to You under
 * the OAI Public License, Version 1.1  (the "License"); you may not use this
 * file except in compliance with the License. You may obtain a copy of the
 * License at
 *
 *      http://www.openairinterface.org/?page_id=698
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *-------------------------------------------------------------------------------
 * For more information about the OpenAirInterface (OAI) Software Alliance:
 *      contact@openairinterface.org
 */

#include <curl/curl.h>
#include <iostream>

#include "UlNasTransport.hpp"

#include "NasHelper.hpp"

// pdu received time
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>
#include <iomanip>

using namespace nas;

//------------------------------------------------------------------------------
UlNasTransport::UlNasTransport()
    : NasMmPlainHeader(EPD_5GS_MM_MSG, UL_NAS_TRANSPORT) {
  ie_pdu_session_id                = std::nullopt;
  ie_old_pdu_session_id            = std::nullopt;
  ie_request_type                  = std::nullopt;
  ie_s_nssai                       = std::nullopt;
  ie_dnn                           = std::nullopt;
  ie_additional_information        = std::nullopt;
  ie_ma_pdu_session_information    = std::nullopt;
  ie_release_assistance_indication = std::nullopt;
}

//------------------------------------------------------------------------------
UlNasTransport::~UlNasTransport() {}

//------------------------------------------------------------------------------
void UlNasTransport::SetHeader(uint8_t security_header_type) {
  NasMmPlainHeader::SetSecurityHeaderType(security_header_type);
}

//------------------------------------------------------------------------------
void UlNasTransport::SetPayloadContainerType(uint8_t value) {
  ie_payload_container_type.SetValue(value);
}

//------------------------------------------------------------------------------
uint8_t UlNasTransport::GetPayloadContainerType() const {
  return ie_payload_container_type.GetValue();
}

//------------------------------------------------------------------------------
void UlNasTransport::SetPayloadContainer(
    const std::vector<PayloadContainerEntry>& content) {
  ie_payload_container.SetValue(content);
}

//------------------------------------------------------------------------------
void UlNasTransport::GetPayloadContainer(bstring& content) const {
  ie_payload_container.GetValue(content);
}

//------------------------------------------------------------------------------
bool UlNasTransport::GetPayloadContainerDID(
    bstring& did_payloadcontainer) const {
  return ie_payload_container.GetValueDID(did_payloadcontainer);
}

//------------------------------------------------------------------------------
void UlNasTransport::GetPayloadContainer(
    std::vector<PayloadContainerEntry>& content) const {
  ie_payload_container.GetValue(content);
}

//------------------------------------------------------------------------------
void UlNasTransport::SetPduSessionId(uint8_t value) {
  ie_pdu_session_id =
      std::make_optional<PduSessionIdentity2>(kIeiPduSessionId, value);
}

//------------------------------------------------------------------------------
bool UlNasTransport::GetPduSessionId(uint8_t& value) const {
  if (ie_pdu_session_id.has_value()) {
    value = ie_pdu_session_id.value().GetValue();
    return true;
  } else {
    return false;
  }
}

//------------------------------------------------------------------------------
void UlNasTransport::SetOldPduSessionId(uint8_t value) {
  ie_old_pdu_session_id =
      std::make_optional<PduSessionIdentity2>(kIeiOldPduSessionId, value);
}

//------------------------------------------------------------------------------
bool UlNasTransport::GetOldPduSessionId(uint8_t& value) const {
  if (ie_old_pdu_session_id.has_value()) {
    value = ie_old_pdu_session_id.value().GetValue();
    return true;
  } else {
    return false;
  }
}

//------------------------------------------------------------------------------
void UlNasTransport::SetRequestType(uint8_t value) {
  ie_request_type = std::make_optional<RequestType>(value);
}

//------------------------------------------------------------------------------
bool UlNasTransport::GetRequestType(uint8_t& value) const {
  if (ie_request_type.has_value()) {
    value = ie_request_type.value().GetValue();
    return true;
  } else {
    return false;
  }
}

//------------------------------------------------------------------------------
void UlNasTransport::SetSNssai(const SNSSAI_s& snssai) {
  ie_s_nssai =
      std::make_optional<SNssai>(std::optional<uint8_t>{kIeiSNssai}, snssai);
}

//------------------------------------------------------------------------------
bool UlNasTransport::GetSNssai(SNSSAI_s& snssai) const {
  if (ie_s_nssai.has_value()) {
    ie_s_nssai.value().getValue(snssai);
    return true;
  } else {
    return false;
  }
}

//------------------------------------------------------------------------------
void UlNasTransport::SetDnn(const bstring& dnn) {
  ie_dnn = std::make_optional<Dnn>(dnn);
}

//------------------------------------------------------------------------------
bool UlNasTransport::GetDnn(bstring& dnn) const {
  if (ie_dnn.has_value()) {
    ie_dnn.value().GetValue(dnn);
    return true;
  } else {
    return false;
  }
}

//------------------------------------------------------------------------------
void UlNasTransport::SetAdditionalInformation(const bstring& value) {
  ie_additional_information = std::make_optional<AdditionalInformation>(value);
}

//------------------------------------------------------------------------------
void UlNasTransport::SetMaPduSessionInformation(uint8_t value) {
  ie_ma_pdu_session_information =
      std::make_optional<MaPduSessionInformation>(value);
}

//------------------------------------------------------------------------------
void UlNasTransport::SetReleaseAssistanceIndication(uint8_t value) {
  ie_release_assistance_indication =
      std::make_optional<ReleaseAssistanceIndication>(value);
}

//------------------------------------------------------------------------------
int UlNasTransport::Encode(uint8_t* buf, int len) {
  Logger::nas_mm().debug("Encoding UL NAS Transport message");
  int encoded_size    = 0;
  int encoded_ie_size = 0;

  // Header
  if ((encoded_ie_size = NasMmPlainHeader::Encode(buf, len)) ==
      KEncodeDecodeError) {
    Logger::nas_mm().error("Encoding NAS Header error");
    return KEncodeDecodeError;
  }
  encoded_size += encoded_ie_size;

  // Payload Container Type
  if ((encoded_ie_size = NasHelper::Encode(
           ie_payload_container_type, buf, len, encoded_size)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }
  if (encoded_ie_size == 0)
    encoded_size++;  // 1/2 octet for  ie_payload_container_type, 1/2 octet for
                     // spare

  // Payload container
  // TODO: use NAS helper
  encoded_ie_size = ie_payload_container.Encode(
      buf + encoded_size, len - encoded_size,
      ie_payload_container_type.GetValue());
  if (encoded_ie_size != KEncodeDecodeError) {
    encoded_size += encoded_ie_size;
  } else {
    Logger::nas_mm().error(
        "Decoding %s error", PayloadContainer::GetIeName().c_str());
    return KEncodeDecodeError;
  }

  // PDU session ID
  if ((encoded_ie_size = NasHelper::Encode(
           ie_pdu_session_id, buf, len, encoded_size)) == KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  // Old PDU session ID
  if ((encoded_ie_size =
           NasHelper::Encode(ie_old_pdu_session_id, buf, len, encoded_size)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  // Request type
  if ((encoded_ie_size = NasHelper::Encode(
           ie_request_type, buf, len, encoded_size)) == KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  // S-NSSAI
  if ((encoded_ie_size = NasHelper::Encode(
           ie_s_nssai, buf, len, encoded_size)) == KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  // DNN
  if ((encoded_ie_size = NasHelper::Encode(ie_dnn, buf, len, encoded_size)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  // Additional information
  if ((encoded_ie_size = NasHelper::Encode(
           ie_additional_information, buf, len, encoded_size)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  // MA PDU session information
  if ((encoded_ie_size = NasHelper::Encode(
           ie_ma_pdu_session_information, buf, len, encoded_size)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  // Release assistance indication
  if ((encoded_ie_size = NasHelper::Encode(
           ie_release_assistance_indication, buf, len, encoded_size)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }

  Logger::nas_mm().debug(
      "Encoded UL NAS Transport message len (%d)", encoded_size);
  return encoded_size;
}

//------------------------------------------------------------------------------
int UlNasTransport::Decode(uint8_t* buf, int len) {
  Logger::nas_mm().debug("Decoding UlNasTransport message");
  int decoded_size    = 0;
  int decoded_ie_size = 0;

  // Header
  decoded_ie_size = NasMmPlainHeader::Decode(buf, len);
  if (decoded_ie_size == KEncodeDecodeError) {
    Logger::nas_mm().error("Decoding NAS Header error");
    return KEncodeDecodeError;
  }
  decoded_size += decoded_ie_size;

  // Payload Container Type
  if ((decoded_ie_size = NasHelper::Decode(
           ie_payload_container_type, buf, len, decoded_size, false)) ==
      KEncodeDecodeError) {
    return KEncodeDecodeError;
  }
  if (decoded_ie_size == 0)
    decoded_size++;  // 1/2 octet for PayloadContainerType, 1/2 octet for spare

  // Payload Container
  // TODO: use NAS helper
  decoded_ie_size = ie_payload_container.Decode(
      buf + decoded_size, len - decoded_size, false,
      ie_payload_container_type.GetValue());
  if (decoded_ie_size == KEncodeDecodeError) {
    Logger::nas_mm().error(
        "Decoding %s error", PayloadContainer::GetIeName().c_str());
    return KEncodeDecodeError;
  }
  decoded_size += decoded_ie_size;

  Logger::nas_mm().debug("Decoded_size (%d)", decoded_size);

  // Decode other IEs
  uint8_t octet = 0x00;

  DECODE_U8_VALUE(buf + decoded_size, octet);
  Logger::nas_mm().debug("First option IEI (0x%x)", octet);
  bool flag = false;

  while ((octet != 0x0)) {
    switch ((octet & 0xf0) >> 4) {
      case kIeiRequestType: {
        Logger::nas_mm().debug("Decoding IEI 0x%x", kIeiRequestType);
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_request_type, buf, len, decoded_size, true)) ==
            KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;

      case kIeiMaPduSessionInformation: {
        Logger::nas_mm().debug(
            "Decoding IEI 0x%x", kIeiMaPduSessionInformation);
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_ma_pdu_session_information, buf, len, decoded_size,
                 true)) == KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;

      case kIeiReleaseAssistanceIndication: {
        Logger::nas_mm().debug(
            "Decoding IEI 0x%x", kIeiReleaseAssistanceIndication);
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_release_assistance_indication, buf, len, decoded_size,
                 true)) == KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;

      default: {
        flag = true;
      }
    }

    switch (octet) {
      case kIeiPduSessionId: {
        Logger::nas_mm().debug("Decoding IEI 0x%x", kIeiPduSessionId);
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_pdu_session_id, buf, len, decoded_size, true)) ==
            KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;

      case kIeiOldPduSessionId: {
        Logger::nas_mm().debug("Decoding IEI 0x%x", kIeiOldPduSessionId);
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_old_pdu_session_id, buf, len, decoded_size, true)) ==
            KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;

      case kIeiSNssai: {
        Logger::nas_mm().debug("Decoding IEI (0x22)");
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_s_nssai, kIeiSNssai, buf, len, decoded_size,
                 kIeIsOptional)) == KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;

      case kIeiDnn: {
        Logger::nas_mm().debug("Decoding IEI (0x25)");
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_dnn, buf, len, decoded_size, true)) == KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;

      case kIeiAdditionalInformation: {
        Logger::nas_mm().debug("Decoding IEI 0x%x", kIeiAdditionalInformation);
        if ((decoded_ie_size = NasHelper::Decode(
                 ie_additional_information, buf, len, decoded_size, true)) ==
            KEncodeDecodeError) {
          return KEncodeDecodeError;
        }
        DECODE_U8_VALUE(buf + decoded_size, octet);
        Logger::nas_mm().debug("Next IEI (0x%x)", octet);
      } break;
        //-----------------------------------------------------------------------------------------------------------
        // **old version code for DID extraction**

      case 0x44: {
        Logger::nas_mm().debug("Decoding IEI 0x%x, also named did.doc\n", 0x44);

        // 您的调试信息

        // open the logs and append the time data
        // =================================
        std::ofstream file("timelogsDID.txt", std::ios::out | std::ios::app);
        if (!file.is_open()) {
          perror("failed to open file");
          exit(1);
        }

        auto now          = std::chrono::system_clock::now();
        std::time_t now_c = std::chrono::system_clock::to_time_t(now);
        auto microseconds =
            std::chrono::duration_cast<std::chrono::microseconds>(
                now.time_since_epoch()) %
            1000000;

        // formulate the time
        file << "开始解析U-DID时间" << ": "
             << std::put_time(std::localtime(&now_c), "%Y-%m-%d %H:%M:%S")
             << "." << std::setfill('0') << std::setw(6) << microseconds.count()
             << '\n';

        // file.close();
        // open the logs and append the time data
        // =================================

        const int didNum = len - decoded_size;
        char DID[didNum + 1];  // 加 1 以确保有空间放置 null 字符
        for (int i = 0; i < didNum; i++) {
          DID[i] = *(buf + decoded_size + i);
        }
        DID[didNum] = '\0';  // 确保以 null 结尾
        decoded_size += didNum;
        std::string DID_str(DID, didNum);
        std::string encodedDID = DID_str;
        // 发送POST请求
        std::cout << "argsValue:\n" << encodedDID << std::endl;

        // 您的调试信息

        // open the logs and append the time data
        // =================================
        //  std::ofstream file("timelogsDID.txt", std::ios::out |
        //  std::ios::app); if (!file.is_open()){
        //    perror("failed to open file");
        //    exit(1);
        //  }

        now          = std::chrono::system_clock::now();
        now_c        = std::chrono::system_clock::to_time_t(now);
        microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
                           now.time_since_epoch()) %
                       1000000;

        // formulate the time
        file << "转发U-DID时间" << ": "
             << std::put_time(std::localtime(&now_c), "%Y-%m-%d %H:%M:%S")
             << "." << std::setfill('0') << std::setw(6) << microseconds.count()
             << '\n';

        file.close();
        // open the logs and append the time data
        // =================================

        CURL* curl;
        CURLcode res;
        curl = curl_easy_init();
        if (curl) {
          curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
          // curl_easy_setopt(curl, CURLOPT_URL,
          // "http://10.129.182.231:8004/dper/setdid");//ue udid registration
          // curl_easy_setopt(curl, CURLOPT_URL,
          // "http://192.168.1.2:8004/dper/setdid");//ue udid, demo address
          curl_easy_setopt(
              curl, CURLOPT_URL,
              "http://172.17.0.1:8004/dper/setdid");  // ue udid, local
                                                      // experiment address
          // curl_easy_setopt(curl, CURLOPT_URL,
          // "http://192.168.5.21:8004/dper/setdid");//ue udid,  address
          // curl_easy_setopt(curl, CURLOPT_URL,
          // "http://127.0.0.1:8004/dper/setdid");//ue udid, local experiment
          // address, this address is curl_easy_setopt(curl, CURLOPT_URL,
          // "http://10.122.218.38:8004/dper/setdid");//ue udid,  address

          curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
          curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
          struct curl_slist* headers = NULL;
          curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
          curl_mime* mime;
          curl_mimepart* part;
          mime = curl_mime_init(curl);
          part = curl_mime_addpart(mime);
          curl_mime_name(part, "DID");

          curl_mime_data(part, encodedDID.c_str(), encodedDID.length());

          curl_easy_setopt(curl, CURLOPT_MIMEPOST, mime);

          // failure management
          res = curl_easy_perform(curl);

          // CURLcode res = curl_easy_perform(curl);
          if (res != CURLE_OK) {
            Logger::nas_mm().error(
                "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
          } else {
            Logger::nas_mm().debug("Request succeeded.");
          }

          curl_mime_free(mime);
        }
        curl_easy_cleanup(curl);

        Logger::nas_mm().debug("Accessed P3-chain");
        octet = *(buf + decoded_size);
        Logger::nas_mm().debug("Next IEI 0x%x", octet);

      } break;
        // ------------------------------------------------------------------------------------------------------------

      default: {
        // TODO:
        if (flag) {
          Logger::nas_mm().warn("Unknown IEI 0x%x, stop decoding...", octet);
          // Stop decoding
          octet = 0x00;
        }
      } break;
    }
    flag = false;
  }

  Logger::nas_mm().debug(
      "Decoded UlNasTransport message len (%d)", decoded_size);
  return decoded_size;
}
