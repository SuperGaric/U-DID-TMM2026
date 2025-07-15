//
// This file is a part of UERANSIM open source project.
// Copyright (c) 2021 ALİ GÜNGÖR.
//
// The software and all associated files are licensed under GPL-3.0
// and subject to the terms and conditions defined in LICENSE file.
//

#include "task.hpp"

#include <gnb/ngap/task.hpp>
#include <lib/rrc/encode.hpp>
#include <fstream>
#include <chrono>
#include <iomanip>
#include <ctime>

namespace nr::gnb
{

void GnbRrcTask::handleRlsSapMessage(NmGnbRlsToRrc &msg)
{
    switch (msg.present)
    {
    case NmGnbRlsToRrc::SIGNAL_DETECTED: {
        m_logger->debug("UE[%d] new signal detected", msg.ueId);
        triggerSysInfoBroadcast();

                
            // 获取带微秒的当前时间
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        auto microseconds = std::chrono::duration_cast<std::chrono::microseconds>(
            now.time_since_epoch()
        ) % 1000000;
        // 转换成本地时间格式
        std::tm tm = *std::localtime(&time); // 如果需 UTC 用 gmtime
        
        // 格式化时间字符串
        char buffer[80];
        std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &tm);
        
        // 追加写入文件
        std::ofstream file("timelogs.txt", std::ios::app);
        if (file) {
            file << "UE启动的时间: " << buffer << "." 
                << std::setw(6) << std::setfill('0') << microseconds.count() << "\n";
        }
        break;
    }
    case NmGnbRlsToRrc::UPLINK_RRC: {
        handleUplinkRrc(msg.ueId, msg.rrcChannel, msg.data);
        break;
    }
    }
}

} // namespace nr::gnb
