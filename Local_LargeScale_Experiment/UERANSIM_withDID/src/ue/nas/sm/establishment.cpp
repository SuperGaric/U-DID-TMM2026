//
// This file is a part of UERANSIM open source project.
// Copyright (c) 2021 ALİ GÜNGÖR.
//
// The software and all associated files are licensed under GPL-3.0
// and subject to the terms and conditions defined in LICENSE file.
//

#include "sm.hpp"
#include <algorithm>
#include <iostream>
#include <lib/nas/proto_conf.hpp>
#include <lib/nas/utils.hpp>
#include <string>
#include <ue/app/task.hpp>
#include <ue/nas/mm/mm.hpp>
#include <utils/common.hpp>
#include <utils/options.hpp>
// #include <curl/curl.h>
#include "httplib.h"

#include <fstream>
#include <chrono>
#include <iomanip>
#include <ctime>

namespace nr::ue
{

std::string send_imsi_to_didserver(const std::string &imsi, int didserver)
{
    httplib::Client cli("http://172.17.0.1:" + std::to_string(didserver));
    cli.set_connection_timeout(10);
    cli.set_read_timeout(10);
    httplib::Headers headers = {{"Content-Type", "application/json"}};

    std::string data = "{\n\"IMSI\":\"" + imsi + "\"\n}";

    // auto res = cli.Post("/hello", headers, data, "application/json");
    auto res = cli.Post("/hello", headers, data, "application/json");

    if (res)
    {
        if (res->status == 200)
        {
            std::cout << "Response from server: " << res->body << std::endl;
            return res->body;
        }
        else
        {
            std::cerr << "Failed to get a valid response, status: " << res->status << std::endl;
            std::cerr << "Response body:" << res->body << std::endl;
            return "";
        }
    }
    else
    {
        std::cerr << "HTTP request failed, error code: " << res.error() << std::endl;
        return "";
    }
}

// 无法引用curl，作废
//  size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
//      size_t total_size = size * nmemb;
//      std::string* response = reinterpret_cast<std::string*>(userp);
//      response->append(reinterpret_cast<char*>(contents), total_size);
//      return total_size;
//  }

// std::string send_imsi_to_didserver(const std::string& imsi, int didserver){
//     CURL *curl;
//     CURLcode res;

//     curl = curl_easy_init();
//     if (curl) {
//         std::string url = "http://localhost:" + std::to_string(didserver) + "/hello";
//         curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
//         curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
//         curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "http");

//         struct curl_slist *headers = nullptr;
//         headers = curl_slist_append(headers, "Content-Type: application/json");
//         curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

//         std::string data = "{\n\"IMSI\" : \"" + imsi + "\"\n}";

//         curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());

//         std::string response_data;
//         curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
//         curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_data);

//         res = curl_easy_perform(curl);

//         if (res != CURLE_OK) {
//             std::cerr << "CURL failed: " << curl_easy_strerror(res) << std::endl;
//         } else {
//             std::cout << "Response from server: " << response_data << std::endl;

//             std::cout << "Received IMSI from server: " << response_data << std::endl;
//         }

//         curl_easy_cleanup(curl);

//         return response_data;

//     }
//     curl_global_cleanup();
// }

static nas::IE5gSmCapability MakeSmCapability()
{
    nas::IE5gSmCapability cap{};
    cap.rqos = nas::EReflectiveQoS::NOT_SUPPORTED;
    cap.mh6pdu = nas::EMultiHomedIPv6PduSession::NOT_SUPPORTED;
    return cap;
}

static nas::IEIntegrityProtectionMaximumDataRate MakeIntegrityMaxRate(const IntegrityMaxDataRateConfig &config)
{
    nas::IEIntegrityProtectionMaximumDataRate res{};
    res.maxRateDownlink = nas::EMaximumDataRatePerUeForUserPlaneIntegrityProtectionForDownlink::SIXTY_FOUR_KBPS;
    res.maxRateUplink = nas::EMaximumDataRatePerUeForUserPlaneIntegrityProtectionForUplink::SIXTY_FOUR_KBPS;
    if (config.downlinkFull)
        res.maxRateDownlink = nas::EMaximumDataRatePerUeForUserPlaneIntegrityProtectionForDownlink::FULL_DATA_RATE;
    if (config.uplinkFull)
        res.maxRateUplink = nas::EMaximumDataRatePerUeForUserPlaneIntegrityProtectionForUplink::FULL_DATA_RATE;
    return res;
}

// 注意
std::string stringToHex(const std::string &str)
{
    std::string hex_str;
    for (size_t i = 0; i < str.size(); ++i)
    {
        char buf[3];
        snprintf(buf, sizeof(buf), "%02x", (unsigned char)str[i]);
        hex_str += buf;
    }
    return hex_str;
}

std::string extractDID(const std::string &response)
{
    size_t did_pos = response.find("\"Id\":\"");
    size_t pk_pos = response.find("\",\"Pk\":");
    if (did_pos != std::string::npos && pk_pos != std::string::npos)
    {
        return response.substr(did_pos + 6, pk_pos - did_pos - 6);
    }
    return "";
}

void NasSm::sendEstablishmentRequest(const SessionConfig &config)
{
    m_logger->debug("Sending PDU Session Establishment Request");

    /* Control the protocol state */
    if (m_mm->m_rmState != ERmState::RM_REGISTERED)
    {
        m_logger->err("PDU session establishment could not be triggered, UE is not registered");
        return;
    }

    if (m_mm->m_mmSubState == EMmSubState::MM_REGISTERED_NON_ALLOWED_SERVICE && !m_mm->hasEmergency() &&
        !m_mm->isHighPriority())
    {
        m_logger->err("PDU session establishment could not be triggered, non allowed service condition");
        return;
    }

    /* Control the received config */
    if (config.type != nas::EPduSessionType::IPV4)
    {
        m_logger->err("PDU session type [%s] is not supported", nas::utils::EnumToString(config.type));
        return;
    }
    if (m_mm->m_rmState == ERmState::RM_REGISTERED && m_mm->m_registeredForEmergency && !config.isEmergency)
    {
        m_logger->err("Non-emergency PDU session cannot be requested, UE is registered for emergency only");
        return;
    }
    if (config.isEmergency && anyEmergencySession())
    {
        m_logger->err(
            "Emergency PDU session cannot be requested, another emergency session already established or establishing");
        return;
    }

    /* Allocate PSI */
    int psi = allocatePduSessionId(config);
    if (psi == 0)
        return;

    /* Allocate PTI */
    int pti = allocateProcedureTransactionId();
    if (pti == 0)
    {
        freePduSessionId(psi);
        return;
    }

    /* Set relevant fields of the PS description */
    auto &ps = m_pduSessions[psi];
    ps->psState = EPsState::ACTIVE_PENDING;
    ps->sessionType = config.type;
    ps->apn = config.apn;
    ps->sNssai = config.sNssai;
    ps->isEmergency = config.isEmergency;
    ps->authorizedQoSRules = {};
    ps->sessionAmbr = {};
    ps->authorizedQoSFlowDescriptions = {};
    ps->pduAddress = {};
    ps->uplinkPending = false;

    /* Make PCO */
    nas::ProtocolConfigurationOptions opt{};
    opt.additionalParams.push_back(std::make_unique<nas::ProtocolConfigurationItem>(
        nas::EProtocolConfigId::CONT_ID_UP_IP_ADDRESS_ALLOCATION_VIA_NAS_SIGNALLING, true, OctetString::Empty()));
    opt.additionalParams.push_back(std::make_unique<nas::ProtocolConfigurationItem>(
        nas::EProtocolConfigId::CONT_ID_DOWN_DNS_SERVER_IPV4_ADDRESS, true, OctetString::Empty()));

    nas::IEExtendedProtocolConfigurationOptions iePco{};
    iePco.configurationProtocol = nas::EConfigurationProtocol::PPP;
    iePco.extension = true;
    iePco.options = opt.encode();

    /* Prepare the establishment request message */
    auto req = std::make_unique<nas::PduSessionEstablishmentRequest>();
    req->pti = pti;
    req->pduSessionId = psi;
    req->integrityProtectionMaximumDataRate = MakeIntegrityMaxRate(m_base->config->integrityMaxRate);
    req->pduSessionType = nas::IEPduSessionType{};
    req->pduSessionType->pduSessionType = nas::EPduSessionType::IPV4;
    req->sscMode = nas::IESscMode{};
    req->sscMode->sscMode = nas::ESscMode::SSC_MODE_1;
    req->extendedProtocolConfigurationOptions = std::move(iePco);
    req->smCapability = MakeSmCapability();

    /* DID function realization */
    std::string imsi_str = m_base->config->supi.value().value;
    printf("m_base->config->supi: %s\n", imsi_str.c_str());
    long long imsi_ll = std::stoll(imsi_str);
    printf("imsi_ll: %lld\n", imsi_ll);
    int ue_num = imsi_ll - 208950000000031;
    int initial_didserver = 8081;

    int didserver = initial_didserver + ue_num;
    printf("This UE's didserver port:%d\n", didserver);
    
    // obtain the time
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
        now.time_since_epoch()
    ) % 1000000;
    // transfer the time form
    std::tm tm = *std::localtime(&time); // 如果需 UTC 用 gmtime
    
    // to time str
    char buffer1[80];
    std::strftime(buffer1, sizeof(buffer1), "%Y-%m-%d %H:%M:%S", &tm);
    
    // logs in the txt
    std::ofstream file("timelogs.txt", std::ios::app);
    if (file) {
        file << "UE发送IMSI时间: " << buffer1 << "." 
            << std::setw(6) << std::setfill('0') << microseconds.count() << "\n";
    }
    
    // send imsi to didserver
    std::string response = send_imsi_to_didserver(imsi_str, didserver);

    time = std::chrono::system_clock::to_time_t(now);
    microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
        now.time_since_epoch()
    ) % 1000000;
    // transfer the time form
    tm = *std::localtime(&time); // 如果需 UTC 用 gmtime
    
    // to time str
    char buffer2[80];
    std::strftime(buffer2, sizeof(buffer2), "%Y-%m-%d %H:%M:%S", &tm);
    
    // logs in the txt

    if (file) {
        file << "接受did时间: " << buffer2 << "." 
            << std::setw(6) << std::setfill('0') << microseconds.count() << "\n";
    }

    if (!response.empty()) {
    // printf("DID document is: %s\n",response.c_str());
    std::cout << "Received DID from server: " << response << std::endl;

    std::string did = extractDID(response);
    std::cout << "Extracted DID: " << did << std::endl;

    // std::string hex_did = stringToHex(response);
    // std::cout << "Hex DID: " << hex_did << std::endl;

    // req->did = nas::IEdid(response);
    req->did = nas::IEdid(did);
    }

    // req->did = nas::IEdid(hex_did);

    /* Set relevant fields of the PT, and start T3580 */
    auto &pt = m_procedureTransactions[pti];
    pt.state = EPtState::PENDING;
    pt.timer = newTransactionTimer(3580);
    pt.message = std::move(req);
    pt.psi = psi;

    /* Send SM message */
    sendSmMessage(psi, *pt.message);
}

void NasSm::receiveEstablishmentAccept(const nas::PduSessionEstablishmentAccept &msg)
{
    m_logger->debug("PDU Session Establishment Accept received");

    if (!checkPtiAndPsi(msg))
        return;

    freeProcedureTransactionId(msg.pti);

    auto &pduSession = m_pduSessions[msg.pduSessionId];
    if (pduSession->psState != EPsState::ACTIVE_PENDING)
    {
        m_logger->err("PS establishment accept received without being requested");
        sendSmCause(nas::ESmCause::MESSAGE_TYPE_NOT_COMPATIBLE_WITH_THE_PROTOCOL_STATE, msg.pti, msg.pduSessionId);
        return;
    }

    if (msg.smCause.has_value())
    {
        m_logger->warn("SM cause received in PduSessionEstablishmentAccept [%s]",
                       nas::utils::EnumToString(msg.smCause->value));
    }

    pduSession->psState = EPsState::ACTIVE;
    pduSession->authorizedQoSRules = nas::utils::DeepCopyIe(msg.authorizedQoSRules);
    pduSession->sessionAmbr = nas::utils::DeepCopyIe(msg.sessionAmbr);
    pduSession->sessionType = msg.selectedPduSessionType.pduSessionType;

    if (msg.authorizedQoSFlowDescriptions.has_value())
        pduSession->authorizedQoSFlowDescriptions = nas::utils::DeepCopyIe(*msg.authorizedQoSFlowDescriptions);
    else
        pduSession->authorizedQoSFlowDescriptions = {};

    if (msg.pduAddress.has_value())
        pduSession->pduAddress = nas::utils::DeepCopyIe(*msg.pduAddress);
    else
        pduSession->pduAddress = {};

    auto *statusUpdate = new NmUeStatusUpdate(NmUeStatusUpdate::SESSION_ESTABLISHMENT);
    statusUpdate->pduSession = pduSession;
    m_base->appTask->push(statusUpdate);

    m_logger->info("PDU Session establishment is successful PSI[%d]", pduSession->psi);
}

void NasSm::receiveEstablishmentReject(const nas::PduSessionEstablishmentReject &msg)
{
    m_logger->err("PDU Session Establishment Reject received [%s]", nas::utils::EnumToString(msg.smCause.value));

    if (!checkPtiAndPsi(msg))
        return;

    freeProcedureTransactionId(msg.pti);

    auto &pduSession = m_pduSessions[msg.pduSessionId];

    if (pduSession->psState != EPsState::ACTIVE_PENDING)
    {
        m_logger->err("PS establishment reject received without being requested");
        sendSmCause(nas::ESmCause::MESSAGE_TYPE_NOT_COMPATIBLE_WITH_THE_PROTOCOL_STATE, msg.pti, msg.pduSessionId);
        return;
    }

    pduSession->psState = EPsState::INACTIVE;

    if (pduSession->isEmergency)
    {
        // This not much important and no need for now
        // TODO: inform the upper layers of the failure of the procedure
    }
}

} // namespace nr::ue